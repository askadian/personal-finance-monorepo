"""
File Upload Processor Lambda Function

This Lambda function is triggered by S3 file uploads and processes financial documents:
- Validates file type and naming
- Parses records from uploaded files (CSV, PDF)
- Writes transactions to DynamoDB Transactions table

Supports modular parser architecture for easy extension.
"""

import json
import os
import boto3
from typing import Dict, Any, List
from decimal import Decimal

from parsers import ParserFactory, DocumentType, ParsedTransaction


# AWS clients (lazy-loaded)
s3_client = None
dynamodb = None

# Environment variables
DYNAMODB_TABLE_NAME = os.environ.get('DYNAMODB_TABLE_NAME', 'Transactions')
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')


def get_s3_client():
    """Get or create S3 client"""
    global s3_client
    if s3_client is None:
        s3_client = boto3.client('s3')
    return s3_client


def get_dynamodb_resource():
    """Get or create DynamoDB resource"""
    global dynamodb
    if dynamodb is None:
        dynamodb = boto3.resource('dynamodb')
    return dynamodb


class DecimalEncoder(json.JSONEncoder):
    """Custom JSON encoder for Decimal types"""
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Main Lambda handler for S3 file upload events
    
    Args:
        event: S3 event containing bucket and object information
        context: Lambda context object
        
    Returns:
        Response dictionary with status and processed records count
    """
    try:
        # Parse S3 event
        records = event.get('Records', [])
        
        if not records:
            return create_response(400, "No S3 records found in event")
        
        total_transactions = 0
        processed_files = []
        failed_files = []
        
        for record in records:
            try:
                # Extract S3 information
                s3_info = record.get('s3', {})
                bucket_name = s3_info.get('bucket', {}).get('name')
                object_key = s3_info.get('object', {}).get('key')
                
                if not bucket_name or not object_key:
                    log_message(f"Invalid S3 record: {record}", "WARNING")
                    continue
                
                log_message(f"Processing file: {object_key} from bucket: {bucket_name}", "INFO")
                
                # Process the file
                transaction_count = process_file(bucket_name, object_key)
                total_transactions += transaction_count
                
                processed_files.append({
                    'file': object_key,
                    'transactions': transaction_count,
                    'status': 'success'
                })
                
                log_message(f"Successfully processed {transaction_count} transactions from {object_key}", "INFO")
                
            except Exception as file_error:
                error_msg = f"Error processing file {object_key}: {str(file_error)}"
                log_message(error_msg, "ERROR")
                failed_files.append({
                    'file': object_key,
                    'error': str(file_error),
                    'status': 'failed'
                })
        
        # Prepare response
        response_body = {
            'processed_files': len(processed_files),
            'failed_files': len(failed_files),
            'total_transactions': total_transactions,
            'files': processed_files + failed_files
        }
        
        status_code = 200 if not failed_files else 207  # 207 = Multi-Status
        return create_response(status_code, response_body)
        
    except Exception as e:
        error_msg = f"Lambda handler error: {str(e)}"
        log_message(error_msg, "ERROR")
        return create_response(500, {"error": error_msg})


def process_file(bucket_name: str, object_key: str) -> int:
    """
    Process a single uploaded file
    
    Args:
        bucket_name: S3 bucket name
        object_key: S3 object key
        
    Returns:
        Number of transactions processed
        
    Raises:
        ValueError: If file validation fails
        Exception: If processing fails
    """
    # Initialize parser factory
    factory = ParserFactory()
    
    # Extract file information
    file_name = object_key.split('/')[-1]
    file_extension = factory.get_file_extension(file_name)
    
    # Validate file extension
    if file_extension not in ['csv', 'pdf']:
        raise ValueError(f"Unsupported file type: .{file_extension}. Supported types: csv, pdf")
    
    # Detect document type from filename
    document_type = factory.detect_document_type(file_name)
    log_message(f"Detected document type: {document_type.value} for file: {file_name}", "INFO")
    
    # Extract user ID from S3 key (expected format: users/{user_id}/...)
    user_id = factory.extract_user_id_from_s3_key(object_key)
    if not user_id:
        raise ValueError(f"Cannot extract user ID from S3 key: {object_key}. Expected format: users/{{user_id}}/...")
    
    log_message(f"Processing file for user: {user_id}", "INFO")
    
    # Download file from S3
    try:
        s3 = get_s3_client()
        response = s3.get_object(Bucket=bucket_name, Key=object_key)
        file_content = response['Body'].read()
    except Exception as e:
        raise Exception(f"Failed to download file from S3: {str(e)}")
    
    # Get appropriate parser
    parser = factory.get_parser(file_extension, document_type)
    if not parser:
        raise ValueError(f"No parser available for file type: .{file_extension}")
    
    # Validate and parse file
    if not parser.validate_file(file_content):
        raise ValueError(f"File validation failed: {file_name}")
    
    transactions = parser.parse(file_content, file_name, user_id, document_type)
    
    if not transactions:
        log_message(f"No transactions found in file: {file_name}", "WARNING")
        return 0
    
    # Write transactions to DynamoDB
    write_transactions_to_dynamodb(transactions)
    
    return len(transactions)


def write_transactions_to_dynamodb(transactions: List[ParsedTransaction]) -> None:
    """
    Write parsed transactions to DynamoDB table
    
    Args:
        transactions: List of parsed transactions
        
    Raises:
        Exception: If DynamoDB write fails
    """
    db = get_dynamodb_resource()
    table = db.Table(DYNAMODB_TABLE_NAME)
    
    try:
        # Batch write for efficiency
        with table.batch_writer() as batch:
            for transaction in transactions:
                item = transaction.to_dynamodb_item()
                batch.put_item(Item=item)
        
        log_message(f"Successfully wrote {len(transactions)} transactions to DynamoDB", "INFO")
        
    except Exception as e:
        raise Exception(f"Failed to write to DynamoDB: {str(e)}")


def create_response(status_code: int, body: Any) -> Dict[str, Any]:
    """
    Create Lambda response
    
    Args:
        status_code: HTTP status code
        body: Response body (dict or string)
        
    Returns:
        Lambda response dictionary
    """
    if isinstance(body, str):
        body = {"message": body}
    
    return {
        'statusCode': status_code,
        'body': json.dumps(body, cls=DecimalEncoder)
    }


def log_message(message: str, level: str = "INFO") -> None:
    """
    Log message with level
    
    Args:
        message: Log message
        level: Log level (INFO, WARNING, ERROR)
    """
    # In production, this could integrate with CloudWatch Logs Insights
    print(f"[{level}] {message}")

"""
Personal Finance API Lambda Handler

This Lambda function handles all GET requests for the Personal Finance API.
It responds to requests for transactions, income, expenses, net worth, and files.
"""

import json
import os
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, List, Optional
from decimal import Decimal
import boto3
import uuid


class DecimalEncoder(json.JSONEncoder):
    """Custom JSON encoder for Decimal types from DynamoDB"""
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)


# Initialize S3 client
s3_client = boto3.client('s3')
BUCKET_NAME = os.environ.get('S3_BUCKET_NAME', 'personal-finance-uploads-dev')
PRESIGNED_URL_EXPIRATION = 300  # 5 minutes


def create_response(status_code: int, body: Dict[str, Any]) -> Dict[str, Any]:
    """Create a standardized API Gateway response"""
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Methods': 'GET,POST,OPTIONS'
        },
        'body': json.dumps(body, cls=DecimalEncoder)
    }


def create_error_response(status_code: int, message: str) -> Dict[str, Any]:
    """Create a standardized error response"""
    return create_response(status_code, {
        'error': {
            'message': message,
            'statusCode': status_code
        }
    })


def get_user_id(event: Dict[str, Any]) -> Optional[str]:
    """Extract user ID from Cognito authorizer context"""
    try:
        # In production, this would come from Cognito authorizer
        authorizer = event.get('requestContext', {}).get('authorizer', {})
        user_id = authorizer.get('claims', {}).get('sub')
        
        # For testing without Cognito, allow a header override
        if not user_id:
            user_id = event.get('headers', {}).get('X-User-Id', 'user_123')
        
        return user_id
    except Exception:
        return None


def parse_query_params(event: Dict[str, Any]) -> Dict[str, Any]:
    """Parse and validate query parameters"""
    params = event.get('queryStringParameters') or {}
    return params


def get_transactions(event: Dict[str, Any]) -> Dict[str, Any]:
    """Handle GET /transactions endpoint"""
    user_id = get_user_id(event)
    if not user_id:
        return create_error_response(401, 'Unauthorized: User ID not found')
    
    params = parse_query_params(event)
    
    # Extract and validate query parameters
    start_date = params.get('startDate')
    end_date = params.get('endDate')
    category = params.get('category')
    limit = int(params.get('limit', 50))
    offset = int(params.get('offset', 0))
    
    # Mock data - in production, this would query DynamoDB
    mock_transactions = [
        {
            "id": "txn_001",
            "userId": user_id,
            "date": "2024-01-15",
            "amount": -45.67,
            "description": "Grocery Store Purchase",
            "category": "groceries",
            "merchant": "Whole Foods",
            "type": "debit",
            "accountId": "acc_001",
            "createdAt": "2024-01-16T10:30:00Z",
            "updatedAt": "2024-01-16T10:30:00Z"
        },
        {
            "id": "txn_002",
            "userId": user_id,
            "date": "2024-01-14",
            "amount": -120.00,
            "description": "Electric Bill",
            "category": "utilities",
            "merchant": "Power Company",
            "type": "debit",
            "accountId": "acc_001",
            "createdAt": "2024-01-15T08:15:00Z",
            "updatedAt": "2024-01-15T08:15:00Z"
        }
    ]
    
    # Apply filters
    filtered_transactions = mock_transactions
    if category:
        filtered_transactions = [t for t in filtered_transactions if t['category'] == category]
    
    # Apply pagination
    paginated_transactions = filtered_transactions[offset:offset + limit]
    
    return create_response(200, {
        'data': paginated_transactions,
        'pagination': {
            'limit': limit,
            'offset': offset,
            'total': len(filtered_transactions)
        }
    })


def get_transaction_by_id(event: Dict[str, Any]) -> Dict[str, Any]:
    """Handle GET /transactions/{transactionId} endpoint"""
    user_id = get_user_id(event)
    if not user_id:
        return create_error_response(401, 'Unauthorized: User ID not found')
    
    transaction_id = event.get('pathParameters', {}).get('transactionId')
    if not transaction_id:
        return create_error_response(400, 'Bad Request: Transaction ID is required')
    
    # Mock data - in production, this would query DynamoDB
    mock_transaction = {
        "id": transaction_id,
        "userId": user_id,
        "date": "2024-01-15",
        "amount": -45.67,
        "description": "Grocery Store Purchase",
        "category": "groceries",
        "merchant": "Whole Foods",
        "type": "debit",
        "accountId": "acc_001",
        "createdAt": "2024-01-16T10:30:00Z",
        "updatedAt": "2024-01-16T10:30:00Z"
    }
    
    return create_response(200, {'data': mock_transaction})


def get_income(event: Dict[str, Any]) -> Dict[str, Any]:
    """Handle GET /income endpoint"""
    user_id = get_user_id(event)
    if not user_id:
        return create_error_response(401, 'Unauthorized: User ID not found')
    
    params = parse_query_params(event)
    
    # Extract query parameters
    start_date = params.get('startDate')
    end_date = params.get('endDate')
    source = params.get('source')
    limit = int(params.get('limit', 50))
    
    # Mock data
    mock_income = [
        {
            "id": "inc_001",
            "userId": user_id,
            "date": "2024-01-31",
            "amount": 5000.00,
            "description": "Monthly Salary",
            "source": "salary",
            "employer": "Tech Corp",
            "taxWithheld": 1200.00,
            "createdAt": "2024-02-01T00:00:00Z",
            "updatedAt": "2024-02-01T00:00:00Z"
        },
        {
            "id": "inc_002",
            "userId": user_id,
            "date": "2024-01-15",
            "amount": 500.00,
            "description": "Freelance Project Payment",
            "source": "freelance",
            "employer": "Client ABC",
            "taxWithheld": 0.00,
            "createdAt": "2024-01-16T00:00:00Z",
            "updatedAt": "2024-01-16T00:00:00Z"
        }
    ]
    
    # Apply filters
    filtered_income = mock_income
    if source:
        filtered_income = [i for i in filtered_income if i['source'] == source]
    
    total_income = sum(i['amount'] for i in filtered_income)
    
    return create_response(200, {
        'data': filtered_income[:limit],
        'summary': {
            'totalIncome': total_income,
            'averageMonthly': total_income
        }
    })


def get_income_summary(event: Dict[str, Any]) -> Dict[str, Any]:
    """Handle GET /income/summary endpoint"""
    user_id = get_user_id(event)
    if not user_id:
        return create_error_response(401, 'Unauthorized: User ID not found')
    
    params = parse_query_params(event)
    
    # Mock summary data
    summary = {
        "userId": user_id,
        "totalIncome": 5500.00,
        "averageMonthly": 5500.00,
        "bySource": {
            "salary": 5000.00,
            "freelance": 500.00,
            "bonus": 0.00,
            "investment": 0.00,
            "other": 0.00
        },
        "period": {
            "startDate": "2024-01-01",
            "endDate": "2024-01-31"
        }
    }
    
    return create_response(200, {'data': summary})


def get_expenses(event: Dict[str, Any]) -> Dict[str, Any]:
    """Handle GET /expenses endpoint"""
    user_id = get_user_id(event)
    if not user_id:
        return create_error_response(401, 'Unauthorized: User ID not found')
    
    params = parse_query_params(event)
    
    # Extract query parameters
    start_date = params.get('startDate')
    end_date = params.get('endDate')
    category = params.get('category')
    limit = int(params.get('limit', 50))
    
    # Mock data
    mock_expenses = [
        {
            "id": "exp_001",
            "userId": user_id,
            "date": "2024-01-15",
            "amount": 1500.00,
            "description": "Monthly Rent",
            "category": "rent",
            "merchant": "Property Management LLC",
            "isRecurring": True,
            "createdAt": "2024-01-16T00:00:00Z",
            "updatedAt": "2024-01-16T00:00:00Z"
        },
        {
            "id": "exp_002",
            "userId": user_id,
            "date": "2024-01-10",
            "amount": 150.00,
            "description": "Grocery Shopping",
            "category": "groceries",
            "merchant": "Whole Foods",
            "isRecurring": False,
            "createdAt": "2024-01-11T00:00:00Z",
            "updatedAt": "2024-01-11T00:00:00Z"
        }
    ]
    
    # Apply filters
    filtered_expenses = mock_expenses
    if category:
        filtered_expenses = [e for e in filtered_expenses if e['category'] == category]
    
    total_expenses = sum(e['amount'] for e in filtered_expenses)
    
    return create_response(200, {
        'data': filtered_expenses[:limit],
        'summary': {
            'totalExpenses': total_expenses,
            'averageMonthly': total_expenses
        }
    })


def get_expenses_summary(event: Dict[str, Any]) -> Dict[str, Any]:
    """Handle GET /expenses/summary endpoint"""
    user_id = get_user_id(event)
    if not user_id:
        return create_error_response(401, 'Unauthorized: User ID not found')
    
    params = parse_query_params(event)
    
    # Mock summary data
    summary = {
        "userId": user_id,
        "totalExpenses": 1650.00,
        "averageMonthly": 1650.00,
        "byCategory": {
            "rent": 1500.00,
            "groceries": 150.00,
            "utilities": 0.00,
            "entertainment": 0.00,
            "healthcare": 0.00,
            "transportation": 0.00,
            "dining": 0.00,
            "shopping": 0.00,
            "other": 0.00
        },
        "period": {
            "startDate": "2024-01-01",
            "endDate": "2024-01-31"
        }
    }
    
    return create_response(200, {'data': summary})


def get_networth(event: Dict[str, Any]) -> Dict[str, Any]:
    """Handle GET /networth endpoint"""
    user_id = get_user_id(event)
    if not user_id:
        return create_error_response(401, 'Unauthorized: User ID not found')
    
    # Mock net worth data
    networth = {
        "userId": user_id,
        "totalAssets": 50000.00,
        "totalLiabilities": 15000.00,
        "netWorth": 35000.00,
        "lastUpdated": "2024-01-31T23:59:59Z",
        "breakdown": {
            "assets": {
                "cash": 10000.00,
                "investments": 30000.00,
                "realEstate": 0.00,
                "other": 10000.00
            },
            "liabilities": {
                "creditCard": 5000.00,
                "studentLoan": 10000.00,
                "mortgage": 0.00,
                "other": 0.00
            }
        }
    }
    
    return create_response(200, {'data': networth})


def get_files(event: Dict[str, Any]) -> Dict[str, Any]:
    """Handle GET /files endpoint"""
    user_id = get_user_id(event)
    if not user_id:
        return create_error_response(401, 'Unauthorized: User ID not found')
    
    params = parse_query_params(event)
    
    # Mock files data
    mock_files = [
        {
            "id": "file_001",
            "userId": user_id,
            "fileName": "statement_2024_01.pdf",
            "fileType": "application/pdf",
            "fileSize": 245678,
            "uploadDate": "2024-01-15T10:30:00Z",
            "status": "processed",
            "s3Key": f"users/{user_id}/statements/statement_2024_01.pdf"
        },
        {
            "id": "file_002",
            "userId": user_id,
            "fileName": "paystub_2024_01.pdf",
            "fileType": "application/pdf",
            "fileSize": 128456,
            "uploadDate": "2024-01-31T15:45:00Z",
            "status": "processed",
            "s3Key": f"users/{user_id}/paystubs/paystub_2024_01.pdf"
        }
    ]
    
    return create_response(200, {
        'data': mock_files,
        'pagination': {
            'total': len(mock_files)
        }
    })


def generate_upload_url(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle POST /upload-url endpoint
    Generate presigned URL for S3 file upload
    """
    user_id = get_user_id(event)
    if not user_id:
        return create_error_response(401, 'Unauthorized: User ID not found')
    
    try:
        # Parse request body
        body = json.loads(event.get('body', '{}'))
        file_key = body.get('fileKey')
        content_type = body.get('contentType', 'application/octet-stream')
        
        if not file_key:
            return create_error_response(400, 'fileKey is required')
        
        # Validate file key format (must start with users/)
        if not file_key.startswith('users/'):
            return create_error_response(400, 'Invalid fileKey format. Must start with users/')
        
        # Verify that the file key belongs to the authenticated user
        expected_prefix = f'users/{user_id}/'
        if not file_key.startswith(expected_prefix):
            return create_error_response(403, 'Unauthorized: Cannot upload to another user\'s folder')
        
        # Validate file extension
        allowed_extensions = ['.pdf', '.csv', '.xlsx', '.xls']
        if not any(file_key.lower().endswith(ext) for ext in allowed_extensions):
            return create_error_response(400, 'Invalid file type. Only PDF, CSV, and Excel files are allowed')
        
        # Generate presigned URL
        presigned_url = s3_client.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': BUCKET_NAME,
                'Key': file_key,
                'ContentType': content_type
            },
            ExpiresIn=PRESIGNED_URL_EXPIRATION
        )
        
        # Generate file ID
        file_id = str(uuid.uuid4())
        
        # Calculate expiration time
        expires_at = (datetime.now(timezone.utc) + timedelta(seconds=PRESIGNED_URL_EXPIRATION)).isoformat().replace('+00:00', 'Z')
        
        return create_response(200, {
            'uploadUrl': presigned_url,
            'fileId': file_id,
            'expiresAt': expires_at
        })
        
    except json.JSONDecodeError:
        return create_error_response(400, 'Invalid JSON in request body')
    except Exception as e:
        print(f"Error generating presigned URL: {str(e)}")
        return create_error_response(500, f'Failed to generate upload URL: {str(e)}')


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Main Lambda handler for Personal Finance API
    
    Routes requests to appropriate handler functions based on the HTTP path and method.
    """
    try:
        # Extract path and method for both API Gateway REST API (payload v1)
        # and HTTP API (payload v2)
        path = event.get('path') or event.get('rawPath', '')
        method = event.get('httpMethod') or event.get('requestContext', {}).get('http', {}).get('method', '')
        method = method.upper()
        
        # Handle OPTIONS for CORS preflight
        if method == 'OPTIONS':
            return create_response(200, {})
        
        # Route GET requests
        if method == 'GET':
            if path == '/transactions' or path == '/v1/transactions':
                return get_transactions(event)
            elif path.startswith('/transactions/') or path.startswith('/v1/transactions/'):
                return get_transaction_by_id(event)
            elif path == '/income/summary' or path == '/v1/income/summary':
                return get_income_summary(event)
            elif path == '/income' or path == '/v1/income':
                return get_income(event)
            elif path == '/expenses/summary' or path == '/v1/expenses/summary':
                return get_expenses_summary(event)
            elif path == '/expenses' or path == '/v1/expenses':
                return get_expenses(event)
            elif path == '/networth' or path == '/v1/networth':
                return get_networth(event)
            elif path == '/files' or path == '/v1/files':
                return get_files(event)
            else:
                return create_error_response(404, f'Not Found: Path {path} not found')
        
        # Route POST requests
        elif method == 'POST':
            if path == '/upload-url' or path == '/v1/upload-url':
                return generate_upload_url(event)
            else:
                return create_error_response(404, f'Not Found: Path {path} not found')
        
        else:
            return create_error_response(405, f'Method Not Allowed: {method}')
    
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return create_error_response(500, f'Internal Server Error: {str(e)}')

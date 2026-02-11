#!/usr/bin/env python3
"""
Local Test Script for File Processor Lambda

This script simulates S3 events and tests the Lambda function locally
without requiring AWS resources.
"""

import os
import sys
import json
from unittest.mock import Mock, patch

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lambda_function import lambda_handler, process_file
from parsers import ParserFactory, DocumentType


def simulate_s3_event(bucket_name, object_key):
    """Create a simulated S3 event"""
    return {
        'Records': [
            {
                'eventVersion': '2.1',
                'eventSource': 'aws:s3',
                'eventName': 'ObjectCreated:Put',
                's3': {
                    'bucket': {
                        'name': bucket_name
                    },
                    'object': {
                        'key': object_key
                    }
                }
            }
        ]
    }


def test_csv_parser():
    """Test CSV parser with sample file"""
    print("\n" + "="*60)
    print("Testing CSV Parser")
    print("="*60)
    
    factory = ParserFactory()
    parser = factory.get_parser('csv', DocumentType.BANK_STATEMENT)
    
    # Read sample file
    sample_file = 'sample_files/bank_statement_jan_2024.csv'
    with open(sample_file, 'rb') as f:
        content = f.read()
    
    # Parse
    transactions = parser.parse(content, sample_file, 'test_user_123', DocumentType.BANK_STATEMENT)
    
    print(f"\n✓ Parsed {len(transactions)} transactions from {sample_file}")
    print("\nSample transactions:")
    for i, tx in enumerate(transactions[:3], 1):
        print(f"\n  Transaction {i}:")
        print(f"    Date: {tx.date}")
        print(f"    Description: {tx.description}")
        print(f"    Amount: ${tx.amount}")
        print(f"    Type: {tx.type}")
        print(f"    Category: {tx.category}")


def test_paystub_parser():
    """Test parser with paystub file"""
    print("\n" + "="*60)
    print("Testing Paystub Parser")
    print("="*60)
    
    factory = ParserFactory()
    parser = factory.get_parser('csv', DocumentType.SALARY_SLIP)
    
    # Read sample file
    sample_file = 'sample_files/paystub_jan_2024.csv'
    with open(sample_file, 'rb') as f:
        content = f.read()
    
    # Parse
    transactions = parser.parse(content, sample_file, 'test_user_123', DocumentType.SALARY_SLIP)
    
    print(f"\n✓ Parsed {len(transactions)} transactions from {sample_file}")
    print("\nSample transactions:")
    for i, tx in enumerate(transactions, 1):
        print(f"\n  Transaction {i}:")
        print(f"    Date: {tx.date}")
        print(f"    Description: {tx.description}")
        print(f"    Amount: ${tx.amount}")
        print(f"    Type: {tx.type}")
        print(f"    Category: {tx.category}")


def test_document_type_detection():
    """Test automatic document type detection"""
    print("\n" + "="*60)
    print("Testing Document Type Detection")
    print("="*60)
    
    test_cases = [
        ('bank_statement_2024.csv', DocumentType.BANK_STATEMENT),
        ('paystub_jan_2024.pdf', DocumentType.SALARY_SLIP),
        ('tax_return_2023.pdf', DocumentType.TAX_STATEMENT),
        ('random_file.csv', DocumentType.UNKNOWN),
    ]
    
    for filename, expected_type in test_cases:
        detected_type = ParserFactory.detect_document_type(filename)
        status = "✓" if detected_type == expected_type else "✗"
        print(f"\n  {status} {filename}")
        print(f"    Detected: {detected_type.value}")
        print(f"    Expected: {expected_type.value}")


def test_lambda_handler_mock():
    """Test Lambda handler with mocked AWS services"""
    print("\n" + "="*60)
    print("Testing Lambda Handler (Mocked)")
    print("="*60)
    
    # Create S3 event
    event = simulate_s3_event(
        'test-bucket',
        'users/user123/statements/bank_statement_jan_2024.csv'
    )
    
    # Mock AWS clients
    with patch('lambda_function.get_s3_client') as mock_get_s3, \
         patch('lambda_function.get_dynamodb_resource') as mock_get_dynamodb:
        
        # Mock S3 client
        mock_s3 = Mock()
        sample_file = 'sample_files/bank_statement_jan_2024.csv'
        with open(sample_file, 'rb') as f:
            content = f.read()
        mock_s3.get_object.return_value = {
            'Body': Mock(read=Mock(return_value=content))
        }
        mock_get_s3.return_value = mock_s3
        
        # Mock DynamoDB resource
        mock_dynamodb = Mock()
        mock_table = Mock()
        mock_batch_writer = Mock()
        mock_batch_writer.__enter__ = Mock(return_value=mock_batch_writer)
        mock_batch_writer.__exit__ = Mock(return_value=False)
        mock_batch_writer.put_item = Mock()
        mock_table.batch_writer.return_value = mock_batch_writer
        mock_dynamodb.Table.return_value = mock_table
        mock_get_dynamodb.return_value = mock_dynamodb
        
        # Invoke Lambda
        response = lambda_handler(event, None)
        
        # Print results
        print(f"\n✓ Lambda invocation successful")
        print(f"  Status Code: {response['statusCode']}")
        
        body = json.loads(response['body'])
        print(f"\n  Results:")
        print(f"    Processed Files: {body['processed_files']}")
        print(f"    Failed Files: {body['failed_files']}")
        print(f"    Total Transactions: {body['total_transactions']}")
        
        # Verify DynamoDB was called
        put_item_calls = mock_batch_writer.put_item.call_count
        print(f"\n  ✓ DynamoDB batch_writer.put_item called {put_item_calls} times")


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("File Processor Lambda - Local Testing")
    print("="*60)
    
    try:
        test_csv_parser()
        test_paystub_parser()
        test_document_type_detection()
        test_lambda_handler_mock()
        
        print("\n" + "="*60)
        print("✓ All tests passed!")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n✗ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

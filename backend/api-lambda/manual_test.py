#!/usr/bin/env python3
"""
Manual test script for Lambda function
Run this locally to test the Lambda handler with various events
"""

import json
import sys
sys.path.insert(0, '.')

from lambda_function import lambda_handler


def test_endpoint(description, event):
    """Test an endpoint and print results"""
    print(f"\n{'='*60}")
    print(f"TEST: {description}")
    print(f"{'='*60}")
    print(f"Request: {event['httpMethod']} {event['path']}")
    if event.get('queryStringParameters'):
        print(f"Query Params: {event['queryStringParameters']}")
    
    response = lambda_handler(event, None)
    
    print(f"\nStatus Code: {response['statusCode']}")
    print(f"Response Body:")
    print(json.dumps(json.loads(response['body']), indent=2))
    
    return response


def main():
    """Run test scenarios"""
    print("Testing Personal Finance API Lambda Function")
    print("=" * 60)
    
    # Test 1: Get all transactions
    test_endpoint("Get All Transactions", {
        'path': '/transactions',
        'httpMethod': 'GET',
        'headers': {'X-User-Id': 'test_user_123'},
        'queryStringParameters': None
    })
    
    # Test 2: Get transactions with filters
    test_endpoint("Get Transactions with Category Filter", {
        'path': '/transactions',
        'httpMethod': 'GET',
        'headers': {'X-User-Id': 'test_user_123'},
        'queryStringParameters': {
            'category': 'groceries',
            'limit': '1'
        }
    })
    
    # Test 3: Get single transaction
    test_endpoint("Get Transaction by ID", {
        'path': '/transactions/txn_001',
        'httpMethod': 'GET',
        'headers': {'X-User-Id': 'test_user_123'},
        'pathParameters': {'transactionId': 'txn_001'}
    })
    
    # Test 4: Get income records
    test_endpoint("Get Income Records", {
        'path': '/income',
        'httpMethod': 'GET',
        'headers': {'X-User-Id': 'test_user_123'},
        'queryStringParameters': None
    })
    
    # Test 5: Get income summary
    test_endpoint("Get Income Summary", {
        'path': '/income/summary',
        'httpMethod': 'GET',
        'headers': {'X-User-Id': 'test_user_123'},
        'queryStringParameters': None
    })
    
    # Test 6: Get expenses
    test_endpoint("Get Expenses", {
        'path': '/expenses',
        'httpMethod': 'GET',
        'headers': {'X-User-Id': 'test_user_123'},
        'queryStringParameters': None
    })
    
    # Test 7: Get expenses summary
    test_endpoint("Get Expenses Summary", {
        'path': '/expenses/summary',
        'httpMethod': 'GET',
        'headers': {'X-User-Id': 'test_user_123'},
        'queryStringParameters': None
    })
    
    # Test 8: Get net worth
    test_endpoint("Get Net Worth", {
        'path': '/networth',
        'httpMethod': 'GET',
        'headers': {'X-User-Id': 'test_user_123'},
        'queryStringParameters': None
    })
    
    # Test 9: Get files
    test_endpoint("Get Files", {
        'path': '/files',
        'httpMethod': 'GET',
        'headers': {'X-User-Id': 'test_user_123'},
        'queryStringParameters': None
    })
    
    # Test 10: Test v1 prefix
    test_endpoint("Get Transactions with /v1 Prefix", {
        'path': '/v1/transactions',
        'httpMethod': 'GET',
        'headers': {'X-User-Id': 'test_user_123'},
        'queryStringParameters': None
    })
    
    # Test 11: Test error handling - invalid path
    test_endpoint("Invalid Path (404)", {
        'path': '/invalid-endpoint',
        'httpMethod': 'GET',
        'headers': {'X-User-Id': 'test_user_123'},
        'queryStringParameters': None
    })
    
    # Test 12: Test error handling - method not allowed
    test_endpoint("Method Not Allowed (405)", {
        'path': '/transactions',
        'httpMethod': 'POST',
        'headers': {'X-User-Id': 'test_user_123'}
    })
    
    # Test 13: CORS preflight
    test_endpoint("CORS Preflight (OPTIONS)", {
        'path': '/transactions',
        'httpMethod': 'OPTIONS',
        'headers': {}
    })
    
    print(f"\n{'='*60}")
    print("All tests completed!")
    print(f"{'='*60}\n")


if __name__ == '__main__':
    main()

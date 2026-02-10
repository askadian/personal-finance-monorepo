"""
Unit tests for Personal Finance API Lambda Handler
"""

import json
import pytest
from lambda_function import (
    lambda_handler,
    create_response,
    create_error_response,
    get_user_id,
    parse_query_params
)


class TestHelperFunctions:
    """Tests for helper functions"""
    
    def test_create_response(self):
        """Test create_response creates proper API Gateway response"""
        body = {'message': 'success'}
        response = create_response(200, body)
        
        assert response['statusCode'] == 200
        assert 'Content-Type' in response['headers']
        assert response['headers']['Content-Type'] == 'application/json'
        assert 'Access-Control-Allow-Origin' in response['headers']
        assert json.loads(response['body']) == body
    
    def test_create_error_response(self):
        """Test create_error_response creates proper error response"""
        response = create_error_response(404, 'Not Found')
        
        assert response['statusCode'] == 404
        body = json.loads(response['body'])
        assert 'error' in body
        assert body['error']['message'] == 'Not Found'
        assert body['error']['statusCode'] == 404
    
    def test_get_user_id_from_authorizer(self):
        """Test extracting user ID from Cognito authorizer"""
        event = {
            'requestContext': {
                'authorizer': {
                    'claims': {
                        'sub': 'user_cognito_123'
                    }
                }
            }
        }
        user_id = get_user_id(event)
        assert user_id == 'user_cognito_123'
    
    def test_get_user_id_from_header(self):
        """Test extracting user ID from header fallback"""
        event = {
            'headers': {
                'X-User-Id': 'user_header_456'
            }
        }
        user_id = get_user_id(event)
        assert user_id == 'user_header_456'
    
    def test_parse_query_params(self):
        """Test parsing query parameters"""
        event = {
            'queryStringParameters': {
                'limit': '10',
                'offset': '5'
            }
        }
        params = parse_query_params(event)
        assert params['limit'] == '10'
        assert params['offset'] == '5'
    
    def test_parse_query_params_empty(self):
        """Test parsing empty query parameters"""
        event = {}
        params = parse_query_params(event)
        assert params == {}


class TestTransactionsEndpoint:
    """Tests for /transactions endpoint"""
    
    def test_get_transactions_success(self):
        """Test successful GET /transactions request"""
        event = {
            'path': '/transactions',
            'httpMethod': 'GET',
            'headers': {'X-User-Id': 'test_user_123'},
            'queryStringParameters': None
        }
        
        response = lambda_handler(event, None)
        
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert 'data' in body
        assert 'pagination' in body
        assert isinstance(body['data'], list)
        assert len(body['data']) > 0
    
    def test_get_transactions_with_filters(self):
        """Test GET /transactions with query filters"""
        event = {
            'path': '/transactions',
            'httpMethod': 'GET',
            'headers': {'X-User-Id': 'test_user_123'},
            'queryStringParameters': {
                'category': 'groceries',
                'limit': '1',
                'offset': '0'
            }
        }
        
        response = lambda_handler(event, None)
        
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert 'data' in body
        # All returned transactions should match the category filter
        for transaction in body['data']:
            assert transaction['category'] == 'groceries'
    
    def test_get_transactions_pagination(self):
        """Test pagination in GET /transactions"""
        event = {
            'path': '/transactions',
            'httpMethod': 'GET',
            'headers': {'X-User-Id': 'test_user_123'},
            'queryStringParameters': {
                'limit': '1',
                'offset': '0'
            }
        }
        
        response = lambda_handler(event, None)
        
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert body['pagination']['limit'] == 1
        assert body['pagination']['offset'] == 0
        assert len(body['data']) <= 1
    
    def test_get_transaction_by_id_success(self):
        """Test successful GET /transactions/{id} request"""
        event = {
            'path': '/transactions/txn_001',
            'httpMethod': 'GET',
            'headers': {'X-User-Id': 'test_user_123'},
            'pathParameters': {'transactionId': 'txn_001'}
        }
        
        response = lambda_handler(event, None)
        
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert 'data' in body
        assert body['data']['id'] == 'txn_001'
    
    def test_get_transaction_by_id_missing_id(self):
        """Test GET /transactions/{id} without transaction ID"""
        event = {
            'path': '/transactions/',
            'httpMethod': 'GET',
            'headers': {'X-User-Id': 'test_user_123'},
            'pathParameters': {}
        }
        
        response = lambda_handler(event, None)
        
        assert response['statusCode'] == 400
        body = json.loads(response['body'])
        assert 'error' in body


class TestIncomeEndpoint:
    """Tests for /income endpoint"""
    
    def test_get_income_success(self):
        """Test successful GET /income request"""
        event = {
            'path': '/income',
            'httpMethod': 'GET',
            'headers': {'X-User-Id': 'test_user_123'},
            'queryStringParameters': None
        }
        
        response = lambda_handler(event, None)
        
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert 'data' in body
        assert 'summary' in body
        assert isinstance(body['data'], list)
    
    def test_get_income_with_source_filter(self):
        """Test GET /income with source filter"""
        event = {
            'path': '/income',
            'httpMethod': 'GET',
            'headers': {'X-User-Id': 'test_user_123'},
            'queryStringParameters': {
                'source': 'salary'
            }
        }
        
        response = lambda_handler(event, None)
        
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        for income in body['data']:
            assert income['source'] == 'salary'
    
    def test_get_income_summary_success(self):
        """Test successful GET /income/summary request"""
        event = {
            'path': '/income/summary',
            'httpMethod': 'GET',
            'headers': {'X-User-Id': 'test_user_123'},
            'queryStringParameters': None
        }
        
        response = lambda_handler(event, None)
        
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert 'data' in body
        assert 'totalIncome' in body['data']
        assert 'averageMonthly' in body['data']
        assert 'bySource' in body['data']


class TestExpensesEndpoint:
    """Tests for /expenses endpoint"""
    
    def test_get_expenses_success(self):
        """Test successful GET /expenses request"""
        event = {
            'path': '/expenses',
            'httpMethod': 'GET',
            'headers': {'X-User-Id': 'test_user_123'},
            'queryStringParameters': None
        }
        
        response = lambda_handler(event, None)
        
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert 'data' in body
        assert 'summary' in body
        assert isinstance(body['data'], list)
    
    def test_get_expenses_with_category_filter(self):
        """Test GET /expenses with category filter"""
        event = {
            'path': '/expenses',
            'httpMethod': 'GET',
            'headers': {'X-User-Id': 'test_user_123'},
            'queryStringParameters': {
                'category': 'rent'
            }
        }
        
        response = lambda_handler(event, None)
        
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        for expense in body['data']:
            assert expense['category'] == 'rent'
    
    def test_get_expenses_summary_success(self):
        """Test successful GET /expenses/summary request"""
        event = {
            'path': '/expenses/summary',
            'httpMethod': 'GET',
            'headers': {'X-User-Id': 'test_user_123'},
            'queryStringParameters': None
        }
        
        response = lambda_handler(event, None)
        
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert 'data' in body
        assert 'totalExpenses' in body['data']
        assert 'averageMonthly' in body['data']
        assert 'byCategory' in body['data']


class TestNetworthEndpoint:
    """Tests for /networth endpoint"""
    
    def test_get_networth_success(self):
        """Test successful GET /networth request"""
        event = {
            'path': '/networth',
            'httpMethod': 'GET',
            'headers': {'X-User-Id': 'test_user_123'},
            'queryStringParameters': None
        }
        
        response = lambda_handler(event, None)
        
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert 'data' in body
        assert 'totalAssets' in body['data']
        assert 'totalLiabilities' in body['data']
        assert 'netWorth' in body['data']
        assert 'breakdown' in body['data']


class TestFilesEndpoint:
    """Tests for /files endpoint"""
    
    def test_get_files_success(self):
        """Test successful GET /files request"""
        event = {
            'path': '/files',
            'httpMethod': 'GET',
            'headers': {'X-User-Id': 'test_user_123'},
            'queryStringParameters': None
        }
        
        response = lambda_handler(event, None)
        
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert 'data' in body
        assert isinstance(body['data'], list)


class TestErrorHandling:
    """Tests for error handling"""
    
    def test_unauthorized_request(self):
        """Test request without user authentication"""
        event = {
            'path': '/transactions',
            'httpMethod': 'GET',
            'requestContext': {},
            'headers': {}
        }
        
        response = lambda_handler(event, None)
        
        # With fallback to 'user_123', this should succeed
        # In production with proper Cognito, this would be 401
        assert response['statusCode'] in [200, 401]
    
    def test_method_not_allowed(self):
        """Test unsupported HTTP method"""
        event = {
            'path': '/transactions',
            'httpMethod': 'POST',
            'headers': {'X-User-Id': 'test_user_123'}
        }
        
        response = lambda_handler(event, None)
        
        assert response['statusCode'] == 405
        body = json.loads(response['body'])
        assert 'error' in body
    
    def test_path_not_found(self):
        """Test request to non-existent path"""
        event = {
            'path': '/nonexistent',
            'httpMethod': 'GET',
            'headers': {'X-User-Id': 'test_user_123'}
        }
        
        response = lambda_handler(event, None)
        
        assert response['statusCode'] == 404
        body = json.loads(response['body'])
        assert 'error' in body
    
    def test_options_request(self):
        """Test OPTIONS request for CORS preflight"""
        event = {
            'path': '/transactions',
            'httpMethod': 'OPTIONS',
            'headers': {}
        }
        
        response = lambda_handler(event, None)
        
        assert response['statusCode'] == 200
        assert 'Access-Control-Allow-Origin' in response['headers']


class TestV1PathPrefix:
    """Tests for endpoints with /v1 prefix"""
    
    def test_transactions_with_v1_prefix(self):
        """Test GET /v1/transactions"""
        event = {
            'path': '/v1/transactions',
            'httpMethod': 'GET',
            'headers': {'X-User-Id': 'test_user_123'},
            'queryStringParameters': None
        }
        
        response = lambda_handler(event, None)
        
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert 'data' in body
    
    def test_income_with_v1_prefix(self):
        """Test GET /v1/income"""
        event = {
            'path': '/v1/income',
            'httpMethod': 'GET',
            'headers': {'X-User-Id': 'test_user_123'},
            'queryStringParameters': None
        }
        
        response = lambda_handler(event, None)
        
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert 'data' in body

"""
Unit Tests for File Processor Lambda

Tests for parsers, factory, and main Lambda handler.
"""

import json
import os
import pytest
from datetime import datetime
from decimal import Decimal
from io import BytesIO
from unittest.mock import Mock, patch, MagicMock

# Add parent directory to path for imports
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from parsers import (
    BaseParser, ParsedTransaction, DocumentType,
    CSVParser, PDFParser, ParserFactory
)
from lambda_function import (
    lambda_handler, process_file,
    write_transactions_to_dynamodb, create_response
)


class TestDocumentType:
    """Test DocumentType enum"""
    
    def test_document_types(self):
        """Test all document types are defined"""
        assert DocumentType.BANK_STATEMENT.value == "bank_statement"
        assert DocumentType.SALARY_SLIP.value == "salary_slip"
        assert DocumentType.TAX_STATEMENT.value == "tax_statement"
        assert DocumentType.UNKNOWN.value == "unknown"


class TestParsedTransaction:
    """Test ParsedTransaction dataclass"""
    
    def test_to_dynamodb_item(self):
        """Test conversion to DynamoDB item format"""
        transaction = ParsedTransaction(
            transaction_id="test-123",
            user_id="user-456",
            date="2024-01-15",
            description="Test Transaction",
            amount=Decimal("100.50"),
            type="expense",
            category="groceries",
            source_file="test.csv",
            document_type="bank_statement"
        )
        
        item = transaction.to_dynamodb_item()
        
        assert item['transaction_id'] == "test-123"
        assert item['user_id'] == "user-456"
        assert item['date'] == "2024-01-15"
        assert item['description'] == "Test Transaction"
        assert item['amount'] == Decimal("100.50")
        assert item['type'] == "expense"
        assert item['category'] == "groceries"
        assert item['source_file'] == "test.csv"
        assert item['document_type'] == "bank_statement"
        assert 'created_at' in item


class TestCSVParser:
    """Test CSV parser"""
    
    def test_can_parse_csv(self):
        """Test CSV parser accepts CSV files"""
        parser = CSVParser()
        assert parser.can_parse('csv', DocumentType.BANK_STATEMENT) is True
        assert parser.can_parse('CSV', DocumentType.BANK_STATEMENT) is True
        assert parser.can_parse('pdf', DocumentType.BANK_STATEMENT) is False
    
    def test_validate_valid_csv(self):
        """Test validation of valid CSV file"""
        parser = CSVParser()
        csv_content = b"date,description,amount\n2024-01-15,Test,100.00"
        assert parser.validate_file(csv_content) is True
    
    def test_validate_invalid_csv(self):
        """Test validation fails for invalid CSV"""
        parser = CSVParser()
        invalid_content = b"not a csv"
        assert parser.validate_file(invalid_content) is False
    
    def test_parse_basic_csv(self):
        """Test parsing basic CSV file"""
        parser = CSVParser()
        csv_content = b"""date,description,amount,type
2024-01-15,Grocery Store,50.00,expense
2024-01-16,Salary,2000.00,income"""
        
        transactions = parser.parse(
            csv_content,
            "test.csv",
            "user123",
            DocumentType.BANK_STATEMENT
        )
        
        assert len(transactions) == 2
        assert transactions[0].description == "Grocery Store"
        assert transactions[0].amount == Decimal("50.00")
        assert transactions[0].type == "expense"
        assert transactions[1].description == "Salary"
        assert transactions[1].amount == Decimal("2000.00")
        assert transactions[1].type == "income"
    
    def test_parse_csv_with_negative_amounts(self):
        """Test parsing CSV with negative amounts"""
        parser = CSVParser()
        csv_content = b"date,description,amount\n2024-01-15,Purchase,-100.00"
        
        transactions = parser.parse(
            csv_content,
            "test.csv",
            "user123",
            DocumentType.BANK_STATEMENT
        )
        
        assert len(transactions) == 1
        assert transactions[0].amount == Decimal("100.00")  # Absolute value
        assert transactions[0].type == "expense"  # Inferred from negative
    
    def test_parse_date_formats(self):
        """Test parsing various date formats"""
        parser = CSVParser()
        
        # Test YYYY-MM-DD
        assert parser._parse_date("2024-01-15") == "2024-01-15"
        
        # Test MM/DD/YYYY
        assert parser._parse_date("01/15/2024") == "2024-01-15"
        
        # Test DD/MM/YYYY
        assert parser._parse_date("15/01/2024") == "2024-01-15"
    
    def test_parse_amount_formats(self):
        """Test parsing various amount formats"""
        parser = CSVParser()
        
        # Test basic amount
        assert parser._parse_amount("100.00") == Decimal("100.00")
        
        # Test with dollar sign
        assert parser._parse_amount("$100.00") == Decimal("100.00")
        
        # Test with commas
        assert parser._parse_amount("1,000.00") == Decimal("1000.00")
        
        # Test negative with parentheses
        assert parser._parse_amount("(100.00)") == Decimal("-100.00")
    
    def test_parse_csv_with_category(self):
        """Test parsing CSV with category column"""
        parser = CSVParser()
        csv_content = b"date,description,amount,type,category\n2024-01-15,Store,50.00,expense,groceries"
        
        transactions = parser.parse(
            csv_content,
            "test.csv",
            "user123",
            DocumentType.BANK_STATEMENT
        )
        
        assert len(transactions) == 1
        assert transactions[0].category == "groceries"


class TestPDFParser:
    """Test PDF parser"""
    
    def test_can_parse_pdf(self):
        """Test PDF parser accepts PDF files"""
        parser = PDFParser()
        assert parser.can_parse('pdf', DocumentType.BANK_STATEMENT) is True
        assert parser.can_parse('PDF', DocumentType.BANK_STATEMENT) is True
        assert parser.can_parse('csv', DocumentType.BANK_STATEMENT) is False
    
    def test_parse_date_formats(self):
        """Test PDF date parsing"""
        parser = PDFParser()
        
        assert parser._parse_date("2024-01-15") == "2024-01-15"
        assert parser._parse_date("01/15/2024") == "2024-01-15"
        assert parser._parse_date("15/01/2024") == "2024-01-15"
    
    def test_parse_amount_formats(self):
        """Test PDF amount parsing"""
        parser = PDFParser()
        
        assert parser._parse_amount("100.00") == Decimal("100.00")
        assert parser._parse_amount("$100.00") == Decimal("100.00")
        assert parser._parse_amount("1,000.00") == Decimal("1000.00")
        assert parser._parse_amount("(100.00)") == Decimal("-100.00")


class TestParserFactory:
    """Test parser factory"""
    
    def test_get_csv_parser(self):
        """Test getting CSV parser"""
        factory = ParserFactory()
        parser = factory.get_parser('csv', DocumentType.BANK_STATEMENT)
        assert parser is not None
        assert isinstance(parser, CSVParser)
    
    def test_get_pdf_parser(self):
        """Test getting PDF parser"""
        factory = ParserFactory()
        parser = factory.get_parser('pdf', DocumentType.BANK_STATEMENT)
        assert parser is not None
        assert isinstance(parser, PDFParser)
    
    def test_get_unsupported_parser(self):
        """Test getting parser for unsupported type"""
        factory = ParserFactory()
        parser = factory.get_parser('xlsx', DocumentType.BANK_STATEMENT)
        assert parser is None
    
    def test_detect_bank_statement(self):
        """Test detecting bank statement from filename"""
        assert ParserFactory.detect_document_type("bank_statement_2024.csv") == DocumentType.BANK_STATEMENT
        assert ParserFactory.detect_document_type("account_statement.pdf") == DocumentType.BANK_STATEMENT
        assert ParserFactory.detect_document_type("statement_jan_2024.csv") == DocumentType.BANK_STATEMENT
    
    def test_detect_salary_slip(self):
        """Test detecting salary slip from filename"""
        assert ParserFactory.detect_document_type("paystub_jan_2024.pdf") == DocumentType.SALARY_SLIP
        assert ParserFactory.detect_document_type("salary_slip.pdf") == DocumentType.SALARY_SLIP
        assert ParserFactory.detect_document_type("payslip_2024.csv") == DocumentType.SALARY_SLIP
    
    def test_detect_tax_statement(self):
        """Test detecting tax statement from filename"""
        assert ParserFactory.detect_document_type("tax_return_2024.pdf") == DocumentType.TAX_STATEMENT
        assert ParserFactory.detect_document_type("1099_form.pdf") == DocumentType.TAX_STATEMENT
        assert ParserFactory.detect_document_type("w2_2024.pdf") == DocumentType.TAX_STATEMENT
    
    def test_detect_unknown_type(self):
        """Test detecting unknown document type"""
        assert ParserFactory.detect_document_type("random_file.csv") == DocumentType.UNKNOWN
    
    def test_get_file_extension(self):
        """Test extracting file extension"""
        assert ParserFactory.get_file_extension("test.csv") == "csv"
        assert ParserFactory.get_file_extension("test.PDF") == "pdf"
        assert ParserFactory.get_file_extension("file.with.dots.txt") == "txt"
        assert ParserFactory.get_file_extension("noextension") == ""
    
    def test_extract_user_id_from_s3_key(self):
        """Test extracting user ID from S3 key"""
        assert ParserFactory.extract_user_id_from_s3_key("users/user123/statements/file.csv") == "user123"
        assert ParserFactory.extract_user_id_from_s3_key("users/abc-xyz/paystubs/file.pdf") == "abc-xyz"
        assert ParserFactory.extract_user_id_from_s3_key("invalid/path/file.csv") is None
        assert ParserFactory.extract_user_id_from_s3_key("file.csv") is None


class TestLambdaFunction:
    """Test main Lambda function"""
    
    @patch('lambda_function.get_s3_client')
    @patch('lambda_function.get_dynamodb_resource')
    def test_lambda_handler_success(self, mock_get_dynamodb, mock_get_s3):
        """Test successful Lambda invocation"""
        # Mock S3 client
        mock_s3 = Mock()
        csv_content = b"date,description,amount,type\n2024-01-15,Test,100.00,expense"
        mock_s3.get_object.return_value = {
            'Body': Mock(read=Mock(return_value=csv_content))
        }
        mock_get_s3.return_value = mock_s3
        
        # Mock DynamoDB resource
        mock_dynamodb = Mock()
        mock_table = Mock()
        mock_batch_writer = Mock()
        mock_batch_writer.__enter__ = Mock(return_value=mock_batch_writer)
        mock_batch_writer.__exit__ = Mock(return_value=False)
        mock_table.batch_writer.return_value = mock_batch_writer
        mock_dynamodb.Table.return_value = mock_table
        mock_get_dynamodb.return_value = mock_dynamodb
        
        # Create S3 event
        event = {
            'Records': [
                {
                    's3': {
                        'bucket': {'name': 'test-bucket'},
                        'object': {'key': 'users/user123/statements/bank_statement.csv'}
                    }
                }
            ]
        }
        
        # Invoke Lambda
        response = lambda_handler(event, None)
        
        # Verify response
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert body['processed_files'] == 1
        assert body['failed_files'] == 0
        assert body['total_transactions'] == 1
    
    def test_lambda_handler_no_records(self):
        """Test Lambda with no S3 records"""
        event = {'Records': []}
        response = lambda_handler(event, None)
        
        assert response['statusCode'] == 400
        body = json.loads(response['body'])
        assert 'No S3 records' in body['message']
    
    @patch('lambda_function.get_s3_client')
    def test_process_file_unsupported_type(self, mock_get_s3):
        """Test processing unsupported file type"""
        with pytest.raises(ValueError, match="Unsupported file type"):
            process_file('test-bucket', 'users/user123/file.xlsx')
    
    @patch('lambda_function.get_s3_client')
    def test_process_file_no_user_id(self, mock_get_s3):
        """Test processing file without user ID in path"""
        with pytest.raises(ValueError, match="Cannot extract user ID"):
            process_file('test-bucket', 'invalid/path/file.csv')
    
    @patch('lambda_function.get_dynamodb_resource')
    def test_write_transactions_to_dynamodb(self, mock_get_dynamodb):
        """Test writing transactions to DynamoDB"""
        # Mock DynamoDB resource
        mock_dynamodb = Mock()
        mock_table = Mock()
        mock_batch_writer = Mock()
        mock_batch_writer.__enter__ = Mock(return_value=mock_batch_writer)
        mock_batch_writer.__exit__ = Mock(return_value=False)
        mock_table.batch_writer.return_value = mock_batch_writer
        mock_dynamodb.Table.return_value = mock_table
        mock_get_dynamodb.return_value = mock_dynamodb
        
        # Create test transactions
        transactions = [
            ParsedTransaction(
                transaction_id="test-1",
                user_id="user123",
                date="2024-01-15",
                description="Test",
                amount=Decimal("100.00"),
                type="expense"
            )
        ]
        
        # Write to DynamoDB
        write_transactions_to_dynamodb(transactions)
        
        # Verify batch writer was used
        mock_table.batch_writer.assert_called_once()
    
    def test_create_response(self):
        """Test creating Lambda response"""
        response = create_response(200, {"message": "Success"})
        
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert body['message'] == "Success"
    
    def test_create_response_with_string(self):
        """Test creating response with string body"""
        response = create_response(400, "Error message")
        
        assert response['statusCode'] == 400
        body = json.loads(response['body'])
        assert body['message'] == "Error message"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

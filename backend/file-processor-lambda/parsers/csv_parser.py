"""
CSV Parser Implementation

Parses CSV files for bank statements, salary slips, and other financial documents.
"""

import csv
import io
import uuid
from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import List

from .base_parser import BaseParser, ParsedTransaction, DocumentType


class CSVParser(BaseParser):
    """Parser for CSV files"""
    
    # Expected CSV headers for different document types
    BANK_STATEMENT_HEADERS = {'date', 'description', 'amount'}
    SALARY_SLIP_HEADERS = {'date', 'description', 'amount', 'type'}
    
    def can_parse(self, file_extension: str, document_type: DocumentType) -> bool:
        """Check if this parser can handle CSV files"""
        return file_extension.lower() == 'csv'
    
    def validate_file(self, file_content: bytes) -> bool:
        """Validate CSV file structure"""
        try:
            content = file_content.decode('utf-8')
            reader = csv.DictReader(io.StringIO(content))
            headers = set(h.lower().strip() for h in reader.fieldnames or [])
            
            # Check if we have minimum required headers
            return bool(headers and ('date' in headers and 'amount' in headers))
        except Exception:
            return False
    
    def parse(self, file_content: bytes, file_name: str, user_id: str, 
              document_type: DocumentType) -> List[ParsedTransaction]:
        """
        Parse CSV file and extract transactions
        
        Expected CSV format:
        - date,description,amount,type (optional: category)
        - Date should be in YYYY-MM-DD or MM/DD/YYYY format
        - Amount can be positive or negative
        - Type can be 'income' or 'expense' (optional, inferred from amount if missing)
        """
        if not self.validate_file(file_content):
            raise ValueError(f"Invalid CSV file: {file_name}")
        
        content = file_content.decode('utf-8')
        reader = csv.DictReader(io.StringIO(content))
        
        transactions = []
        for row_num, row in enumerate(reader, start=2):  # Start at 2 (header is row 1)
            try:
                transaction = self._parse_row(row, user_id, file_name, document_type)
                if transaction:
                    transactions.append(transaction)
            except Exception as e:
                # Log warning but continue processing other rows
                print(f"Warning: Failed to parse row {row_num} in {file_name}: {str(e)}")
                continue
        
        if not transactions:
            raise ValueError(f"No valid transactions found in {file_name}")
        
        return transactions
    
    def _parse_row(self, row: dict, user_id: str, file_name: str, 
                   document_type: DocumentType) -> ParsedTransaction:
        """Parse a single CSV row into a transaction"""
        # Normalize keys to lowercase
        row = {k.lower().strip(): v.strip() for k, v in row.items()}
        
        # Extract date
        date_str = row.get('date', '')
        parsed_date = self._parse_date(date_str)
        
        # Extract amount
        amount_str = row.get('amount', '0')
        amount = self._parse_amount(amount_str)
        
        # Determine transaction type
        transaction_type = row.get('type', '').lower()
        if not transaction_type:
            # Infer from amount (negative = expense, positive = income)
            transaction_type = 'expense' if amount < 0 else 'income'
        elif transaction_type not in ['income', 'expense']:
            # Default to expense if invalid
            transaction_type = 'expense'
        
        # Use absolute value for amount
        amount = abs(amount)
        
        # Extract other fields
        description = row.get('description', 'Transaction')
        category = row.get('category', None)
        
        # Generate unique transaction ID
        transaction_id = str(uuid.uuid4())
        
        return ParsedTransaction(
            transaction_id=transaction_id,
            user_id=user_id,
            date=parsed_date,
            description=description,
            amount=amount,
            type=transaction_type,
            category=category,
            source_file=file_name,
            document_type=document_type.value
        )
    
    def _parse_date(self, date_str: str) -> str:
        """Parse date string into ISO format (YYYY-MM-DD)"""
        date_formats = [
            '%Y-%m-%d',      # 2024-01-15
            '%m/%d/%Y',      # 01/15/2024
            '%d/%m/%Y',      # 15/01/2024
            '%Y/%m/%d',      # 2024/01/15
            '%m-%d-%Y',      # 01-15-2024
            '%d-%m-%Y',      # 15-01-2024
        ]
        
        for fmt in date_formats:
            try:
                date_obj = datetime.strptime(date_str, fmt)
                return date_obj.strftime('%Y-%m-%d')
            except ValueError:
                continue
        
        raise ValueError(f"Unable to parse date: {date_str}")
    
    def _parse_amount(self, amount_str: str) -> Decimal:
        """Parse amount string into Decimal"""
        # Remove common currency symbols and whitespace
        cleaned = amount_str.replace('$', '').replace(',', '').replace(' ', '').strip()
        
        # Handle parentheses for negative amounts (e.g., "(100.00)")
        if cleaned.startswith('(') and cleaned.endswith(')'):
            cleaned = '-' + cleaned[1:-1]
        
        try:
            return Decimal(cleaned)
        except (InvalidOperation, ValueError):
            raise ValueError(f"Unable to parse amount: {amount_str}")

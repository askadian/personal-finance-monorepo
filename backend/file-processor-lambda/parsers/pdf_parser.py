"""
PDF Parser Implementation

Parses PDF files for bank statements, salary slips, and other financial documents.
Uses pypdf for PDF text extraction and pattern matching for transaction identification.
"""

import io
import re
import uuid
from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import List, Optional

try:
    from pypdf import PdfReader
except ImportError:
    # Fallback for older versions
    try:
        from PyPDF2 import PdfReader
    except ImportError:
        PdfReader = None

from .base_parser import BaseParser, ParsedTransaction, DocumentType


class PDFParser(BaseParser):
    """Parser for PDF files"""
    
    # Regex patterns for transaction detection
    DATE_PATTERN = r'\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}[/-]\d{1,2}[/-]\d{1,2})\b'
    AMOUNT_PATTERN = r'\$?\s*-?\(?\d{1,3}(?:,\d{3})*(?:\.\d{2})?\)?'
    
    def __init__(self):
        if PdfReader is None:
            raise ImportError("pypdf or PyPDF2 is required for PDF parsing. Install with: pip install pypdf")
    
    def can_parse(self, file_extension: str, document_type: DocumentType) -> bool:
        """Check if this parser can handle PDF files"""
        return file_extension.lower() == 'pdf'
    
    def validate_file(self, file_content: bytes) -> bool:
        """Validate PDF file structure"""
        try:
            pdf = PdfReader(io.BytesIO(file_content))
            # Check if PDF has at least one page with text
            return len(pdf.pages) > 0 and bool(pdf.pages[0].extract_text().strip())
        except Exception:
            return False
    
    def parse(self, file_content: bytes, file_name: str, user_id: str, 
              document_type: DocumentType) -> List[ParsedTransaction]:
        """
        Parse PDF file and extract transactions
        
        This is a basic implementation that uses pattern matching to identify transactions.
        For production, consider using specialized PDF parsing libraries or ML models
        for better accuracy with various PDF formats.
        """
        if not self.validate_file(file_content):
            raise ValueError(f"Invalid PDF file: {file_name}")
        
        # Extract text from PDF
        pdf = PdfReader(io.BytesIO(file_content))
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"
        
        # Parse based on document type
        if document_type == DocumentType.BANK_STATEMENT:
            transactions = self._parse_bank_statement(text, user_id, file_name, document_type)
        elif document_type == DocumentType.SALARY_SLIP:
            transactions = self._parse_salary_slip(text, user_id, file_name, document_type)
        elif document_type == DocumentType.TAX_STATEMENT:
            transactions = self._parse_tax_statement(text, user_id, file_name, document_type)
        else:
            # Generic parsing for unknown types
            transactions = self._parse_generic(text, user_id, file_name, document_type)
        
        if not transactions:
            raise ValueError(f"No valid transactions found in {file_name}")
        
        return transactions
    
    def _parse_bank_statement(self, text: str, user_id: str, file_name: str, 
                             document_type: DocumentType) -> List[ParsedTransaction]:
        """Parse bank statement PDF"""
        transactions = []
        lines = text.split('\n')
        
        for line in lines:
            # Look for lines with date and amount patterns
            dates = re.findall(self.DATE_PATTERN, line)
            amounts = re.findall(self.AMOUNT_PATTERN, line)
            
            if dates and amounts:
                try:
                    # Get the first date and amount from the line
                    date_str = dates[0]
                    amount_str = amounts[-1]  # Usually the last amount is the transaction amount
                    
                    parsed_date = self._parse_date(date_str)
                    amount = self._parse_amount(amount_str)
                    
                    # Extract description (text between date and amount)
                    description = self._extract_description(line, date_str, amount_str)
                    
                    # Determine type (expense if negative, income if positive)
                    transaction_type = 'expense' if amount < 0 else 'income'
                    amount = abs(amount)
                    
                    transaction = ParsedTransaction(
                        transaction_id=str(uuid.uuid4()),
                        user_id=user_id,
                        date=parsed_date,
                        description=description,
                        amount=amount,
                        type=transaction_type,
                        category=None,
                        source_file=file_name,
                        document_type=document_type.value
                    )
                    transactions.append(transaction)
                except (ValueError, InvalidOperation) as e:
                    # Skip invalid lines
                    continue
        
        return transactions
    
    def _parse_salary_slip(self, text: str, user_id: str, file_name: str, 
                          document_type: DocumentType) -> List[ParsedTransaction]:
        """Parse salary slip PDF"""
        # Look for common salary slip patterns
        salary_patterns = [
            r'(?:gross|basic|net)\s+(?:salary|pay)[\s:]*' + self.AMOUNT_PATTERN,
            r'(?:total|net)\s+(?:earnings|payment)[\s:]*' + self.AMOUNT_PATTERN,
        ]
        
        transactions = []
        for pattern in salary_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                try:
                    amount_str = re.findall(self.AMOUNT_PATTERN, match.group())[0]
                    amount = abs(self._parse_amount(amount_str))
                    
                    # Try to find date in the document
                    date_matches = re.findall(self.DATE_PATTERN, text)
                    date_str = date_matches[0] if date_matches else datetime.now().strftime('%Y-%m-%d')
                    parsed_date = self._parse_date(date_str) if date_matches else date_str
                    
                    transaction = ParsedTransaction(
                        transaction_id=str(uuid.uuid4()),
                        user_id=user_id,
                        date=parsed_date,
                        description=f"Salary Payment - {file_name}",
                        amount=amount,
                        type='income',
                        category='salary',
                        source_file=file_name,
                        document_type=document_type.value
                    )
                    transactions.append(transaction)
                except (ValueError, InvalidOperation):
                    continue
        
        return transactions
    
    def _parse_tax_statement(self, text: str, user_id: str, file_name: str, 
                            document_type: DocumentType) -> List[ParsedTransaction]:
        """Parse tax statement PDF"""
        # Simplified tax parsing - look for tax payments
        tax_patterns = [
            r'(?:tax|payment)[\s:]*' + self.AMOUNT_PATTERN,
            r'(?:total|net)\s+(?:tax|liability)[\s:]*' + self.AMOUNT_PATTERN,
        ]
        
        transactions = []
        for pattern in tax_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                try:
                    amount_str = re.findall(self.AMOUNT_PATTERN, match.group())[0]
                    amount = abs(self._parse_amount(amount_str))
                    
                    # Try to find date
                    date_matches = re.findall(self.DATE_PATTERN, text)
                    date_str = date_matches[0] if date_matches else datetime.now().strftime('%Y-%m-%d')
                    parsed_date = self._parse_date(date_str) if date_matches else date_str
                    
                    transaction = ParsedTransaction(
                        transaction_id=str(uuid.uuid4()),
                        user_id=user_id,
                        date=parsed_date,
                        description=f"Tax Payment - {file_name}",
                        amount=amount,
                        type='expense',
                        category='tax',
                        source_file=file_name,
                        document_type=document_type.value
                    )
                    transactions.append(transaction)
                except (ValueError, InvalidOperation):
                    continue
        
        return transactions
    
    def _parse_generic(self, text: str, user_id: str, file_name: str, 
                      document_type: DocumentType) -> List[ParsedTransaction]:
        """Generic parsing for unknown document types"""
        # Use bank statement parser as fallback
        return self._parse_bank_statement(text, user_id, file_name, document_type)
    
    def _extract_description(self, line: str, date_str: str, amount_str: str) -> str:
        """Extract description from a line by removing date and amount"""
        description = line.replace(date_str, '').replace(amount_str, '').strip()
        # Clean up multiple spaces
        description = re.sub(r'\s+', ' ', description)
        return description if description else 'Transaction'
    
    def _parse_date(self, date_str: str) -> str:
        """Parse date string into ISO format (YYYY-MM-DD)"""
        date_formats = [
            '%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y', '%Y/%m/%d',
            '%m-%d-%Y', '%d-%m-%Y', '%m/%d/%y', '%d/%m/%y',
            '%Y%m%d', '%m%d%Y', '%d%m%Y'
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
        # Remove currency symbols, whitespace, and commas
        cleaned = amount_str.replace('$', '').replace(',', '').replace(' ', '').strip()
        
        # Handle parentheses for negative amounts
        if cleaned.startswith('(') and cleaned.endswith(')'):
            cleaned = '-' + cleaned[1:-1]
        
        try:
            return Decimal(cleaned)
        except (InvalidOperation, ValueError):
            raise ValueError(f"Unable to parse amount: {amount_str}")

"""
Parser Factory

Factory class for creating appropriate parsers based on file type.
Implements Factory pattern for parser instantiation.
"""

import re
from typing import Optional

from .base_parser import BaseParser, DocumentType
from .csv_parser import CSVParser
from .pdf_parser import PDFParser


class ParserFactory:
    """Factory for creating file parsers"""
    
    # Document type detection patterns in filenames
    DOCUMENT_TYPE_PATTERNS = {
        DocumentType.BANK_STATEMENT: [
            r'bank.*statement',
            r'statement.*\d{4}',
            r'account.*statement',
        ],
        DocumentType.SALARY_SLIP: [
            r'salary',
            r'pay.*stub',
            r'paystub',
            r'payslip',
            r'pay.*slip',
        ],
        DocumentType.TAX_STATEMENT: [
            r'tax',
            r'1099',
            r'w-?2',
            r'return',
        ]
    }
    
    def __init__(self):
        """Initialize parser factory with available parsers"""
        self.parsers = [
            CSVParser(),
            PDFParser(),
        ]
    
    def get_parser(self, file_extension: str, document_type: DocumentType) -> Optional[BaseParser]:
        """
        Get appropriate parser for the given file type and document type
        
        Args:
            file_extension: File extension without dot (e.g., 'csv', 'pdf')
            document_type: Type of document to parse
            
        Returns:
            Parser instance that can handle the file, or None if no parser found
        """
        for parser in self.parsers:
            if parser.can_parse(file_extension, document_type):
                return parser
        return None
    
    @staticmethod
    def detect_document_type(file_name: str) -> DocumentType:
        """
        Detect document type from filename
        
        Args:
            file_name: Name of the file
            
        Returns:
            Detected document type or UNKNOWN
        """
        file_name_lower = file_name.lower()
        
        for doc_type, patterns in ParserFactory.DOCUMENT_TYPE_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, file_name_lower):
                    return doc_type
        
        return DocumentType.UNKNOWN
    
    @staticmethod
    def get_file_extension(file_name: str) -> str:
        """
        Extract file extension from filename
        
        Args:
            file_name: Name of the file
            
        Returns:
            File extension without dot (e.g., 'csv', 'pdf')
        """
        if '.' in file_name:
            return file_name.rsplit('.', 1)[1].lower()
        return ''
    
    @staticmethod
    def extract_user_id_from_s3_key(s3_key: str) -> Optional[str]:
        """
        Extract user ID from S3 object key
        Expected format: users/{user_id}/...
        
        Args:
            s3_key: S3 object key
            
        Returns:
            User ID or None if not found
        """
        parts = s3_key.split('/')
        if len(parts) >= 2 and parts[0] == 'users':
            return parts[1]
        return None

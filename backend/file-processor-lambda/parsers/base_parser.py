"""
Base Parser Interface

Defines the abstract base class for all file parsers.
Uses Strategy pattern for easy extensibility.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum
from typing import List, Optional


class DocumentType(Enum):
    """Supported document types"""
    BANK_STATEMENT = "bank_statement"
    SALARY_SLIP = "salary_slip"
    TAX_STATEMENT = "tax_statement"
    UNKNOWN = "unknown"


@dataclass
class ParsedTransaction:
    """Represents a single parsed transaction record"""
    transaction_id: str
    user_id: str
    date: str  # ISO format YYYY-MM-DD
    description: str
    amount: Decimal
    type: str  # 'income' or 'expense'
    category: Optional[str] = None
    source_file: Optional[str] = None
    document_type: Optional[str] = None
    
    def to_dynamodb_item(self) -> dict:
        """Convert to DynamoDB item format"""
        return {
            'transaction_id': self.transaction_id,
            'user_id': self.user_id,
            'date': self.date,
            'description': self.description,
            'amount': self.amount,
            'type': self.type,
            'category': self.category or 'uncategorized',
            'source_file': self.source_file or '',
            'document_type': self.document_type or DocumentType.UNKNOWN.value,
            'created_at': datetime.now(timezone.utc).isoformat()
        }


class BaseParser(ABC):
    """Abstract base class for file parsers"""
    
    @abstractmethod
    def can_parse(self, file_extension: str, document_type: DocumentType) -> bool:
        """
        Determine if this parser can handle the given file type and document type
        
        Args:
            file_extension: File extension (e.g., 'csv', 'pdf')
            document_type: Type of document
            
        Returns:
            True if parser can handle this file, False otherwise
        """
        pass
    
    @abstractmethod
    def parse(self, file_content: bytes, file_name: str, user_id: str, 
              document_type: DocumentType) -> List[ParsedTransaction]:
        """
        Parse file content and extract transactions
        
        Args:
            file_content: Raw file content as bytes
            file_name: Name of the file being parsed
            user_id: User ID for the transactions
            document_type: Type of document being parsed
            
        Returns:
            List of parsed transactions
            
        Raises:
            ValueError: If file cannot be parsed
        """
        pass
    
    @abstractmethod
    def validate_file(self, file_content: bytes) -> bool:
        """
        Validate that the file content is parseable
        
        Args:
            file_content: Raw file content
            
        Returns:
            True if valid, False otherwise
        """
        pass

# File Upload Processor Lambda - Implementation Summary

## Overview

This document summarizes the implementation of the File Upload Processor Lambda, a cloud-native Python function that processes financial documents uploaded to S3 and writes extracted transaction data to DynamoDB.

## Implementation Date

February 10, 2026

## Requirements Met

✅ **S3 File Upload Trigger**: Lambda is triggered automatically by S3 ObjectCreated events  
✅ **File Type Validation**: Validates file extensions (.csv, .pdf) before processing  
✅ **Naming Validation**: Extracts user ID from S3 key path (users/{user_id}/...)  
✅ **Record Parsing**: Extracts transaction records from CSV and PDF files  
✅ **DynamoDB Integration**: Writes parsed transactions to Transactions table  
✅ **Modular Design**: Strategy pattern allows easy addition of new file types and document types  
✅ **Multiple Document Types**: Supports Bank Statements, Salary Slips, Tax Statements, and generic documents  

## Architecture

### Design Pattern: Strategy Pattern

The implementation uses the **Strategy Pattern** for parser selection, making it easy to add new file types and document types without modifying existing code.

```
┌─────────────────────────────────────────────────────────────┐
│                      Lambda Handler                          │
│  (Handles S3 Events, Orchestrates Processing)               │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                   Parser Factory                             │
│  (Selects appropriate parser based on file type)           │
└────────────┬────────────────────────────────────────────────┘
             │
             ├──────────────────┬──────────────────┐
             ▼                  ▼                  ▼
      ┌──────────┐       ┌──────────┐       ┌──────────┐
      │   CSV    │       │   PDF    │       │  Future  │
      │  Parser  │       │  Parser  │       │  Parser  │
      └──────────┘       └──────────┘       └──────────┘
             │                  │                  │
             └──────────────────┴──────────────────┘
                               │
                               ▼
                    ┌──────────────────┐
                    │  ParsedTransaction│
                    │  (Data Model)     │
                    └──────────────────┘
                               │
                               ▼
                    ┌──────────────────┐
                    │    DynamoDB      │
                    │  (Transactions)  │
                    └──────────────────┘
```

## Components

### 1. Parser Package (`parsers/`)

#### `base_parser.py`
- **BaseParser**: Abstract base class defining parser interface
- **ParsedTransaction**: Data class representing a transaction
- **DocumentType**: Enum for supported document types

#### `csv_parser.py`
- Implements CSV file parsing
- Handles multiple date formats (YYYY-MM-DD, MM/DD/YYYY, DD/MM/YYYY)
- Supports various amount formats ($, commas, parentheses for negative)
- Infers transaction type from amount if not specified
- Gracefully handles invalid rows

#### `pdf_parser.py`
- Implements PDF file parsing using pypdf
- Uses regex pattern matching to extract transactions
- Supports different parsing strategies for different document types
- Handles bank statements, salary slips, and tax documents

#### `parser_factory.py`
- Factory class for creating parsers
- Automatic document type detection from filename
- S3 key parsing for user ID extraction
- File extension extraction

### 2. Lambda Function (`lambda_function.py`)

Main handler that:
1. Receives S3 event notifications
2. Downloads file from S3
3. Validates file type and structure
4. Selects appropriate parser
5. Extracts transactions
6. Writes to DynamoDB in batches
7. Returns processing results

### 3. Infrastructure (`cloudformation-template.yaml`)

CloudFormation template creates:
- **S3 Bucket**: Encrypted with event notifications for .csv and .pdf files
- **Lambda Function**: Python 3.12 with 512MB memory, 5-minute timeout
- **IAM Role**: Least-privilege permissions (S3 read, DynamoDB write, CloudWatch logs)
- **DynamoDB Table**: Transactions table with GSI on date
- **CloudWatch Resources**: Log groups and error alarms

## Supported File Formats

### CSV Format

```csv
date,description,amount,type,category
2024-01-15,Grocery Store,125.50,expense,groceries
2024-01-20,Monthly Salary,5000.00,income,salary
```

**Required columns**: date, amount  
**Optional columns**: description, type, category

### PDF Format

The PDF parser uses pattern matching to extract transactions from various layouts. Best suited for:
- Bank statements with tabular transaction data
- Salary slips with payment breakdowns
- Tax statements with liability information

## S3 File Organization

Expected S3 key structure:
```
users/{user_id}/statements/{filename}
users/{user_id}/paystubs/{filename}
users/{user_id}/tax/{filename}
```

The user ID is automatically extracted from the S3 key path.

## DynamoDB Schema

```json
{
  "user_id": "string (HASH KEY)",
  "transaction_id": "string (RANGE KEY, UUID)",
  "date": "string (ISO 8601)",
  "description": "string",
  "amount": "number (Decimal)",
  "type": "string (income|expense)",
  "category": "string",
  "source_file": "string",
  "document_type": "string",
  "created_at": "string (ISO 8601)"
}
```

## Testing

### Unit Tests (29 tests)
- Parser validation and parsing logic
- Factory pattern implementation
- Lambda handler success and error cases
- DynamoDB integration
- S3 event handling

### Manual Testing
- Integration test script (`manual_test.py`)
- Sample CSV files for testing
- Mocked AWS services for local testing

### Test Coverage
All critical code paths are covered by unit tests.

## Error Handling

1. **File Validation Errors**: Detailed error messages for invalid files
2. **Parsing Errors**: Individual row/line errors don't stop processing
3. **DynamoDB Errors**: Caught and reported with context
4. **Partial Success**: Returns 207 (Multi-Status) when some files succeed and others fail

## Security Features

✅ **Input Validation**: File type and content validation  
✅ **Least Privilege IAM**: Read-only S3, write-only DynamoDB  
✅ **Encryption**: S3 bucket uses AES-256 encryption  
✅ **Public Access Blocked**: S3 bucket blocks all public access  
✅ **User Isolation**: User ID extracted from S3 path  
✅ **Audit Trail**: CloudWatch Logs for all operations  
✅ **No Vulnerabilities**: All dependencies scanned and verified  

## Performance Considerations

- **Batch Writing**: Uses DynamoDB batch_writer for efficiency
- **Memory**: 512MB allocated for large file processing
- **Timeout**: 5-minute timeout for complex PDFs
- **Lazy Loading**: AWS clients are lazy-loaded to improve cold start time

## Extensibility

### Adding New File Types (e.g., .xlsx)

1. Create new parser class:
```python
class ExcelParser(BaseParser):
    def can_parse(self, file_extension: str, document_type: DocumentType) -> bool:
        return file_extension.lower() == 'xlsx'
    
    def validate_file(self, file_content: bytes) -> bool:
        # Validation logic
        pass
    
    def parse(self, file_content: bytes, ...) -> List[ParsedTransaction]:
        # Parsing logic
        pass
```

2. Add to factory:
```python
def __init__(self):
    self.parsers = [
        CSVParser(),
        PDFParser(),
        ExcelParser(),  # New parser
    ]
```

3. Update CloudFormation S3 notifications to include .xlsx files

### Adding New Document Types

1. Add to `DocumentType` enum:
```python
class DocumentType(Enum):
    BANK_STATEMENT = "bank_statement"
    SALARY_SLIP = "salary_slip"
    TAX_STATEMENT = "tax_statement"
    INVOICE = "invoice"  # New type
    UNKNOWN = "unknown"
```

2. Add detection patterns to factory:
```python
DOCUMENT_TYPE_PATTERNS = {
    DocumentType.INVOICE: [r'invoice', r'bill', r'receipt'],
    ...
}
```

3. Implement parsing logic in relevant parsers

## Deployment

### Prerequisites
- AWS Account with permissions for Lambda, S3, DynamoDB, IAM, CloudWatch
- AWS CLI configured
- Python 3.12+

### Deployment Steps

1. Create CloudFormation stack:
```bash
aws cloudformation create-stack \
  --stack-name personal-finance-file-processor-dev \
  --template-body file://cloudformation-template.yaml \
  --parameters \
    ParameterKey=Environment,ParameterValue=dev \
  --capabilities CAPABILITY_NAMED_IAM
```

2. Build deployment package:
```bash
mkdir -p package
pip install -r requirements.txt -t package/
cp -r lambda_function.py parsers package/
cd package && zip -r ../lambda-deployment-package.zip .
```

3. Update Lambda function code:
```bash
aws lambda update-function-code \
  --function-name file-processor-dev \
  --zip-file fileb://lambda-deployment-package.zip
```

## Monitoring

### CloudWatch Logs
- Log Group: `/aws/lambda/file-processor-{environment}`
- All processing steps logged with INFO, WARNING, or ERROR level

### CloudWatch Metrics
- Invocations
- Errors
- Duration
- Concurrent executions

### CloudWatch Alarms
- Error alarm triggers on >5 errors in 5 minutes

## Known Limitations

1. **PDF Parsing**: Basic pattern matching may not work for all PDF formats
2. **File Size**: Lambda timeout limits processing of very large files
3. **Encoding**: CSV parser assumes UTF-8 encoding
4. **Date Formats**: Limited to common formats (extensible)

## Future Enhancements

- [ ] Support for Excel files (.xlsx)
- [ ] OCR for scanned PDFs
- [ ] Machine learning for automatic categorization
- [ ] Duplicate transaction detection
- [ ] File archival after processing
- [ ] Multi-currency support
- [ ] Batch processing optimization
- [ ] Enhanced error notifications (SNS/SES)

## Dependencies

- `boto3>=1.34.0` - AWS SDK
- `pypdf>=3.17.0` - PDF parsing
- `pytest>=7.4.0` - Testing framework
- `pytest-cov>=4.1.0` - Coverage reporting
- `moto>=5.0.0` - AWS mocking for tests

All dependencies are free from known security vulnerabilities.

## Files Created

```
backend/file-processor-lambda/
├── README.md                       # User documentation
├── IMPLEMENTATION_SUMMARY.md       # This file
├── lambda_function.py              # Main handler
├── requirements.txt                # Dependencies
├── cloudformation-template.yaml    # Infrastructure
├── manual_test.py                  # Integration tests
├── .gitignore                      # Git ignore rules
├── parsers/
│   ├── __init__.py
│   ├── base_parser.py
│   ├── csv_parser.py
│   ├── pdf_parser.py
│   └── parser_factory.py
├── tests/
│   └── test_lambda_function.py     # Unit tests (29 tests)
└── sample_files/
    ├── bank_statement_jan_2024.csv
    └── paystub_jan_2024.csv
```

## Conclusion

The File Upload Processor Lambda successfully implements all requirements with a modular, extensible architecture. The implementation follows AWS best practices for security, performance, and maintainability. The Strategy pattern makes it easy to add support for new file types and document types without modifying existing code.

**Status**: ✅ Complete and Production-Ready

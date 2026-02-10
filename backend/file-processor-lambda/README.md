# File Upload Processor Lambda

This Lambda function processes financial documents uploaded to S3, extracts transaction data, and writes it to DynamoDB.

## Overview

The File Upload Processor Lambda is triggered by S3 file upload events and performs the following operations:

1. **File Validation**: Validates file type and naming conventions
2. **Document Classification**: Automatically detects document type (Bank Statement, Salary Slip, Tax Statement, etc.)
3. **Parsing**: Extracts transaction records using modular parsers
4. **Storage**: Writes parsed transactions to DynamoDB Transactions table

## Supported File Types

Currently supports:
- **.csv** - Comma-separated values files
- **.pdf** - PDF documents

## Supported Document Types

- **Bank Statement** - Transaction history from bank accounts
- **Salary Slip** - Paycheck stubs and salary information
- **Tax Statement** - Tax returns and related documents
- **Unknown** - Generic financial documents

## Architecture

### Modular Parser Design

The implementation uses the **Strategy Pattern** for easy extensibility:

```
parsers/
├── __init__.py              # Package exports
├── base_parser.py           # Abstract base class
├── csv_parser.py            # CSV implementation
├── pdf_parser.py            # PDF implementation
└── parser_factory.py        # Factory for parser creation
```

#### Adding New File Types

To add support for a new file type (e.g., .xlsx):

1. Create a new parser class inheriting from `BaseParser`
2. Implement required methods: `can_parse()`, `validate_file()`, `parse()`
3. Add parser instance to `ParserFactory.__init__()`
4. Update CloudFormation S3 notification filters

#### Adding New Document Types

To add a new document type:

1. Add enum value to `DocumentType` in `base_parser.py`
2. Add detection patterns to `ParserFactory.DOCUMENT_TYPE_PATTERNS`
3. Implement parsing logic in relevant parser classes

## Project Structure

```
backend/file-processor-lambda/
├── lambda_function.py              # Main Lambda handler
├── parsers/                        # Modular parser package
│   ├── __init__.py
│   ├── base_parser.py              # Base classes and types
│   ├── csv_parser.py               # CSV parser implementation
│   ├── pdf_parser.py               # PDF parser implementation
│   └── parser_factory.py           # Factory pattern implementation
├── requirements.txt                # Python dependencies
├── cloudformation-template.yaml    # Infrastructure as Code
├── tests/
│   └── test_lambda_function.py    # Comprehensive unit tests
└── README.md                       # This file
```

## CSV File Format

Expected CSV format:

```csv
date,description,amount,type,category
2024-01-15,Grocery Store,50.00,expense,groceries
2024-01-20,Salary Deposit,2000.00,income,salary
```

### Required Columns
- `date` - Transaction date (YYYY-MM-DD, MM/DD/YYYY, or DD/MM/YYYY)
- `amount` - Transaction amount (positive or negative)

### Optional Columns
- `description` - Transaction description
- `type` - Transaction type ('income' or 'expense', inferred from amount if missing)
- `category` - Transaction category

### Amount Formats
- Basic: `100.00`
- With currency: `$100.00`
- With commas: `1,000.00`
- Negative (parentheses): `(100.00)`
- Negative (minus): `-100.00`

## PDF File Parsing

The PDF parser uses pattern matching to extract transactions from various PDF formats:

- **Bank Statements**: Extracts date, description, and amount from transaction lines
- **Salary Slips**: Identifies salary payments and earnings
- **Tax Statements**: Extracts tax payments and liabilities

**Note**: PDF parsing is more complex and may require customization for specific formats. The implementation provides a baseline that can be extended.

## S3 File Organization

Expected S3 key format:

```
users/{user_id}/statements/{filename}
users/{user_id}/paystubs/{filename}
users/{user_id}/tax/{filename}
```

The Lambda extracts the `user_id` from the S3 key path and associates all transactions with that user.

## DynamoDB Schema

Transactions are written to the DynamoDB table with the following structure:

```json
{
  "user_id": "user123",
  "transaction_id": "uuid-v4",
  "date": "2024-01-15",
  "description": "Grocery Store",
  "amount": 50.00,
  "type": "expense",
  "category": "groceries",
  "source_file": "bank_statement_jan_2024.csv",
  "document_type": "bank_statement",
  "created_at": "2024-01-15T10:30:00Z"
}
```

## Local Development

### Prerequisites

- Python 3.12+
- pip

### Setup

1. Install dependencies:
```bash
cd backend/file-processor-lambda
pip install -r requirements.txt
```

2. Run tests:
```bash
pytest tests/ -v
```

3. Run tests with coverage:
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```

### Local Testing

Create a test script to simulate S3 events:

```python
import json
from lambda_function import lambda_handler

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

response = lambda_handler(event, None)
print(json.dumps(response, indent=2))
```

## Deployment

### Using CloudFormation

The CloudFormation template creates all necessary resources:

- **S3 Bucket**: With encryption and event notifications
- **Lambda Function**: With appropriate IAM permissions
- **DynamoDB Table**: With GSI for date queries
- **CloudWatch Logs**: For monitoring and debugging
- **CloudWatch Alarms**: For error alerting

```bash
aws cloudformation create-stack \
  --stack-name personal-finance-file-processor-dev \
  --template-body file://cloudformation-template.yaml \
  --parameters \
    ParameterKey=Environment,ParameterValue=dev \
    ParameterKey=S3BucketName,ParameterValue=personal-finance-uploads \
    ParameterKey=DynamoDBTableName,ParameterValue=Transactions \
  --capabilities CAPABILITY_NAMED_IAM
```

### Deploying Lambda Code

1. Create deployment package:
```bash
cd backend/file-processor-lambda
mkdir -p package
pip install -r requirements.txt -t package/
cp -r lambda_function.py parsers package/
cd package
zip -r ../lambda-deployment-package.zip .
cd ..
```

2. Update Lambda function:
```bash
aws lambda update-function-code \
  --function-name file-processor-dev \
  --zip-file fileb://lambda-deployment-package.zip
```

### Using GitHub Actions

*(Coming soon - CI/CD workflow for automated deployment)*

## Configuration

### Environment Variables

The Lambda function uses these environment variables (configured in CloudFormation):

- `ENVIRONMENT` - Deployment environment (dev, staging, prod)
- `DYNAMODB_TABLE_NAME` - DynamoDB table name for transactions
- `LOG_LEVEL` - Logging level (INFO by default)

### Lambda Settings

- **Runtime**: Python 3.12
- **Memory**: 512 MB
- **Timeout**: 300 seconds (5 minutes)
- **Handler**: `lambda_function.lambda_handler`

## Monitoring

### CloudWatch Logs

Lambda logs are available at:
```
/aws/lambda/file-processor-{environment}
```

### Metrics

Key metrics to monitor:
- Invocations
- Errors
- Duration
- Concurrent executions

### Alarms

CloudFormation creates an alarm for:
- Lambda errors (>5 errors in 5 minutes)

## Error Handling

The Lambda function handles errors gracefully:

1. **File Validation Errors**: Logged with details about invalid files
2. **Parsing Errors**: Individual row/line errors don't stop processing
3. **DynamoDB Errors**: Caught and reported with context
4. **Partial Success**: Returns 207 (Multi-Status) when some files succeed and others fail

Example error response:
```json
{
  "statusCode": 207,
  "body": {
    "processed_files": 1,
    "failed_files": 1,
    "total_transactions": 5,
    "files": [
      {
        "file": "users/user123/good.csv",
        "transactions": 5,
        "status": "success"
      },
      {
        "file": "users/user123/bad.csv",
        "error": "Invalid CSV format",
        "status": "failed"
      }
    ]
  }
}
```

## Security Considerations

1. **S3 Bucket Security**:
   - Encryption at rest (AES-256)
   - Public access blocked
   - CORS configured for specific origins

2. **IAM Permissions**:
   - Least privilege access
   - Read-only access to S3
   - Write-only access to DynamoDB

3. **Input Validation**:
   - File type validation
   - File size limits (enforced by Lambda timeout)
   - Content validation before processing

4. **Data Protection**:
   - User ID extracted from S3 path (isolation)
   - Transaction IDs use UUID v4
   - CloudWatch Logs for audit trail

## Testing

### Unit Tests

Comprehensive test coverage includes:

- Parser validation and parsing logic
- Factory pattern implementation
- Lambda handler success and error cases
- DynamoDB integration
- S3 event handling

Run tests:
```bash
pytest tests/ -v
```

### Integration Testing

For end-to-end testing:

1. Upload a test CSV file to S3
2. Monitor CloudWatch Logs
3. Query DynamoDB for inserted transactions

## Future Enhancements

- [ ] Support for additional file types (.xlsx, .txt, .json)
- [ ] Machine learning for automatic categorization
- [ ] Advanced PDF parsing with OCR support
- [ ] Duplicate transaction detection
- [ ] File archival after processing
- [ ] S3 lifecycle policies for old files
- [ ] Enhanced error notifications (SNS/SES)
- [ ] Batch processing for large files
- [ ] Transaction validation rules
- [ ] Support for multi-currency

## Troubleshooting

### Common Issues

**Issue**: Lambda times out
- **Solution**: Increase memory allocation or timeout setting

**Issue**: Unable to extract user ID
- **Solution**: Ensure S3 key follows format: `users/{user_id}/...`

**Issue**: PDF parsing returns no transactions
- **Solution**: PDF format may not match expected patterns. Check logs for details.

**Issue**: CSV parsing fails
- **Solution**: Ensure CSV has required columns (date, amount)

## Support

For issues or questions:
1. Check CloudWatch Logs for detailed error messages
2. Review unit tests for expected formats
3. Open a GitHub issue with:
   - Error message
   - Sample file (redacted)
   - S3 event payload

## License

See main repository LICENSE file.

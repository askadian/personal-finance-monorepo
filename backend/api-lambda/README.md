# Personal Finance API Lambda

This directory contains the Python Lambda function that serves the Personal Finance REST API.

## Overview

The Lambda function implements all GET endpoints defined in the [OpenAPI specification](../../api/specs/openapi.yaml):

- `/transactions` - Get all transactions with filtering and pagination
- `/transactions/{id}` - Get a single transaction by ID
- `/income` - Get all income records with filtering
- `/income/summary` - Get income summary and aggregations
- `/expenses` - Get all expenses with filtering
- `/expenses/summary` - Get expenses summary and aggregations
- `/networth` - Get net worth calculation
- `/files` - Get list of uploaded files

## Project Structure

```
backend/api-lambda/
├── lambda_function.py              # Main Lambda handler
├── requirements.txt                # Python dependencies
├── cloudformation-template.yaml    # CloudFormation IaC template
├── tests/
│   └── test_lambda_function.py    # Unit tests
└── README.md                       # This file
```

## Local Development

### Prerequisites

- Python 3.12+
- pip

### Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run tests:
```bash
pytest tests/ -v
```

3. Run tests with coverage:
```bash
pytest tests/ -v --cov=lambda_function --cov-report=term-missing
```

### Testing Locally

You can test the Lambda function locally by creating a test event:

```python
import json
from lambda_function import lambda_handler

# Example test event
event = {
    'path': '/transactions',
    'httpMethod': 'GET',
    'headers': {'X-User-Id': 'test_user_123'},
    'queryStringParameters': {'limit': '10'}
}

response = lambda_handler(event, None)
print(json.dumps(response, indent=2))
```

## Deployment

### Using GitHub Actions (Recommended)

The Lambda function is automatically deployed via GitHub Actions when changes are pushed to the `main` branch.

**Workflow:** `.github/workflows/deploy-api-lambda.yml`

The workflow performs:
1. Runs unit tests
2. Validates CloudFormation template
3. Builds deployment package
4. Deploys to AWS (dev environment by default)

**Manual Deployment:**
You can trigger a manual deployment to different environments:
1. Go to Actions tab in GitHub
2. Select "Deploy Personal Finance API Lambda" workflow
3. Click "Run workflow"
4. Choose environment (dev, staging, or prod)

### Using AWS CLI

1. Create deployment package:
```bash
cd backend/api-lambda
mkdir -p package
pip install boto3 -t package/
cp lambda_function.py package/
cd package
zip -r ../lambda-deployment-package.zip .
cd ..
```

2. Deploy CloudFormation stack:
```bash
aws cloudformation create-stack \
  --stack-name personal-finance-api-dev \
  --template-body file://cloudformation-template.yaml \
  --parameters ParameterKey=Environment,ParameterValue=dev \
  --capabilities CAPABILITY_NAMED_IAM
```

3. Update Lambda function code:
```bash
aws lambda update-function-code \
  --function-name personal-finance-api-dev \
  --zip-file fileb://lambda-deployment-package.zip
```

## CloudFormation Resources

The CloudFormation template creates:

- **Lambda Function** - Python 3.12 runtime with 256MB memory
- **IAM Role** - Execution role with permissions for:
  - CloudWatch Logs
  - DynamoDB read access
  - S3 read access
- **API Gateway** - REST API with proxy integration
- **CloudWatch Log Groups** - For Lambda and API Gateway logs

## Configuration

### Environment Variables

The Lambda function uses these environment variables (set by CloudFormation):

- `ENVIRONMENT` - Deployment environment (dev, staging, prod)
- `DYNAMODB_TABLE_NAME` - Name of the DynamoDB table
- `LOG_LEVEL` - Logging level (INFO by default)

### Authentication

Currently, the API uses a fallback header (`X-User-Id`) for testing. In production:

1. Uncomment Cognito authorizer in CloudFormation template
2. Configure Cognito User Pool
3. Update Lambda to extract user from Cognito claims

## API Testing

### Using curl

```bash
# Get transactions
curl -X GET "https://<api-gateway-url>/dev/transactions?limit=10" \
  -H "X-User-Id: test_user"

# Get income summary
curl -X GET "https://<api-gateway-url>/dev/income/summary" \
  -H "X-User-Id: test_user"

# Get net worth
curl -X GET "https://<api-gateway-url>/dev/networth" \
  -H "X-User-Id: test_user"
```

### Using Postman/Bruno

Import the collections from the `api/collections/` directory for pre-configured requests.

## Monitoring

### CloudWatch Logs

- Lambda logs: `/aws/lambda/personal-finance-api-{environment}`
- API Gateway logs: `/aws/apigateway/personal-finance-api-{environment}`

### Metrics

The API Gateway stage has:
- Detailed CloudWatch metrics enabled
- Request/response logging enabled
- X-Ray tracing enabled

## Security Considerations

1. **Authentication**: Configure Cognito authorizer for production
2. **HTTPS Only**: API Gateway enforces HTTPS
3. **IAM Permissions**: Lambda has least-privilege access
4. **Input Validation**: All query parameters are validated
5. **CORS**: Configured for cross-origin requests

## Future Enhancements

- [ ] Connect to actual DynamoDB tables
- [ ] Implement Cognito authentication
- [ ] Add caching layer (ElastiCache/DAX)
- [ ] Implement request throttling
- [ ] Add comprehensive error logging
- [ ] Implement pagination tokens
- [ ] Add API versioning support

## Support

For issues or questions, please open a GitHub issue or contact the Personal Finance Team.

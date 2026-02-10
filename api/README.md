# Personal Finance API Documentation

This directory contains the OpenAPI specifications and API collections for the Personal Finance Tracker application.

## 📁 Directory Structure

```
api/
├── specs/
│   └── openapi.yaml                    # OpenAPI 3.0 specification
├── collections/
│   ├── postman/
│   │   ├── personal-finance-api.postman_collection.json
│   │   └── environments/
│   │       ├── mock.postman_environment.json
│   │       ├── staging.postman_environment.json
│   │       └── production.postman_environment.json
│   └── bruno/
│       ├── personal-finance-api/       # Bruno collection
│       │   ├── bruno.json
│       │   ├── Transactions/
│       │   ├── Income/
│       │   ├── Expenses/
│       │   ├── NetWorth/
│       │   └── Files/
│       └── environments/
│           ├── mock.bru
│           ├── staging.bru
│           └── production.bru
```

## 📖 OpenAPI Specification

The OpenAPI specification (`specs/openapi.yaml`) provides a complete API definition following the OpenAPI 3.0 standard.

### Features

- **Authentication**: AWS Cognito JWT Bearer token authentication
- **Endpoints**: Complete REST API for transactions, income, expenses, net worth, and file management
- **Data Models**: Fully documented request/response schemas
- **Examples**: Mock data examples for all endpoints
- **Error Handling**: Standardized error responses

### Using the OpenAPI Spec

#### View in Swagger Editor
1. Go to [Swagger Editor](https://editor.swagger.io/)
2. Import the `specs/openapi.yaml` file
3. View and interact with the API documentation

#### Generate API Documentation
```bash
# Using Redoc
npx @redocly/cli build-docs specs/openapi.yaml -o api-docs.html

# Using Swagger UI
npx swagger-ui-watcher specs/openapi.yaml
```

#### Generate Mock Server
```bash
# Using Prism
npx @stoplight/prism-cli mock specs/openapi.yaml
```

## 🚀 Postman Collection

The Postman collection provides a complete set of API requests with mock responses and parameterized environments.

### Importing the Collection

1. Open Postman
2. Click **Import** button
3. Select `collections/postman/personal-finance-api.postman_collection.json`
4. Import all environment files from `collections/postman/environments/`

### Available Environments

- **Mock Environment**: For testing with mock data (no real backend required)
- **Staging Environment**: For staging environment testing
- **Production Environment**: For production use

### Setting Up Authentication

1. Select an environment (Mock, Staging, or Production)
2. For Staging/Production:
   - Obtain a JWT token from AWS Cognito
   - Set the `access_token` variable in the environment
3. For Mock:
   - The mock token is already set

### Using the Collection

Each request is organized into folders:
- **Transactions**: Fetch and view transaction data
- **Income**: Manage income records and summaries
- **Expenses**: Track expenses and view analytics
- **Net Worth**: View net worth calculations and history
- **Files**: Upload and manage financial documents

#### Parameterized Requests

All requests use environment variables for easy switching between environments:

- `{{base_url}}`: API base URL
- `{{api_version}}`: API version (v1)
- `{{access_token}}`: JWT authentication token
- `{{start_date}}`: Default start date for queries
- `{{end_date}}`: Default end date for queries
- `{{limit}}`: Default pagination limit
- `{{transaction_id}}`: Sample transaction ID

### Running Tests

The collection includes automated tests that verify:
- Response status codes
- Response structure
- Data types
- Response times

Run the entire collection using Postman's Collection Runner or Newman:

```bash
# Install Newman
npm install -g newman

# Run collection with mock environment
newman run collections/postman/personal-finance-api.postman_collection.json \
  -e collections/postman/environments/mock.postman_environment.json
```

## 🐻 Bruno Collection

Bruno is a fast, git-friendly open-source API client. The Bruno collection is organized as a directory structure for better version control.

### Setting Up Bruno

1. Download and install [Bruno](https://www.usebruno.com/)
2. Open Bruno
3. Click **Open Collection**
4. Select the `collections/bruno/personal-finance-api` directory

### Available Environments

- **mock**: For testing with mock data
- **staging**: For staging environment testing
- **production**: For production use

### Using the Collection

The collection is organized into folders matching the API structure:

- **Transactions**: Transaction queries and details
- **Income**: Income tracking and summaries
- **Expenses**: Expense management and analytics
- **NetWorth**: Net worth calculations
- **Files**: File upload operations

#### Switching Environments

1. In Bruno, click on the environment dropdown (top right)
2. Select the desired environment (mock, staging, or production)
3. Modify environment variables as needed

#### Environment Variables

Each environment includes:
- `base_url`: API endpoint URL
- `api_version`: API version
- `access_token`: Authentication token
- `start_date`: Query start date
- `end_date`: Query end date
- `limit`: Pagination limit
- `transaction_id`: Sample transaction ID

For staging/production environments, also includes:
- `cognito_user_pool_id`: AWS Cognito User Pool ID
- `cognito_client_id`: AWS Cognito Client ID

### Running Tests

Each request includes built-in tests that verify response structure and data types. Tests run automatically when you send a request.

## 🎯 API Endpoints

### Transactions
- `GET /v1/transactions` - Get all transactions with optional filtering
- `GET /v1/transactions/{transactionId}` - Get a specific transaction

### Income
- `GET /v1/income` - Get all income records
- `GET /v1/income/summary` - Get income summary with aggregated statistics

### Expenses
- `GET /v1/expenses` - Get all expense records
- `GET /v1/expenses/summary` - Get expense summary with category breakdown

### Net Worth
- `GET /v1/networth` - Get current net worth and historical data

### Files
- `POST /v1/files/upload-url` - Request presigned URL for file upload
- `GET /v1/files` - Get list of uploaded files

## 🔐 Authentication

All endpoints require authentication using AWS Cognito JWT tokens.

### For Testing (Mock Environment)

Use the pre-configured mock token in the mock environment.

### For Staging/Production

1. Authenticate with AWS Cognito to obtain a JWT token
2. Set the token in your environment's `access_token` variable
3. The token will be automatically included in all requests as a Bearer token

#### Example: Getting Cognito Token

```bash
# Using AWS CLI
aws cognito-idp initiate-auth \
  --auth-flow USER_PASSWORD_AUTH \
  --client-id YOUR_CLIENT_ID \
  --auth-parameters USERNAME=user@example.com,PASSWORD=your_password
```

## 📊 Mock Data

All collections include comprehensive mock data examples that match the production API structure:

### Sample Transaction
```json
{
  "id": "txn_001",
  "userId": "user_123",
  "date": "2024-01-15",
  "amount": -45.67,
  "description": "Grocery Store Purchase",
  "category": "groceries",
  "merchant": "Whole Foods",
  "type": "debit",
  "accountId": "acc_001",
  "createdAt": "2024-01-16T10:30:00Z",
  "updatedAt": "2024-01-16T10:30:00Z"
}
```

### Sample Income Record
```json
{
  "id": "inc_001",
  "userId": "user_123",
  "date": "2024-01-31",
  "amount": 5000.00,
  "description": "Monthly Salary",
  "source": "salary",
  "employer": "Tech Corp",
  "taxWithheld": 1200.00,
  "createdAt": "2024-02-01T00:00:00Z",
  "updatedAt": "2024-02-01T00:00:00Z"
}
```

## 🛠️ Development Workflow

### 1. Design Phase
Use the OpenAPI specification to design and review API changes before implementation.

### 2. Mock Testing
Use Postman or Bruno with the mock environment to test API interactions without a backend.

### 3. Integration Testing
Switch to the staging environment to test with the actual staging backend.

### 4. Production
Use the production environment for live API access.

## 📝 Updating the Collections

When the API changes:

1. Update the OpenAPI specification (`specs/openapi.yaml`)
2. Update Postman collection requests and examples
3. Update Bruno collection request files
4. Update environment variables if needed
5. Commit all changes to version control

## 🔄 Version Control

All collections are designed to be version-controlled:

- **Postman**: JSON files that can be committed to Git
- **Bruno**: Directory structure optimized for Git with individual .bru files
- **OpenAPI**: YAML file for easy diffs and collaboration

## 📚 Additional Resources

- [OpenAPI Specification](https://spec.openapis.org/oas/v3.0.3)
- [Postman Documentation](https://learning.postman.com/docs/)
- [Bruno Documentation](https://docs.usebruno.com/)
- [AWS Cognito Authentication](https://docs.aws.amazon.com/cognito/)

## 🤝 Contributing

When adding new endpoints:

1. Update the OpenAPI spec first
2. Generate mock examples
3. Add requests to both Postman and Bruno collections
4. Include appropriate tests
5. Update this README if needed

## 📞 Support

For issues or questions about the API:
- Check the OpenAPI specification for detailed endpoint documentation
- Review mock examples in the collections
- Refer to the main project README for architecture details

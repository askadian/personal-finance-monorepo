# API Quick Reference

## Base URLs

- **Production**: `https://api.personal-finance.example.com/v1`
- **Staging**: `https://api-staging.personal-finance.example.com/v1`
- **Mock**: `https://mock-api.personal-finance.example.com/v1`

## Authentication

All endpoints require AWS Cognito JWT Bearer token:
```
Authorization: Bearer <your_jwt_token>
```

## Endpoints Overview

### 📊 Transactions

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/transactions` | Get all transactions with filtering |
| GET | `/transactions/{id}` | Get specific transaction |

**Query Parameters:**
- `startDate` (date): Filter from date (YYYY-MM-DD)
- `endDate` (date): Filter to date (YYYY-MM-DD)
- `category` (string): Filter by category
- `limit` (integer): Max results (1-100, default: 50)
- `offset` (integer): Skip results (default: 0)

### 💰 Income

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/income` | Get all income records |
| GET | `/income/summary` | Get income summary statistics |

**Query Parameters:**
- `startDate` (date): Filter from date
- `endDate` (date): Filter to date
- `source` (string): Filter by source (salary, bonus, investment, freelance, other)
- `limit` (integer): Max results (1-100, default: 50)
- `period` (string): Summary period (month, quarter, year, all)

### 💸 Expenses

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/expenses` | Get all expense records |
| GET | `/expenses/summary` | Get expense summary statistics |

**Query Parameters:**
- `startDate` (date): Filter from date
- `endDate` (date): Filter to date
- `category` (string): Filter by category
- `limit` (integer): Max results (1-100, default: 50)
- `period` (string): Summary period (month, quarter, year, all)

### 📈 Net Worth

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/networth` | Get net worth data and history |

**Query Parameters:**
- `startDate` (date): History start date
- `endDate` (date): History end date

### 📁 Files

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/files/upload-url` | Request presigned S3 upload URL |
| GET | `/files` | Get uploaded files list |

**Query Parameters (GET):**
- `fileType` (string): Filter by type
- `status` (string): Filter by status (uploaded, processing, processed, failed)

**Request Body (POST):**
```json
{
  "fileName": "statement.pdf",
  "fileType": "bank_statement",
  "contentType": "application/pdf"
}
```

## Common Response Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 401 | Unauthorized - Invalid or missing token |
| 400 | Bad Request - Invalid parameters |
| 404 | Not Found - Resource doesn't exist |
| 500 | Internal Server Error |

## Example Requests

### Get Transactions
```bash
curl -X GET \
  "https://api.personal-finance.example.com/v1/transactions?startDate=2024-01-01&limit=10" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Accept: application/json"
```

### Get Income Summary
```bash
curl -X GET \
  "https://api.personal-finance.example.com/v1/income/summary?period=year" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Accept: application/json"
```

### Request Upload URL
```bash
curl -X POST \
  "https://api.personal-finance.example.com/v1/files/upload-url" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "fileName": "bank_statement_jan_2024.pdf",
    "fileType": "bank_statement",
    "contentType": "application/pdf"
  }'
```

## Data Types

### Transaction Categories
- groceries
- utilities
- entertainment
- healthcare
- transportation
- dining
- shopping
- other

### Income Sources
- salary
- bonus
- investment
- freelance
- other

### File Types
- bank_statement
- pay_stub
- 1099-int
- 1099-div
- w-2
- credit_card_statement
- investment_statement
- other

### File Status
- uploaded
- processing
- processed
- failed

## Using with Collections

### Postman
1. Import `api/collections/postman/personal-finance-api.postman_collection.json`
2. Import environment from `api/collections/postman/environments/`
3. Set `access_token` variable
4. Start making requests

### Bruno
1. Open `api/collections/bruno/personal-finance-api` folder in Bruno
2. Select environment (mock, staging, or production)
3. Set `access_token` in environment
4. Start making requests

## Need Help?

- Full documentation: [API README](./README.md)
- OpenAPI spec: [specs/openapi.yaml](./specs/openapi.yaml)
- Issues: [GitHub Issues](https://github.com/askadian/personal-finance-monorepo/issues)

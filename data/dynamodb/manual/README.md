# DynamoDB Manual Setup Guide

This guide provides step-by-step instructions to manually create and seed the DynamoDB table for the Personal Finance application.

## Table Overview

**Table Name:** `Transactions`

**Purpose:** Store parsed transaction records from uploaded financial statements in a time-series format.

## Table Schema

### Primary Key Structure
- **Partition Key (HASH):** `user_id` (String)
- **Sort Key (RANGE):** `transaction_id` (String, UUID format)

### Attributes
| Attribute | Type | Description | Example |
|-----------|------|-------------|---------|
| user_id | String | User identifier (Partition Key) | `user-123e4567-e89b-12d3` |
| transaction_id | String | Unique transaction identifier (Sort Key) | `txn-a456f891-e23c-45d6` |
| date | String | Transaction date in ISO 8601 format | `2024-01-15T10:30:00Z` |
| description | String | Transaction description | `Amazon.com purchase` |
| amount | Number | Transaction amount (Decimal) | `99.99` |
| type | String | Transaction type | `income` or `expense` |
| category | String | Transaction category | `shopping`, `salary`, `utilities` |
| source_file | String | Source file name | `statement_jan_2024.pdf` |
| document_type | String | Document type | `bank_statement`, `pay_stub`, `tax_document` |
| created_at | String | Record creation timestamp in ISO 8601 | `2024-01-15T11:00:00Z` |

## Step-by-Step Setup Instructions

### Step 1: Access AWS Console

1. Log in to your [AWS Management Console](https://console.aws.amazon.com/)
2. Navigate to the **DynamoDB** service
   - You can search for "DynamoDB" in the AWS search bar
   - Or find it under "Database" category in the services menu

### Step 2: Create the Table

1. Click on **"Create table"** button
2. Configure the table settings:

   **Table Details:**
   - **Table name:** `Transactions`
   
   **Partition key:**
   - **Partition key:** `user_id`
   - **Type:** String
   
   **Sort key:**
   - ☑️ Check "Add sort key"
   - **Sort key:** `transaction_id`
   - **Type:** String

3. **Table settings:**
   - Select **"Customize settings"** for more control

4. **Read/write capacity settings:**
   - Choose one of the following based on your needs:
     - **On-demand** (Recommended for development/testing)
       - Pay per request
       - Automatically scales
     - **Provisioned** (For predictable workloads)
       - Read capacity: 5 units (adjust as needed)
       - Write capacity: 5 units (adjust as needed)
       - ☑️ Enable "Auto scaling" (recommended)

5. **Encryption settings:**
   - Select **"Owned by Amazon DynamoDB"** (default, no additional cost)
   - Or choose **"AWS managed key"** for enhanced security

6. **Tags (Optional):**
   - Add tags for cost tracking and organization:
     - Key: `Project`, Value: `PersonalFinance`
     - Key: `Environment`, Value: `Development`

7. Click **"Create table"**
   - Wait for the table status to change from "Creating" to "Active" (typically 1-2 minutes)

### Step 3: Verify Table Creation

1. In the DynamoDB console, select your `Transactions` table
2. Click on the **"Overview"** tab
3. Verify the following:
   - Table status is "Active"
   - Partition key: `user_id` (String)
   - Sort key: `transaction_id` (String)

### Step 4: Seed Sample Data

#### Option A: Using AWS Console

1. In your `Transactions` table, click on **"Explore table items"** or **"Items"** tab
2. Click **"Create item"**
3. Add the following sample items:

**Sample Item 1: Grocery Expense**
```json
{
  "user_id": "user-550e8400-e29b-41d4-a716-446655440000",
  "transaction_id": "txn-660e8400-e29b-41d4-a716-446655440001",
  "date": "2024-01-15T10:30:00Z",
  "description": "Whole Foods Market",
  "amount": 125.50,
  "type": "expense",
  "category": "groceries",
  "source_file": "bank_statement_jan_2024.csv",
  "document_type": "bank_statement",
  "created_at": "2024-01-15T11:00:00Z"
}
```

**Sample Item 2: Salary Income**
```json
{
  "user_id": "user-550e8400-e29b-41d4-a716-446655440000",
  "transaction_id": "txn-770e8400-e29b-41d4-a716-446655440002",
  "date": "2024-01-01T00:00:00Z",
  "description": "Monthly Salary - January",
  "amount": 5000.00,
  "type": "income",
  "category": "salary",
  "source_file": "paystub_jan_2024.pdf",
  "document_type": "pay_stub",
  "created_at": "2024-01-02T08:00:00Z"
}
```

**Sample Item 3: Utility Bill**
```json
{
  "user_id": "user-550e8400-e29b-41d4-a716-446655440000",
  "transaction_id": "txn-880e8400-e29b-41d4-a716-446655440003",
  "date": "2024-01-20T14:00:00Z",
  "description": "Electric Company - January Bill",
  "amount": 89.75,
  "type": "expense",
  "category": "utilities",
  "source_file": "utility_bill_jan_2024.pdf",
  "document_type": "bank_statement",
  "created_at": "2024-01-20T15:30:00Z"
}
```

**Sample Item 4: Online Shopping**
```json
{
  "user_id": "user-550e8400-e29b-41d4-a716-446655440000",
  "transaction_id": "txn-990e8400-e29b-41d4-a716-446655440004",
  "date": "2024-01-18T16:45:00Z",
  "description": "Amazon.com - Home Office Supplies",
  "amount": 234.99,
  "type": "expense",
  "category": "shopping",
  "source_file": "credit_card_statement_jan_2024.csv",
  "document_type": "bank_statement",
  "created_at": "2024-01-19T09:00:00Z"
}
```

**Sample Item 5: Restaurant Expense**
```json
{
  "user_id": "user-550e8400-e29b-41d4-a716-446655440000",
  "transaction_id": "txn-aa0e8400-e29b-41d4-a716-446655440005",
  "date": "2024-01-22T19:30:00Z",
  "description": "Italian Restaurant Downtown",
  "amount": 67.50,
  "type": "expense",
  "category": "dining",
  "source_file": "credit_card_statement_jan_2024.csv",
  "document_type": "bank_statement",
  "created_at": "2024-01-23T10:00:00Z"
}
```

#### Option B: Using AWS CLI

If you prefer using the command line, you can use the AWS CLI:

1. Ensure AWS CLI is installed and configured:
   ```bash
   aws configure
   ```

2. Create sample items using the AWS CLI:

```bash
# Sample Item 1: Grocery Expense
aws dynamodb put-item \
    --table-name Transactions \
    --item '{
        "user_id": {"S": "user-550e8400-e29b-41d4-a716-446655440000"},
        "transaction_id": {"S": "txn-660e8400-e29b-41d4-a716-446655440001"},
        "date": {"S": "2024-01-15T10:30:00Z"},
        "description": {"S": "Whole Foods Market"},
        "amount": {"N": "125.50"},
        "type": {"S": "expense"},
        "category": {"S": "groceries"},
        "source_file": {"S": "bank_statement_jan_2024.csv"},
        "document_type": {"S": "bank_statement"},
        "created_at": {"S": "2024-01-15T11:00:00Z"}
    }'

# Sample Item 2: Salary Income
aws dynamodb put-item \
    --table-name Transactions \
    --item '{
        "user_id": {"S": "user-550e8400-e29b-41d4-a716-446655440000"},
        "transaction_id": {"S": "txn-770e8400-e29b-41d4-a716-446655440002"},
        "date": {"S": "2024-01-01T00:00:00Z"},
        "description": {"S": "Monthly Salary - January"},
        "amount": {"N": "5000.00"},
        "type": {"S": "income"},
        "category": {"S": "salary"},
        "source_file": {"S": "paystub_jan_2024.pdf"},
        "document_type": {"S": "pay_stub"},
        "created_at": {"S": "2024-01-02T08:00:00Z"}
    }'

# Sample Item 3: Utility Bill
aws dynamodb put-item \
    --table-name Transactions \
    --item '{
        "user_id": {"S": "user-550e8400-e29b-41d4-a716-446655440000"},
        "transaction_id": {"S": "txn-880e8400-e29b-41d4-a716-446655440003"},
        "date": {"S": "2024-01-20T14:00:00Z"},
        "description": {"S": "Electric Company - January Bill"},
        "amount": {"N": "89.75"},
        "type": {"S": "expense"},
        "category": {"S": "utilities"},
        "source_file": {"S": "utility_bill_jan_2024.pdf"},
        "document_type": {"S": "bank_statement"},
        "created_at": {"S": "2024-01-20T15:30:00Z"}
    }'

# Sample Item 4: Online Shopping
aws dynamodb put-item \
    --table-name Transactions \
    --item '{
        "user_id": {"S": "user-550e8400-e29b-41d4-a716-446655440000"},
        "transaction_id": {"S": "txn-990e8400-e29b-41d4-a716-446655440004"},
        "date": {"S": "2024-01-18T16:45:00Z"},
        "description": {"S": "Amazon.com - Home Office Supplies"},
        "amount": {"N": "234.99"},
        "type": {"S": "expense"},
        "category": {"S": "shopping"},
        "source_file": {"S": "credit_card_statement_jan_2024.csv"},
        "document_type": {"S": "bank_statement"},
        "created_at": {"S": "2024-01-19T09:00:00Z"}
    }'

# Sample Item 5: Restaurant Expense
aws dynamodb put-item \
    --table-name Transactions \
    --item '{
        "user_id": {"S": "user-550e8400-e29b-41d4-a716-446655440000"},
        "transaction_id": {"S": "txn-aa0e8400-e29b-41d4-a716-446655440005"},
        "date": {"S": "2024-01-22T19:30:00Z"},
        "description": {"S": "Italian Restaurant Downtown"},
        "amount": {"N": "67.50"},
        "type": {"S": "expense"},
        "category": {"S": "dining"},
        "source_file": {"S": "credit_card_statement_jan_2024.csv"},
        "document_type": {"S": "bank_statement"},
        "created_at": {"S": "2024-01-23T10:00:00Z"}
    }'
```

### Step 5: Query and Verify Sample Data

#### Using AWS Console:
1. Go to the **"Explore table items"** tab
2. You should see 5 items for user `user-550e8400-e29b-41d4-a716-446655440000`
3. Click on any item to view its details

#### Using AWS CLI:
```bash
# Query all transactions for a specific user
aws dynamodb query \
    --table-name Transactions \
    --key-condition-expression "user_id = :uid" \
    --expression-attribute-values '{":uid":{"S":"user-550e8400-e29b-41d4-a716-446655440000"}}'
```

### Step 6: Test Common Query Patterns

#### Get a specific transaction:
```bash
aws dynamodb get-item \
    --table-name Transactions \
    --key '{
        "user_id": {"S": "user-550e8400-e29b-41d4-a716-446655440000"},
        "transaction_id": {"S": "txn-660e8400-e29b-41d4-a716-446655440001"}
    }'
```

#### Get all transactions for a user (with pagination):
```bash
aws dynamodb query \
    --table-name Transactions \
    --key-condition-expression "user_id = :uid" \
    --expression-attribute-values '{":uid":{"S":"user-550e8400-e29b-41d4-a716-446655440000"}}' \
    --limit 10
```

## Common Categories for Reference

Here are common transaction categories you can use:

### Income Categories:
- `salary`
- `bonus`
- `investment_income`
- `freelance`
- `other_income`

### Expense Categories:
- `groceries`
- `dining`
- `utilities`
- `rent`
- `transportation`
- `healthcare`
- `shopping`
- `entertainment`
- `insurance`
- `subscriptions`
- `education`
- `travel`

## Cleanup (Optional)

To delete the table and all its data:

### Using AWS Console:
1. Select the `Transactions` table
2. Click **"Delete"**
3. Type `delete` to confirm
4. Click **"Delete table"**

### Using AWS CLI:
```bash
aws dynamodb delete-table --table-name Transactions
```

## Next Steps

- For automated table creation using GitHub Actions, see the `/data/dynamodb/auto` folder
- For infrastructure as code deployment using AWS CDK, see the `/infra` directory
- Refer to the main [DEPLOYMENT.md](../../../DEPLOYMENT.md) for end-to-end deployment instructions

## Troubleshooting

### Issue: Table creation fails
- **Solution:** Check your AWS permissions. You need `dynamodb:CreateTable` permission.

### Issue: Cannot add items
- **Solution:** Verify table is in "Active" state and you have `dynamodb:PutItem` permission.

### Issue: Items not appearing
- **Solution:** Check you're using the correct partition key and sort key values. Keys are case-sensitive.

### Issue: Unexpected costs
- **Solution:** For development, use "On-demand" billing mode. Delete the table when not in use.

## Additional Resources

- [AWS DynamoDB Documentation](https://docs.aws.amazon.com/dynamodb/)
- [DynamoDB Best Practices](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices.html)
- [AWS CLI DynamoDB Reference](https://docs.aws.amazon.com/cli/latest/reference/dynamodb/)

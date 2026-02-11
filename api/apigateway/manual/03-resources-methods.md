# Resources and Methods Setup

This guide walks through creating API resources (paths) and HTTP methods for the Personal Finance API.

## 📋 Overview

In this step, you will:
1. Create resource hierarchy matching the OpenAPI spec
2. Add HTTP methods to resources
3. Configure method request parameters
4. Set up request validation

**Estimated Time**: 20-30 minutes

## 🏗️ API Structure to Build

Based on the OpenAPI specification, we'll create this structure:

```
/ (root)
└── v1
    ├── transactions
    │   ├── GET
    │   ├── OPTIONS (for CORS)
    │   └── {transactionId}
    │       ├── GET
    │       └── OPTIONS
    ├── income
    │   ├── GET
    │   ├── OPTIONS
    │   └── summary
    │       ├── GET
    │       └── OPTIONS
    ├── expenses
    │   ├── GET
    │   ├── OPTIONS
    │   └── summary
    │       ├── GET
    │       └── OPTIONS
    ├── networth
    │   ├── GET
    │   └── OPTIONS
    └── files
        ├── GET
        ├── OPTIONS
        └── upload-url
            ├── POST
            └── OPTIONS
```

## 🚀 Step-by-Step Instructions

### Step 1: Create Version Resource (v1)

1. **Select Root Resource**
   - In Resources, click on `/` (root resource)

2. **Create Resource**
   - Click **Actions** dropdown → **Create Resource**

3. **Configure Resource**:
   - **Resource Name**: `v1`
   - **Resource Path**: `v1` (should auto-populate)
   - **Enable API Gateway CORS**: Leave **unchecked** (we'll configure manually)
   
4. **Click "Create Resource"**

### Step 2: Create Transactions Resource

1. **Select v1 Resource**
   - Click on `/v1` in the resources tree

2. **Create Resource**
   - Click **Actions** → **Create Resource**

3. **Configure**:
   - **Resource Name**: `transactions`
   - **Resource Path**: `transactions`
   
4. **Click "Create Resource"**

You should now have: `/v1/transactions`

### Step 3: Add GET Method to Transactions

1. **Select /v1/transactions**
   - Click on the `transactions` resource

2. **Create Method**
   - Click **Actions** → **Create Method**
   - Select **GET** from dropdown
   - Click the checkmark ✓

3. **Setup Method**:
   - **Integration type**: We'll configure this in the next guide
   - For now, select **Mock** (temporary)
   - Click **Save**

> **Note**: We're using Mock temporarily. We'll change this to Lambda Proxy Integration in the next guide.

### Step 4: Add Path Parameter Resource

Create resource for individual transaction by ID:

1. **Select /v1/transactions**

2. **Create Resource**
   - Click **Actions** → **Create Resource**

3. **Configure**:
   - **Resource Name**: `transactionId`
   - **Resource Path**: `{transactionId}`
   
   > **Important**: Include the curly braces `{}` to make it a path parameter

4. **Click "Create Resource"**

5. **Add GET Method**
   - Select `/v1/transactions/{transactionId}`
   - Click **Actions** → **Create Method**
   - Select **GET**
   - Click checkmark, then **Save** (use Mock integration for now)

### Step 5: Create Income Resources

1. **Select /v1**

2. **Create Resource**:
   - Resource Name: `income`
   - Resource Path: `income`
   - Create Resource

3. **Add GET Method to /v1/income**
   - Select income resource
   - Actions → Create Method → GET
   - Use Mock integration, Save

4. **Create Summary Sub-resource**:
   - Select `/v1/income`
   - Actions → Create Resource
   - Resource Name: `summary`
   - Resource Path: `summary`
   - Create Resource

5. **Add GET Method to /v1/income/summary**
   - Select summary resource
   - Actions → Create Method → GET
   - Use Mock integration, Save

### Step 6: Create Expenses Resources

Follow the same pattern as Income:

1. **Create /v1/expenses**
   - Select /v1
   - Actions → Create Resource
   - Name: `expenses`, Path: `expenses`

2. **Add GET Method to /v1/expenses**

3. **Create /v1/expenses/summary**
   - Select /v1/expenses
   - Actions → Create Resource
   - Name: `summary`, Path: `summary`

4. **Add GET Method to /v1/expenses/summary**

### Step 7: Create Net Worth Resource

1. **Create /v1/networth**
   - Select /v1
   - Actions → Create Resource
   - Name: `networth`, Path: `networth`

2. **Add GET Method to /v1/networth**

### Step 8: Create Files Resources

1. **Create /v1/files**
   - Select /v1
   - Actions → Create Resource
   - Name: `files`, Path: `files`

2. **Add GET Method to /v1/files**

3. **Create /v1/files/upload-url**
   - Select /v1/files
   - Actions → Create Resource
   - Name: `upload-url`, Path: `upload-url`

4. **Add POST Method to /v1/files/upload-url**
   - Actions → Create Method → **POST**
   - Use Mock integration, Save

## 📝 Configure Query Parameters (Optional)

For resources that accept query parameters (like transactions with filters):

### Example: Transactions Filters

1. **Select GET method on /v1/transactions**

2. **Click on "Method Request"**

3. **Expand "URL Query String Parameters"**

4. **Add Query String Parameters**:
   - Click **Add query string**
   - Name: `startDate`, Required: No
   - Click **Add query string**
   - Name: `endDate`, Required: No
   - Name: `category`, Required: No
   - Name: `limit`, Required: No
   - Name: `offset`, Required: No

5. **Click checkmark after each**

> **Note**: Query parameters are validated but not enforced at the API Gateway level. Validation happens in Lambda.

## 🔍 Verify Resource Structure

Your Resources tree should now look like:

```
/
└── v1
    ├── transactions
    │   ├── GET
    │   └── {transactionId}
    │       └── GET
    ├── income
    │   ├── GET
    │   └── summary
    │       └── GET
    ├── expenses
    │   ├── GET
    │   └── summary
    │       └── GET
    ├── networth
    │   └── GET
    └── files
        ├── GET
        └── upload-url
            └── POST
```

## 📋 Checklist

Verify all resources and methods are created:

- [ ] `/v1` resource created
- [ ] `/v1/transactions` with GET method
- [ ] `/v1/transactions/{transactionId}` with GET method
- [ ] `/v1/income` with GET method
- [ ] `/v1/income/summary` with GET method
- [ ] `/v1/expenses` with GET method
- [ ] `/v1/expenses/summary` with GET method
- [ ] `/v1/networth` with GET method
- [ ] `/v1/files` with GET method
- [ ] `/v1/files/upload-url` with POST method

## 💡 Understanding Path Parameters

### What are Path Parameters?

Path parameters are variable parts of the URL:
- Example: `/v1/transactions/{transactionId}`
- `{transactionId}` is replaced with actual ID: `/v1/transactions/txn_001`

### How They Work

1. **In API Gateway**: Define with `{paramName}` syntax
2. **In Lambda**: Received in `event.pathParameters.paramName`
3. **In Request**: `/v1/transactions/txn_001` → `transactionId = "txn_001"`

## 🚨 Troubleshooting

### Cannot Create Resource
**Problem**: Create Resource button is grayed out
**Solution**: 
- Make sure you've selected a parent resource
- Refresh the page if issue persists

### Path Parameter Not Working
**Problem**: Path parameter like `{transactionId}` shows as literal text
**Solution**: 
- Ensure you included curly braces: `{paramName}`
- Resource Path must match Resource Name with braces

### Method Already Exists Error
**Problem**: "Method already exists" when creating method
**Solution**:
- Check if method already exists on that resource
- Delete existing method if needed (Actions → Delete Method)

### Cannot See New Resources
**Problem**: Resources don't appear in tree
**Solution**:
- Click "Resources" in left sidebar to refresh
- Expand parent resources to see children

## 📚 Best Practices

1. **Consistent Naming**: Use lowercase, hyphen-separated names
   - ✅ `upload-url`
   - ❌ `uploadUrl` or `upload_url`

2. **Path Parameters**: Use descriptive names
   - ✅ `{transactionId}`
   - ❌ `{id}` or `{x}`

3. **Resource Hierarchy**: Keep it logical and shallow
   - ✅ `/v1/income/summary`
   - ❌ `/v1/data/income/records/summary`

4. **Versioning**: Always use version prefix (`/v1`)
   - Allows API evolution without breaking changes

## 📖 Additional Resources

- [API Gateway Resources](https://docs.aws.amazon.com/apigateway/latest/developerguide/how-to-create-api.html)
- [Path Parameters](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-method-settings-method-request.html)
- [REST API Best Practices](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-method-settings-method-request.html)

## ✅ Completion

You've successfully created all API resources and methods!

**What's Next**: In the next step, you'll connect these endpoints to Lambda functions using Lambda Proxy Integration.

---

**Next Step**: [Lambda Integration](./04-lambda-integration.md) →

**Previous Step**: [← REST API Setup](./02-rest-api-setup.md)

**Back to**: [Manual Setup Guide](./README.md)

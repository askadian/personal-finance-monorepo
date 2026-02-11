# REST API Setup

This guide walks through creating a new REST API in AWS API Gateway.

## 📋 Overview

In this step, you will:
1. Create a new REST API
2. Configure basic API settings
3. Understand API Gateway structure
4. Set up API documentation

**Estimated Time**: 10-15 minutes

## 🚀 Step-by-Step Instructions

### Step 1: Navigate to API Gateway Console

1. **Open AWS Management Console**
   - Go to: https://console.aws.amazon.com/apigateway/

2. **Select Your Region**
   - Ensure you're in the same region as your Lambda functions
   - Recommended: `us-east-1` (N. Virginia)

3. **View API Gateway Dashboard**
   - You should see the API Gateway home screen

### Step 2: Create REST API

1. **Click "Create API"**
   - Or if you already have APIs, click "Create API" button

2. **Choose API Type**
   - Select **"REST API"** (not REST API Private or HTTP API)
   - Under REST API, click **"Build"**
   
   > **Note**: We're using REST API (not HTTP API) because it provides:
   > - Full feature set for authorizers
   > - Request/response validation
   > - API keys and usage plans
   > - More control over CORS

### Step 3: Configure API Settings

Fill in the following details:

#### Choose the protocol
- Select: **REST**

#### Create new API
- Select: **New API**

#### Settings:

**API Name:**
```
personal-finance-api
```

**Description:** (Optional but recommended)
```
REST API for Personal Finance Tracker application. Provides endpoints for transactions, income, expenses, net worth, and file management.
```

**Endpoint Type:**
- Select: **Regional**

> **Endpoint Types Explained**:
> - **Edge Optimized**: Uses CloudFront for global distribution (higher latency for single-region)
> - **Regional**: Deployed in specific region (recommended for single-region apps)
> - **Private**: Only accessible from VPC (for internal APIs)

### Step 4: Create API

1. **Review Settings**
   - API name: `personal-finance-api`
   - Description: (your description)
   - Endpoint Type: Regional

2. **Click "Create API"**
   - The API will be created in a few seconds
   - You'll be redirected to the API's Resources page

### Step 5: Note API Details

After creation, note these important details:

1. **API ID**: Found in the API overview
   - Format: `abcd123456`
   - Used in API invoke URLs

2. **Root Resource ID**: Listed in Resources
   - Usually shown as `/`
   - This is the starting point for all paths

3. **API ARN**: In API settings
   - Format: `arn:aws:apigateway:region::/restapis/api-id`

**Example API Invoke URL Format**:
```
https://{api-id}.execute-api.{region}.amazonaws.com/{stage}
```

## 📊 Understanding API Structure

Your new API has the following structure:

```
personal-finance-api
└── / (root resource)
    ├── (resources will be added)
    └── (methods will be added)
```

In the next steps, you'll add:
- Resources (paths like `/v1`, `/transactions`)
- Methods (GET, POST, etc.)
- Integrations (Lambda functions)

## 🔧 Initial Configuration

### Enable CORS (We'll configure this properly later)

Even though we'll set up CORS properly later, it's good to understand where it's configured:

1. **In API Gateway Console**
   - Select your API
   - We'll configure CORS when we add resources

### Configure API Settings (Optional)

1. **Click on "Settings" in the left sidebar**

2. **API Settings** (optional configurations):
   - **Default endpoint**: Enable (allows API Gateway URL)
   - **Binary Media Types**: Leave empty for now
   - **Minimum compression size**: Leave at default (blank)

3. **Click "Save Changes"** if you made any modifications

## 📝 API Documentation

### Add OpenAPI Definition (Optional)

You can import your OpenAPI spec later:

1. **Go to "Documentation"** in left sidebar
2. You can import the OpenAPI spec from `api/specs/openapi.yaml`
3. Or click "Import API" and select the file

> **Note**: We'll build the API manually for learning purposes, but importing from OpenAPI spec is useful for automated deployments.

## 🔍 Verify API Creation

### Check API Details

1. **View API Overview**
   - In the left sidebar, click on your API name
   - Click "Dashboard"
   - Verify API ID, name, and endpoint type

2. **Note API Endpoint**
   ```
   https://{your-api-id}.execute-api.{region}.amazonaws.com
   ```

### Verify IAM Role for API Gateway

API Gateway needs permissions to invoke Lambda functions:

1. **Go to IAM Console**
2. **Check for API Gateway Service Role**
   - API Gateway creates this automatically
   - Or you may need to create it later when adding Lambda integration

## 📋 Checklist

Before proceeding, verify:

- [ ] REST API created successfully
- [ ] API name is `personal-finance-api`
- [ ] Endpoint type is Regional
- [ ] API ID noted and saved
- [ ] Root resource (/) visible in Resources
- [ ] API invoke URL format understood

## 🎨 API Gateway Console Overview

Familiarize yourself with the console layout:

### Left Sidebar
- **Resources**: Where you build your API structure
- **Stages**: Deployment stages (dev, staging, prod)
- **Authorizers**: Cognito and Lambda authorizers
- **Models**: Request/response schemas
- **Documentation**: API documentation
- **Binary Support**: Binary media types
- **Dashboard**: API metrics and overview
- **Settings**: API configuration

### Main Area
- **Resources Tree**: Shows your API structure
- **Method Execution**: Shows request/response flow
- **Integration Request/Response**: Configure Lambda integration

## 🚨 Troubleshooting

### API Creation Failed
**Problem**: Error creating API
**Solution**: 
- Check IAM permissions
- Ensure you selected correct endpoint type
- Try a different region if issues persist

### Cannot See Newly Created API
**Problem**: API doesn't appear in list
**Solution**:
- Refresh the page
- Check you're in the correct region (top-right corner)
- Verify IAM permissions

### Endpoint Type Cannot Be Changed
**Problem**: Need to change from Edge to Regional
**Solution**:
- Endpoint type cannot be changed after creation
- Delete and recreate the API with correct type
- Or clone the API with a different endpoint type

## 📚 Additional Resources

- [API Gateway REST API Concepts](https://docs.aws.amazon.com/apigateway/latest/developerguide/rest-api-develop.html)
- [Choosing Between REST APIs and HTTP APIs](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-vs-rest.html)
- [API Gateway Endpoints](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-api-endpoint-types.html)

## 💡 Best Practices

1. **Use Descriptive Names**: Makes management easier
2. **Add Descriptions**: Documents the API purpose
3. **Regional Endpoints**: Use for single-region applications
4. **Consistent Naming**: Use same prefix for all related resources
5. **Tag Resources**: Add tags for cost tracking and organization

## 📸 Expected Console Screenshots

At this point, your API Gateway console should show:

1. **Resources Page**:
   - API Name: `personal-finance-api`
   - One resource: `/` (root)
   - No methods yet

2. **Dashboard**:
   - API ID displayed
   - No metrics yet (not deployed)

## ✅ Completion

You've successfully created your REST API! 

**What's Next**: In the next step, you'll create resources and methods.

---

**Next Step**: [Resources and Methods](./03-resources-methods.md) →

**Previous Step**: [← Prerequisites](./01-prerequisites.md)

**Back to**: [Manual Setup Guide](./README.md)

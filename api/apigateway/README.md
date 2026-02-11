# API Gateway Setup for Personal Finance API

This directory contains instructions and automation scripts for setting up AWS API Gateway to integrate the frontend UI with the Personal Finance REST API backend.

## 📁 Directory Structure

```
api/apigateway/
├── README.md                           # This file - Overview and quick start
├── manual/                             # Step-by-step manual setup instructions
│   ├── README.md                       # Manual setup guide
│   ├── 01-prerequisites.md             # Prerequisites and requirements
│   ├── 02-rest-api-setup.md           # Creating REST API
│   ├── 03-resources-methods.md        # Setting up resources and methods
│   ├── 04-lambda-integration.md       # Integrating with Lambda functions
│   ├── 05-cognito-authorizer.md       # Setting up Cognito authorizer
│   ├── 06-cors-configuration.md       # Configuring CORS
│   ├── 07-deployment-stages.md        # Creating deployment stages
│   ├── 08-custom-domain.md            # Setting up custom domain (optional)
│   ├── 09-monitoring-logging.md       # Setting up monitoring and logging
│   └── 10-testing-validation.md       # Testing and validating the setup
└── automation/                         # Automation scripts and IaC
    ├── README.md                       # Automation guide
    ├── cloudformation/                 # CloudFormation templates (planned)
    ├── terraform/                      # Terraform scripts (planned)
    └── scripts/                        # Helper scripts (planned)
```

## 🎯 Overview

The Personal Finance API Gateway serves as the front door for all client requests to the Personal Finance API. It provides:

- **Request routing** to backend Lambda functions
- **Authentication** via AWS Cognito
- **Authorization** using JWT tokens
- **CORS handling** for web applications
- **Request/response transformation**
- **Throttling and rate limiting**
- **Monitoring and logging**

## 📋 API Endpoints

Based on the [OpenAPI specification](../specs/openapi.yaml), the API Gateway will expose:

### Transactions
- `GET /v1/transactions` - Get all transactions with filtering
- `GET /v1/transactions/{transactionId}` - Get specific transaction

### Income
- `GET /v1/income` - Get all income records
- `GET /v1/income/summary` - Get income summary

### Expenses
- `GET /v1/expenses` - Get all expense records
- `GET /v1/expenses/summary` - Get expense summary

### Net Worth
- `GET /v1/networth` - Get net worth data

### Files
- `POST /v1/files/upload-url` - Request file upload URL
- `GET /v1/files` - Get list of files

## 🚀 Quick Start

### For Manual Setup
Follow the comprehensive step-by-step guide in the [manual](./manual/) directory:

```bash
cd api/apigateway/manual
# Start with README.md and follow the numbered guides
```

### For Automated Setup
Use the automation scripts (coming soon):

```bash
cd api/apigateway/automation
# Follow instructions in automation/README.md
```

## 🏗️ Architecture

```
┌─────────────┐
│   Client    │ (Web/Mobile App)
│ (Frontend)  │
└──────┬──────┘
       │ HTTPS
       │
       ▼
┌─────────────────────────┐
│    API Gateway          │
│  ┌──────────────────┐   │
│  │ Cognito          │   │
│  │ Authorizer       │   │
│  └──────────────────┘   │
│  ┌──────────────────┐   │
│  │ Request          │   │
│  │ Validation       │   │
│  └──────────────────┘   │
└──────────┬──────────────┘
           │
           ▼
    ┌─────────────┐
    │   Lambda    │
    │  Function   │
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │  DynamoDB   │
    └─────────────┘
```

## 🔐 Security

The API Gateway implements multiple security layers:

1. **HTTPS Only**: All traffic is encrypted in transit
2. **Cognito Authentication**: JWT token-based authentication
3. **IAM Permissions**: Least-privilege access for Lambda execution
4. **CORS**: Properly configured for cross-origin requests
5. **Throttling**: Rate limiting to prevent abuse
6. **WAF Integration**: Web Application Firewall (optional)

## 📊 Integration with Backend

The API Gateway integrates with two Lambda functions:

1. **API Lambda** (`backend/api-lambda/`) - Handles GET requests for:
   - Transactions
   - Income
   - Expenses
   - Net Worth
   - Files listing

2. **File Processor Lambda** (`backend/file-processor-lambda/`) - Handles:
   - File upload URL generation
   - File processing and validation

## 🛠️ Setup Methods

### Option 1: Manual Setup (Recommended for Learning)
- Step-by-step guide using AWS Console
- Includes screenshots and detailed explanations
- Best for understanding how API Gateway works
- See [manual/README.md](./manual/README.md)

### Option 2: CloudFormation (Recommended for Production)
- Infrastructure as Code (IaC)
- Automated, repeatable deployments
- Version controlled
- See [automation/cloudformation/](./automation/cloudformation/)

### Option 3: Terraform (Alternative IaC)
- Multi-cloud capable
- Advanced state management
- See [automation/terraform/](./automation/terraform/)

## 📝 Prerequisites

Before setting up API Gateway, ensure you have:

- ✅ AWS Account with appropriate permissions
- ✅ Backend Lambda functions deployed (`backend/api-lambda/`)
- ✅ DynamoDB table created (if using real data)
- ✅ AWS Cognito User Pool configured (for authentication)
- ✅ AWS CLI installed (for automation)
- ✅ Understanding of API Gateway concepts

## 🎓 Documentation References

- **OpenAPI Spec**: [../specs/openapi.yaml](../specs/openapi.yaml)
- **Backend API Lambda**: [../../backend/api-lambda/README.md](../../backend/api-lambda/README.md)
- **API Collections**: [../collections/](../collections/)
- **AWS API Gateway Docs**: https://docs.aws.amazon.com/apigateway/

## 📈 Deployment Stages

The API Gateway should be configured with multiple stages:

- **dev** - Development environment for testing
- **staging** - Pre-production environment
- **prod** - Production environment

Each stage can have different:
- Lambda function versions
- Throttling limits
- Logging levels
- Custom domain mappings

## 🔍 Monitoring and Observability

Once deployed, monitor your API Gateway using:

- **CloudWatch Metrics**: Request count, latency, errors
- **CloudWatch Logs**: Request/response logs
- **X-Ray Tracing**: Distributed tracing for debugging
- **CloudWatch Alarms**: Alerts for errors and performance issues

## 🧪 Testing

After setup, test your API Gateway using:

1. **AWS Console Test Feature**: Built-in testing in API Gateway console
2. **Postman Collection**: [../collections/postman/](../collections/postman/)
3. **Bruno Collection**: [../collections/bruno/](../collections/bruno/)
4. **curl**: Command-line testing
5. **Frontend Application**: End-to-end testing

## 🆘 Troubleshooting

Common issues and solutions:

### 502 Bad Gateway
- Check Lambda function permissions
- Verify Lambda integration configuration
- Check Lambda function logs in CloudWatch

### 403 Forbidden
- Verify Cognito authorizer configuration
- Check JWT token validity
- Verify API Gateway resource policies

### CORS Errors
- Ensure OPTIONS method is configured
- Verify CORS headers in responses
- Check browser console for specific error

### High Latency
- Enable API caching
- Optimize Lambda function cold starts
- Use provisioned concurrency for Lambda

## 🔄 Updates and Maintenance

When updating the API:

1. Update OpenAPI specification first
2. Update Lambda function code
3. Update API Gateway resources/methods
4. Deploy to dev stage and test
5. Deploy to staging stage and validate
6. Deploy to production stage

## 🤝 Contributing

When adding new endpoints:

1. Update [OpenAPI spec](../specs/openapi.yaml)
2. Update Lambda function code
3. Update API Gateway configuration
4. Update this documentation
5. Update test collections

## 📞 Support

For questions or issues:
- Review the detailed manual setup guide
- Check AWS API Gateway documentation
- Open an issue in the repository
- Contact the Personal Finance team

## 🗺️ Roadmap

Future enhancements:

- [ ] WAF integration for enhanced security
- [ ] API caching strategy
- [ ] Multi-region deployment
- [ ] API versioning support
- [ ] GraphQL API Gateway (alternative)
- [ ] WebSocket support for real-time updates
- [ ] API keys for third-party integrations

---

**Next Steps**: Start with the [manual setup guide](./manual/README.md) or explore the [automation options](./automation/README.md).

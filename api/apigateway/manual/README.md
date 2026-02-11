# Manual API Gateway Setup Guide

This guide provides step-by-step instructions for manually setting up AWS API Gateway for the Personal Finance API using the AWS Web Console.

## 📖 Overview

This manual setup guide will walk you through creating an API Gateway REST API that integrates with your Lambda functions and implements proper authentication, CORS, and monitoring.

**Estimated Time**: 60-90 minutes

## 📚 Guide Structure

Follow these guides in order:

### 1. [Prerequisites](./01-prerequisites.md)
- AWS account setup
- Required permissions
- Backend Lambda deployment verification
- Cognito User Pool setup

### 2. [REST API Setup](./02-rest-api-setup.md)
- Creating a new REST API
- Configuring API settings
- Understanding API Gateway concepts

### 3. [Resources and Methods](./03-resources-methods.md)
- Creating API resources (paths)
- Configuring HTTP methods
- Setting up request/response models

### 4. [Lambda Integration](./04-lambda-integration.md)
- Connecting API Gateway to Lambda functions
- Configuring proxy integration
- Setting up request/response transformations

### 5. [Cognito Authorizer](./05-cognito-authorizer.md)
- Creating Cognito authorizer
- Configuring JWT validation
- Testing authentication

### 6. [CORS Configuration](./06-cors-configuration.md)
- Understanding CORS requirements
- Configuring OPTIONS method
- Setting up CORS headers

### 7. [Deployment and Stages](./07-deployment-stages.md)
- Creating deployment stages (dev, staging, prod)
- Stage variables and configuration
- Stage-specific settings

### 8. [Custom Domain](./08-custom-domain.md) *(Optional)*
- Setting up custom domain
- SSL certificate configuration
- DNS configuration

### 9. [Monitoring and Logging](./09-monitoring-logging.md)
- Enabling CloudWatch logs
- Setting up metrics and alarms
- X-Ray tracing configuration

### 10. [Testing and Validation](./10-testing-validation.md)
- Testing endpoints in AWS Console
- Using Postman/Bruno collections
- Troubleshooting common issues

## 🎯 What You'll Build

By the end of this guide, you'll have:

- ✅ A fully functional REST API Gateway
- ✅ Integration with Personal Finance Lambda functions
- ✅ Cognito-based authentication
- ✅ Proper CORS configuration
- ✅ Multiple deployment stages (dev, staging, prod)
- ✅ Comprehensive logging and monitoring
- ✅ Tested and validated endpoints

## 📋 API Structure

The API Gateway will expose these endpoints:

```
/v1
├── /transactions
│   ├── GET (list all transactions)
│   └── /{transactionId}
│       └── GET (get specific transaction)
├── /income
│   ├── GET (list all income)
│   └── /summary
│       └── GET (get income summary)
├── /expenses
│   ├── GET (list all expenses)
│   └── /summary
│       └── GET (get expense summary)
├── /networth
│   └── GET (get net worth data)
└── /files
    ├── GET (list files)
    └── /upload-url
        └── POST (get presigned upload URL)
```

## 🏗️ Architecture Diagram

```
Internet
    │
    │ HTTPS
    ▼
┌────────────────────────────────────┐
│      AWS API Gateway               │
│                                    │
│  ┌──────────────────────────────┐ │
│  │  Cognito Authorizer          │ │
│  │  (JWT Validation)            │ │
│  └──────────────────────────────┘ │
│                                    │
│  ┌──────────────────────────────┐ │
│  │  CORS Configuration          │ │
│  └──────────────────────────────┘ │
│                                    │
│  ┌──────────────────────────────┐ │
│  │  Request Validation          │ │
│  └──────────────────────────────┘ │
└────────────┬───────────────────────┘
             │
             ▼
    ┌────────────────┐
    │  Lambda Proxy  │
    │  Integration   │
    └────────┬───────┘
             │
       ┌─────┴─────┐
       │           │
       ▼           ▼
┌─────────────┐ ┌─────────────────────┐
│  API Lambda │ │ File Processor      │
│  Function   │ │ Lambda Function     │
└──────┬──────┘ └──────┬──────────────┘
       │               │
       ▼               ▼
┌─────────────┐ ┌─────────────┐
│  DynamoDB   │ │     S3      │
└─────────────┘ └─────────────┘
```

## 🔑 Key Concepts

Before starting, understand these API Gateway concepts:

### REST API vs HTTP API
- **REST API**: Full-featured, supports resource policies, API keys, request validation
- **HTTP API**: Lower latency, lower cost, simpler features
- **We'll use REST API** for full feature support

### Resources and Methods
- **Resources**: API paths (e.g., `/transactions`, `/income`)
- **Methods**: HTTP verbs (GET, POST, PUT, DELETE, OPTIONS)

### Integration Types
- **Lambda Proxy Integration**: Passes entire request to Lambda (recommended)
- **Lambda Integration**: Custom request/response transformations
- **HTTP Integration**: Forwards to HTTP endpoint
- **Mock Integration**: Returns static response

### Stages
- **Stage**: Named reference to a deployment
- Each stage can have different configurations
- Common stages: dev, staging, prod

### Authorizers
- **Cognito User Pools**: JWT token validation
- **Lambda Authorizer**: Custom authorization logic
- **IAM Authorization**: AWS signature v4

## ⚠️ Important Notes

### Before You Begin
1. **Have your Lambda functions deployed** - The API Gateway needs Lambda ARNs
2. **Have Cognito User Pool ready** - Required for authentication
3. **Use consistent naming** - Helps with organization and troubleshooting
4. **Take notes of ARNs** - You'll need them for configuration

### Best Practices
- ✅ Use descriptive names for resources and methods
- ✅ Enable CloudWatch logging from the start
- ✅ Test in dev stage before promoting to staging/prod
- ✅ Use stage variables for environment-specific configuration
- ✅ Document any custom configurations

### Common Pitfalls to Avoid
- ❌ Forgetting to deploy after making changes
- ❌ Not configuring CORS for web applications
- ❌ Missing Lambda execution permissions
- ❌ Incorrect Cognito authorizer configuration
- ❌ Not setting up proper IAM roles

## 🚀 Getting Started

Ready to begin? Start with [Prerequisites](./01-prerequisites.md) to ensure you have everything needed.

## 📞 Need Help?

If you encounter issues:
1. Check the troubleshooting section in each guide
2. Review CloudWatch logs for error messages
3. Verify all prerequisites are met
4. Consult AWS API Gateway documentation
5. Open an issue in the repository

## 🔄 Alternative: Automated Setup

If you prefer automated setup using Infrastructure as Code:
- See [../automation/README.md](../automation/README.md) for CloudFormation/Terraform options

---

**Next Step**: Continue to [Prerequisites](./01-prerequisites.md) →

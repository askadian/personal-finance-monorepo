# API Gateway Automation

This directory contains automation scripts and Infrastructure as Code (IaC) templates for deploying AWS API Gateway.

## 📋 Overview

Instead of manual setup, use automation for:
- ✅ Repeatable deployments
- ✅ Version control
- ✅ Faster setup
- ✅ Consistency across environments
- ✅ Easy rollbacks

## 📁 Directory Structure

```
automation/
├── README.md                    # This file
├── cloudformation/              # AWS CloudFormation templates
│   ├── README.md
│   ├── api-gateway.yaml        # Main API Gateway template
│   ├── parameters/             # Parameter files per environment
│   │   ├── dev.json
│   │   ├── staging.json
│   │   └── prod.json
│   └── scripts/                # Helper scripts
│       ├── deploy.sh
│       ├── validate.sh
│       └── delete.sh
├── terraform/                   # Terraform configurations
│   ├── README.md
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── environments/
│   │   ├── dev.tfvars
│   │   ├── staging.tfvars
│   │   └── prod.tfvars
│   └── modules/
│       ├── api-gateway/
│       └── cognito-authorizer/
└── scripts/                     # General automation scripts
    ├── README.md
    ├── generate-openapi.py      # Generate from OpenAPI spec
    ├── import-api.sh            # Import API from OpenAPI
    └── test-api.sh              # Automated API testing
```

## 🎯 Automation Options

### Option 1: CloudFormation (Recommended for AWS-only)

AWS-native Infrastructure as Code:

**Pros**:
- ✅ Native AWS support
- ✅ No additional tools needed
- ✅ Tight integration with AWS services
- ✅ AWS manages state

**Cons**:
- ❌ AWS-only (vendor lock-in)
- ❌ YAML/JSON can be verbose
- ❌ Less flexible than Terraform

**Use when**:
- You're committed to AWS
- Want native AWS integration
- Team familiar with CloudFormation

**Status**: 🚧 Coming soon - CloudFormation templates will be added

### Option 2: Terraform (Recommended for Multi-cloud)

Third-party Infrastructure as Code:

**Pros**:
- ✅ Multi-cloud support
- ✅ Better state management
- ✅ More readable syntax (HCL)
- ✅ Large community and modules

**Cons**:
- ❌ Requires Terraform installation
- ❌ Need to manage state file
- ❌ Learning curve

**Use when**:
- You use multiple cloud providers
- Want better IaC experience
- Team familiar with Terraform

**Status**: 🚧 Coming soon - Terraform configurations will be added

### Option 3: AWS CLI Scripts

Shell scripts using AWS CLI:

**Pros**:
- ✅ Simple and straightforward
- ✅ Easy to understand
- ✅ Good for quick deployments

**Cons**:
- ❌ Less declarative
- ❌ Harder to maintain
- ❌ No state management

**Use when**:
- Quick prototyping
- Simple deployments
- CI/CD pipelines

**Status**: 🚧 Coming soon - AWS CLI scripts will be added

### Option 4: AWS SAM (Serverless Application Model)

AWS SAM simplifies serverless deployments:

**Pros**:
- ✅ Simplified CloudFormation syntax
- ✅ Local testing support
- ✅ Built-in best practices

**Cons**:
- ❌ AWS Lambda-focused
- ❌ Less control than CloudFormation

**Use when**:
- Deploying serverless applications
- Want simplified syntax
- Need local testing

**Status**: 🚧 Future consideration

## 🚀 Quick Start (Coming Soon)

### Using CloudFormation

```bash
cd automation/cloudformation

# Validate template
./scripts/validate.sh

# Deploy to dev
./scripts/deploy.sh dev

# Deploy to prod
./scripts/deploy.sh prod
```

### Using Terraform

```bash
cd automation/terraform

# Initialize Terraform
terraform init

# Plan deployment
terraform plan -var-file=environments/dev.tfvars

# Apply deployment
terraform apply -var-file=environments/dev.tfvars
```

### Using AWS CLI

```bash
cd automation/scripts

# Import from OpenAPI spec
./import-api.sh ../../specs/openapi.yaml dev

# Test API
./test-api.sh dev
```

## 📝 What Will Be Automated

The automation scripts will create:

1. **API Gateway REST API**
   - All resources and methods from OpenAPI spec
   - Lambda proxy integrations
   - Request/response models

2. **Cognito Authorizer**
   - Configured for JWT validation
   - Applied to protected endpoints

3. **CORS Configuration**
   - OPTIONS methods
   - Proper CORS headers

4. **Deployment Stages**
   - Dev, staging, prod stages
   - Stage-specific configurations

5. **CloudWatch Integration**
   - Logging enabled
   - Metrics configured
   - Alarms set up

6. **IAM Roles and Permissions**
   - API Gateway execution roles
   - Lambda invoke permissions

7. **Custom Domain** (optional)
   - SSL certificate
   - DNS configuration
   - API mappings

## 🔄 CI/CD Integration

The automation scripts can be integrated with CI/CD pipelines:

### GitHub Actions Example

```yaml
name: Deploy API Gateway

on:
  push:
    branches: [main]
    paths:
      - 'api/apigateway/**'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v1
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
      
      - name: Deploy CloudFormation stack
        run: |
          cd api/apigateway/automation/cloudformation
          ./scripts/deploy.sh dev
```

## 📋 Prerequisites

Before using automation:

- [ ] AWS CLI installed and configured
- [ ] Appropriate AWS permissions (APIGateway, Lambda, CloudFormation/Terraform)
- [ ] Backend Lambda functions deployed
- [ ] Cognito User Pool created
- [ ] OpenAPI specification finalized

## 🔒 Security Considerations

When automating:

1. **Credentials**: Never commit AWS credentials
   - Use environment variables
   - Use AWS profiles
   - Use IAM roles in CI/CD

2. **Secrets**: Store sensitive values securely
   - Use AWS Secrets Manager
   - Use Parameter Store
   - Use CI/CD secret management

3. **Least Privilege**: Use minimal required permissions
   - Create specific IAM roles for automation
   - Limit scope of permissions

## 💡 Best Practices

1. **Version Control**: Commit all IaC templates
2. **Environments**: Separate configs per environment
3. **Testing**: Test in dev before prod
4. **Documentation**: Document custom configurations
5. **Validation**: Validate templates before deploying
6. **State Management**: Backup Terraform state files
7. **Idempotency**: Ensure scripts can run multiple times safely

## 🔮 Future Enhancements

Planned additions:

- [ ] Complete CloudFormation templates
- [ ] Complete Terraform configurations
- [ ] AWS CLI deployment scripts
- [ ] Automated testing scripts
- [ ] CI/CD pipeline examples
- [ ] Blue/green deployment support
- [ ] Canary deployment support
- [ ] Automated rollback scripts
- [ ] Cost estimation tools
- [ ] Documentation generation from templates

## 📞 Contributing

To add automation scripts:

1. Create the script/template
2. Test thoroughly in dev environment
3. Document prerequisites and usage
4. Add examples
5. Submit pull request

## 📚 Additional Resources

- [CloudFormation API Gateway Documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-restapi.html)
- [Terraform AWS Provider - API Gateway](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/api_gateway_rest_api)
- [AWS SAM Documentation](https://docs.aws.amazon.com/serverless-application-model/)
- [Infrastructure as Code Best Practices](https://docs.aws.amazon.com/whitepapers/latest/introduction-devops-aws/infrastructure-as-code.html)

## 🤝 Support

For automation questions:
- Review the manual setup guide first
- Check AWS documentation
- Review example templates (when available)
- Open an issue in the repository

---

**Note**: Automation scripts are under development. For now, please use the [manual setup guide](../manual/README.md).

**Back to**: [API Gateway README](../README.md)

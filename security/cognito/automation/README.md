# Cognito User Pool Automation

This directory contains automation scripts and Infrastructure as Code (IaC) templates for deploying AWS Cognito User Pool.

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
│   ├── cognito-user-pool.yaml  # Main User Pool template
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
│       └── cognito-user-pool/
└── scripts/                     # General automation scripts
    ├── README.md
    ├── create-test-user.sh      # Create test users
    ├── configure-client.sh      # Configure app client
    └── export-config.sh         # Export configuration
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

### Option 4: AWS CDK (Cloud Development Kit)

AWS CDK with TypeScript/Python:

**Pros**:
- ✅ Use familiar programming languages
- ✅ Type safety and IDE support
- ✅ Powerful abstractions

**Cons**:
- ❌ Requires CDK installation
- ❌ Generated CloudFormation can be complex

**Use when**:
- Team prefers programming over config files
- Want programmatic resource creation
- Need complex logic

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

# Create User Pool
./create-user-pool.sh dev

# Configure app client
./configure-client.sh dev

# Create test user
./create-test-user.sh dev testuser@example.com
```

## 📝 What Will Be Automated

The automation scripts will create:

1. **Cognito User Pool**
   - Email-based sign-in
   - Password policies
   - MFA configuration
   - Email verification

2. **App Client**
   - OAuth 2.0 configuration
   - Callback URLs per environment
   - Token expiration settings
   - Public client (no secret)

3. **Hosted UI Domain**
   - Cognito domain or custom domain
   - Branding configuration
   - CSS customization

4. **Email Configuration**
   - SES integration (production)
   - Cognito email (development)
   - Custom email templates

5. **Security Settings**
   - Password policies
   - MFA settings
   - Advanced security features (optional)

6. **IAM Roles and Policies**
   - SNS role for SMS
   - Lambda trigger permissions (if using)

## 🔄 CI/CD Integration

The automation scripts can be integrated with CI/CD pipelines:

### GitHub Actions Example

```yaml
name: Deploy Cognito User Pool

on:
  push:
    branches: [main]
    paths:
      - 'security/cognito/**'

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
          cd security/cognito/automation/cloudformation
          ./scripts/deploy.sh dev
```

## 📋 Prerequisites

Before using automation:

- [ ] AWS CLI installed and configured
- [ ] Appropriate AWS permissions (Cognito, IAM)
- [ ] CloudFormation/Terraform installed (depending on choice)
- [ ] Frontend callback URLs identified
- [ ] Domain for custom hosted UI (optional)

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
8. **Parameter Files**: Use separate parameter files for each environment

## 🔮 Future Enhancements

Planned additions:

- [ ] Complete CloudFormation templates
- [ ] Complete Terraform configurations
- [ ] AWS CLI deployment scripts
- [ ] Automated testing scripts
- [ ] CI/CD pipeline examples
- [ ] User migration scripts
- [ ] Backup and restore scripts
- [ ] Cost estimation tools
- [ ] Documentation generation from templates

## 📊 Environment Configuration

### Development
```yaml
environment: dev
user_pool_name: personal-finance-user-pool-dev
domain_prefix: personal-finance-dev
email_service: cognito
mfa: optional
password_policy: default
```

### Staging
```yaml
environment: staging
user_pool_name: personal-finance-user-pool-staging
domain_prefix: personal-finance-staging
email_service: ses
mfa: optional
password_policy: default
```

### Production
```yaml
environment: prod
user_pool_name: personal-finance-user-pool-prod
domain_prefix: personal-finance-prod
custom_domain: auth.yourdomain.com
email_service: ses
mfa: optional
password_policy: strong
advanced_security: enabled
```

## 📞 Contributing

To add automation scripts:

1. Create the script/template
2. Test thoroughly in dev environment
3. Document prerequisites and usage
4. Add examples
5. Submit pull request

## 📚 Additional Resources

- [CloudFormation Cognito Documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html)
- [Terraform AWS Cognito Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cognito_user_pool)
- [AWS CLI Cognito Commands](https://docs.aws.amazon.com/cli/latest/reference/cognito-idp/index.html)
- [Infrastructure as Code Best Practices](https://docs.aws.amazon.com/whitepapers/latest/introduction-devops-aws/infrastructure-as-code.html)

## 🤝 Support

For automation questions:
- Review the manual setup guide first
- Check AWS documentation
- Review example templates (when available)
- Open an issue in the repository

---

**Note**: Automation scripts are under development. For now, please use the [manual setup guide](../manual/README.md).

**Back to**: [Cognito README](../README.md)

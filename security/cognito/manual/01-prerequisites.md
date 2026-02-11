# Prerequisites for Cognito User Pool Setup

Before setting up AWS Cognito User Pool, ensure you have all necessary requirements and understanding.

## 📋 Overview

This guide covers:
1. AWS account and permissions requirements
2. Understanding of key Cognito concepts
3. Planning your User Pool configuration
4. Gathering necessary information

**Estimated Time**: 15 minutes

## ✅ Requirements Checklist

### AWS Account Requirements

- [ ] **Active AWS Account**
  - Sign up at https://aws.amazon.com if you don't have one
  - Credit card required for account activation
  - Free tier available for Cognito (50,000 MAU)

- [ ] **AWS Console Access**
  - Ability to log in to AWS Management Console
  - Access to Cognito service
  - Access to IAM for permission management

- [ ] **Required AWS Permissions**
  ```json
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Action": [
          "cognito-idp:CreateUserPool",
          "cognito-idp:UpdateUserPool",
          "cognito-idp:DescribeUserPool",
          "cognito-idp:CreateUserPoolClient",
          "cognito-idp:UpdateUserPoolClient",
          "cognito-idp:CreateUserPoolDomain",
          "cognito-idp:DescribeUserPoolDomain",
          "cognito-idp:ListUsers",
          "cognito-idp:AdminCreateUser",
          "cognito-idp:AdminSetUserPassword"
        ],
        "Resource": "*"
      }
    ]
  }
  ```

### Knowledge Requirements

- [ ] **Basic AWS Understanding**
  - Familiarity with AWS Console navigation
  - Understanding of AWS services and regions
  - Basic knowledge of IAM roles and permissions

- [ ] **Authentication Concepts**
  - Understanding of OAuth 2.0 protocol
  - Familiarity with JWT (JSON Web Tokens)
  - Knowledge of authentication vs authorization
  - Understanding of token-based authentication

- [ ] **Web Application Concepts**
  - Understanding of HTTP/HTTPS
  - Familiarity with REST APIs
  - Knowledge of frontend-backend integration
  - Understanding of cross-origin requests (CORS)

### Planning Requirements

- [ ] **User Pool Configuration Planning**
  - Decide on sign-in method (email recommended)
  - Plan required user attributes
  - Determine password policy requirements
  - Decide on MFA strategy (optional/required)

- [ ] **Frontend Application Details**
  - Frontend domain/URL (e.g., https://app.example.com)
  - Callback URLs for OAuth redirect
  - Logout URLs
  - Development vs production environments

- [ ] **Email/SMS Configuration**
  - Email service decision (Cognito default or SES)
  - Domain for sending emails (if using SES)
  - SMS service requirements (if using MFA with SMS)

## 🔍 Understanding Key Concepts

### What is AWS Cognito User Pool?

AWS Cognito User Pool is a fully managed user directory service that:
- Stores user profiles and credentials
- Handles user registration and authentication
- Issues JWT tokens for authenticated users
- Provides hosted UI for login/signup
- Supports MFA, password reset, email verification
- Scales automatically based on usage

### Authentication Flow

Understanding the authentication flow is crucial:

```
┌─────────────┐
│   User      │
│  (Browser)  │
└──────┬──────┘
       │ 1. Navigate to app
       ▼
┌─────────────┐
│  Frontend   │
│    App      │
└──────┬──────┘
       │ 2. Redirect to Cognito
       ▼
┌─────────────┐
│   Cognito   │
│  Hosted UI  │
└──────┬──────┘
       │ 3. User logs in
       ▼
┌─────────────┐
│   Cognito   │
│  User Pool  │ 4. Validates credentials
└──────┬──────┘
       │ 5. Issues JWT tokens
       ▼
┌─────────────┐
│  Frontend   │
│    App      │ 6. Stores tokens
└──────┬──────┘
       │ 7. Makes API requests with token
       ▼
┌─────────────┐
│     API     │
│   Gateway   │ 8. Validates token
└──────┬──────┘
       │ 9. Forwards to Lambda
       ▼
┌─────────────┐
│   Lambda    │
│  Function   │ 10. Processes request
└─────────────┘
```

### JWT Tokens Explained

**ID Token:**
- Contains user identity information
- Used by frontend to display user info
- Contains claims: username, email, custom attributes
- Short-lived (typically 1 hour)

Example ID token claims:
```json
{
  "sub": "a1b2c3d4-5678-90ab-cdef-EXAMPLE11111",
  "email": "user@example.com",
  "email_verified": true,
  "cognito:username": "user@example.com",
  "aud": "your-app-client-id",
  "token_use": "id",
  "iat": 1234567890,
  "exp": 1234571490
}
```

**Access Token:**
- Used for API authorization
- Sent in Authorization header to API Gateway
- Contains scopes and permissions
- Short-lived (typically 1 hour)

**Refresh Token:**
- Long-lived (typically 30 days)
- Used to obtain new ID and access tokens
- Should be stored securely
- Can be revoked for security

### OAuth 2.0 Grant Types

**Authorization Code Grant** (Recommended for this project):
- Most secure flow for web applications
- Uses authorization code exchange
- Supports PKCE for public clients
- Tokens never exposed in browser URL

**Implicit Grant** (Not recommended):
- Simpler but less secure
- Tokens exposed in URL
- No refresh token support
- Being phased out

### Sign-in Options

**Email (Recommended):**
- Users sign in with email address
- Natural and familiar to users
- Easy to remember
- Supports email verification

**Username:**
- Users create and use a username
- Additional field to manage
- Harder for users to remember
- Can be used as alias

**Phone Number:**
- Users sign in with phone number
- Requires SMS verification
- Additional SMS costs
- Regional availability concerns

## 📝 Information to Gather

Before starting, collect this information:

### 1. User Pool Configuration

| Setting | Decision | Notes |
|---------|----------|-------|
| User Pool Name | `personal-finance-user-pool` | Descriptive name |
| AWS Region | `us-east-1` (or your choice) | Choose closest region |
| Sign-in Option | Email (recommended) | How users will sign in |
| Required Attributes | email | Cannot be changed later |
| Custom Attributes | (if needed) | Plan carefully, immutable |

### 2. Password Policy

| Setting | Recommendation | Notes |
|---------|---------------|-------|
| Minimum Length | 8 characters | Balance security and usability |
| Uppercase Required | Yes | Enhanced security |
| Lowercase Required | Yes | Enhanced security |
| Numbers Required | Yes | Enhanced security |
| Symbols Required | Yes | Enhanced security |
| Temporary Password Validity | 7 days | How long temp passwords are valid |

### 3. MFA Configuration

| Setting | Recommendation | Notes |
|---------|---------------|-------|
| MFA Enforcement | Optional | Users can enable if desired |
| MFA Methods | TOTP preferred | Authenticator apps |
| SMS Backup | Optional | Additional cost |

### 4. Email Configuration

| Setting | Development | Production |
|---------|-------------|------------|
| Email Service | Cognito default | Amazon SES |
| Sender Email | no-reply@verificationemail.com | noreply@yourdomain.com |
| Email Sending Limit | 50/day | Unlimited with SES |

### 5. Frontend URLs

| Environment | URL | Notes |
|-------------|-----|-------|
| Development | http://localhost:3000 | Local development |
| Staging | https://staging.yourdomain.com | Staging environment |
| Production | https://app.yourdomain.com | Production environment |

## 🛠️ Tools and Access Needed

### AWS Console
- Browser access to https://console.aws.amazon.com
- Bookmark: https://console.aws.amazon.com/cognito/

### Text Editor
- For saving User Pool ID, App Client ID, etc.
- Notepad, VSCode, or similar

### Browser Developer Tools
- For inspecting tokens and network requests
- Chrome DevTools, Firefox Developer Tools

## 🚨 Important Decisions

These decisions are **immutable** after User Pool creation:

### ⚠️ Required Attributes
Once you mark an attribute as "required," you cannot change it. Choose carefully:
- **Recommended**: Only email as required
- **Avoid**: Making too many attributes required
- **Reason**: More flexibility for user onboarding

### ⚠️ Custom Attributes
Custom attributes cannot be removed or modified after creation:
- **Plan ahead**: Determine all custom attributes needed
- **Naming**: Use descriptive names (e.g., `custom:membershipLevel`)
- **Type**: String, Number, DateTime, Boolean
- **Mutability**: Readable and writable vs read-only

### ⚠️ Sign-in Method
The sign-in method (username, email, phone) cannot be changed:
- **Recommended**: Email (most user-friendly)
- **Alternative**: Username (if email privacy is a concern)
- **Consider**: User experience and ease of use

## ✅ Pre-Setup Verification

Before proceeding, verify:

1. **AWS Account**
   ```bash
   # Login to AWS Console
   # Navigate to: https://console.aws.amazon.com/cognito/
   # Verify you can access the Cognito service
   ```

2. **Permissions**
   ```bash
   # In IAM, check your user has Cognito permissions
   # Or confirm you have Administrator access
   ```

3. **Planning Complete**
   - [ ] User Pool name decided
   - [ ] Sign-in method decided
   - [ ] Required attributes planned
   - [ ] Password policy defined
   - [ ] MFA strategy determined
   - [ ] Frontend URLs identified

## 📚 Recommended Reading

Before starting:
- [AWS Cognito User Pool Overview](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-identity-pools.html)
- [OAuth 2.0 Simplified](https://oauth.net/2/)
- [Understanding JWT](https://jwt.io/introduction)

## 🎯 Next Steps

Once you've completed this checklist and gathered all information:

1. **Review your decisions** - Ensure sign-in method and required attributes are correct
2. **Have information ready** - Keep your planning notes accessible
3. **Proceed to next guide** - [User Pool Setup](./02-user-pool-setup.md)

## 🆘 Troubleshooting

### Cannot Access Cognito Service
- Verify your AWS account is active
- Check you're in the correct region
- Verify IAM permissions

### Don't Know Frontend URLs Yet
- You can add callback URLs later
- Start with `http://localhost:3000` for development
- Update production URLs when ready

### Unsure About Configuration
- Start with recommended settings
- Can be modified later (except immutable items)
- Test with development User Pool first

---

**Next Step**: Continue to [User Pool Setup](./02-user-pool-setup.md) →

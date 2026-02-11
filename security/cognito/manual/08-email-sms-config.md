# Email and SMS Configuration

Guide for configuring email and SMS delivery for Cognito.

## 📋 Overview

Configure how Cognito sends verification emails and SMS messages.

**Estimated Time**: 10 minutes

## Email Configuration

**Development/Testing:**
- Use Cognito default email
- Limit: 50 emails per day
- From: no-reply@verificationemail.com

**Production:**
- Use Amazon SES
- Unlimited sending (based on SES limits)
- Custom from address (noreply@yourdomain.com)
- Custom email templates

## SMS Configuration

**Required for:**
- SMS-based MFA
- Phone number verification

**Setup:**
- Create IAM role for SNS
- Configure SMS settings in Cognito
- Set spending limits

**Cost:** Standard SMS rates apply

## Email Templates

Customize email messages:
- Verification emails
- Password reset emails
- Welcome emails

---

**Previous**: [MFA Setup](./07-mfa-setup.md) | **Next**: [Lambda Triggers](./09-triggers-lambda.md)

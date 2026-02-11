# User Attributes Configuration

Configuration guide for user attributes in Cognito User Pool.

## 📋 Overview

User attributes define the information stored for each user in your User Pool.

**Estimated Time**: 10 minutes

## Standard Attributes

AWS Cognito provides standard attributes:
- email (required for this project)
- name
- phone_number
- birthdate
- address
- And more...

## Custom Attributes

You can define custom attributes for your application-specific data:
- Format: `custom:attributeName`
- Types: String, Number, DateTime, Boolean
- Immutable after creation

## Configuration

For the Personal Finance app, the following attributes are recommended:

**Required:**
- email (already configured)

**Optional:**
- name
- phone_number (if using SMS MFA)

**Custom attributes** (examples):
- custom:membershipLevel
- custom:preferredCurrency
- custom:accountCreationDate

---

**Previous**: [Hosted UI Setup](./04-hosted-ui-setup.md) | **Next**: [Password Policies](./06-password-policies.md)

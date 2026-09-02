# Frontend Cost Analysis

This document provides a rough cost estimate for hosting the `frontend/` React application on Amazon S3 and Amazon CloudFront.

## Assumptions

The estimate below assumes a small personal project with moderate usage:

- 1 GB of static assets stored in S3
- 10,000 page views per month
- 2 to 5 GB of CloudFront data transfer out per month
- Low request volume
- One custom domain managed with Route 53

Actual costs vary by region, traffic, file sizes, and cache efficiency.

## Cost components

### 1. Amazon S3

S3 is used to store the generated static frontend files.

Typical charges:

- Storage: very small for a frontend build, usually only a few cents per month
- Requests: usually negligible for a low-traffic static site

Estimated monthly cost:

- **$0.02 to $0.03** for around 1 GB of storage
- Requests: usually pennies

### 2. Amazon CloudFront

CloudFront serves the website to users and caches files at the edge.

Typical charges:

- Data transfer out to the internet
- HTTPS requests

Estimated monthly cost:

- For 2 to 5 GB/month of traffic: roughly **$0.20 to $0.60**
- Request charges are usually minimal at low traffic levels

### 3. Route 53

If you use a custom domain such as `app.example.com`, you may need Route 53.

Typical charges:

- Hosted zone: around **$0.50/month**
- DNS query charges: usually minor

### 4. ACM certificate

If you use HTTPS with CloudFront and a custom domain:

- ACM public certificates are **free**

## Rough monthly estimate

### Without a custom domain

Expected total:

- **About $0.25 to $1/month**

### With a custom domain via Route 53

Expected total:

- **About $0.75 to $2/month**

## Cost optimization tips

- Keep static assets cached for a long time
- Use hashed filenames for JS and CSS bundles
- Invalidate only `index.html` when possible
- Keep the S3 bucket private and let CloudFront serve public traffic
- Reduce image sizes and bundle size to lower bandwidth usage

## Example monthly scenario

A small personal finance dashboard with a few users might look like this:

- S3 storage: a few cents
- CloudFront bandwidth: a few tens of cents
- Route 53 hosted zone: $0.50

That usually keeps the frontend hosting cost well under a few dollars per month.

## Important note

This estimate covers only the frontend hosting layer. It does **not** include backend services such as:

- API Gateway
- Lambda
- DynamoDB
- Cognito
- S3 upload storage for user documents

Those services can add separate charges depending on usage.

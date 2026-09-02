# Hosting the Frontend on S3 and CloudFront

This guide explains how to deploy the `frontend/` React application as a static site on Amazon S3 and serve it through Amazon CloudFront.

## What this setup does

- Builds the React app into static assets
- Stores the build output in a private S3 bucket
- Serves the site through CloudFront over HTTPS
- Supports client-side routing for React Router
- Keeps the bucket private by using CloudFront access to S3

## Prerequisites

Before you begin, make sure you have:

- An AWS account
- AWS CLI installed and configured
- Node.js and npm installed
- The repository cloned locally
- Permission to create S3, CloudFront, and ACM resources

## Step 1: Build the frontend

From the repository root:

```bash
cd frontend
npm install
npm run build
```

This creates a production build in `frontend/build/`.

## Step 2: Create an S3 bucket

Create a bucket for the static frontend files, for example:

- `personal-finance-frontend-prod`

Recommended settings:

- Keep **Block all public access** enabled
- Enable **Versioning** if you want rollback capability
- Enable **Default encryption**
- Use the same AWS region as your other resources where practical

You do **not** need to make the bucket public if you use CloudFront with Origin Access Control.

## Step 3: Upload the build artifacts to S3

Upload the compiled frontend to the bucket:

```bash
aws s3 sync build/ s3://personal-finance-frontend-prod --delete
```

If you rebuild the app, run the sync command again to update the bucket.

## Step 4: Create a CloudFront distribution

In the CloudFront console:

1. Create a new distribution
2. Set the origin to your S3 bucket
3. Use **Origin Access Control (OAC)** so the bucket stays private
4. Set the **Default root object** to `index.html`
5. Set **Viewer protocol policy** to `Redirect HTTP to HTTPS`
6. Attach a cache policy suitable for a React SPA

## Step 5: Configure SPA routing

If you use React Router, set CloudFront custom error responses so client-side routes resolve correctly:

- 403 → `/index.html` with HTTP 200
- 404 → `/index.html` with HTTP 200

This allows routes like `/dashboard` to work when the page is refreshed.

## Step 6: Allow CloudFront to read from S3

If you use Origin Access Control, CloudFront will sign requests to S3. Update the S3 bucket policy so only the CloudFront distribution can read objects.

## Step 7: Configure environment variables

The frontend uses build-time environment variables for API and AWS configuration. Before building, set values such as:

```bash
REACT_APP_UPLOAD_API_URL=https://your-api-id.execute-api.us-east-1.amazonaws.com/dev
REACT_APP_FINANCE_API_URL=https://your-api-id.execute-api.us-east-1.amazonaws.com
REACT_APP_S3_BUCKET_NAME=personal-finance-uploads-dev
REACT_APP_AWS_REGION=us-east-1
```

Then rebuild and re-upload the site.

## Step 8: Add a custom domain, if needed

If you want a friendly URL such as `app.example.com`:

1. Request an ACM certificate in `us-east-1`
2. Add the certificate to CloudFront
3. Create a DNS record pointing your domain to the CloudFront distribution

## Step 9: Invalidate CloudFront after deployment

After deploying a new build, invalidate cached content:

```bash
aws cloudfront create-invalidation \
  --distribution-id YOUR_DISTRIBUTION_ID \
  --paths "/*"
```

For a React app, it is often enough to invalidate only `index.html` if your static asset filenames are hashed.

## Recommended deployment flow

A simple production deploy looks like this:

```bash
cd frontend
npm run build
aws s3 sync build/ s3://personal-finance-frontend-prod --delete
aws cloudfront create-invalidation --distribution-id YOUR_DISTRIBUTION_ID --paths "/*"
```

## Notes

- Keep the bucket private
- Use HTTPS only
- Rebuild whenever environment variables change
- CloudFront is the public entry point; S3 remains the origin storage layer

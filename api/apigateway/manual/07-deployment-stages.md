# Deployment and Stages

This guide walks through deploying your API and configuring multiple stages (dev, staging, prod).

## 📋 Overview

In this step, you will:
1. Deploy your API to a stage
2. Create multiple deployment stages
3. Configure stage-specific settings
4. Test deployed endpoints

**Estimated Time**: 15-20 minutes

## 🚀 Understanding Deployments and Stages

### What is a Deployment?

A **deployment** is a snapshot of your API configuration at a point in time.

### What is a Stage?

A **stage** is a named reference to a deployment, like:
- `dev` - Development environment
- `staging` - Pre-production testing
- `prod` - Production environment

### Why Multiple Stages?

- Test changes in `dev` before promoting to `prod`
- Different Lambda versions per stage
- Different throttling/logging per environment

## 📝 Step-by-Step Instructions

### Step 1: Create First Deployment

1. **Go to Resources**
   - Select your API in API Gateway console
   - Click **Resources** in left sidebar

2. **Deploy API**
   - Click **Actions** dropdown
   - Select **Deploy API**

3. **Deployment Configuration**:
   - **Deployment stage**: Select **[New Stage]**
   - **Stage name**: `dev`
   - **Stage description**: `Development environment`
   - **Deployment description**: `Initial deployment with Lambda integration and Cognito auth`

4. **Click Deploy**

Your API is now deployed! You'll see the **Invoke URL**:
```
https://{api-id}.execute-api.{region}.amazonaws.com/dev
```

### Step 2: Test Deployed Endpoint

Copy the invoke URL and test:

```bash
# Without authentication (should return 401)
curl https://{api-id}.execute-api.us-east-1.amazonaws.com/dev/v1/transactions

# With authentication
curl https://{api-id}.execute-api.us-east-1.amazonaws.com/dev/v1/transactions \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Step 3: Configure Stage Settings

1. **Go to Stages**
   - Click **Stages** in left sidebar
   - Select **dev** stage

2. **Configure Settings**:

#### Logs/Tracing Tab

- **CloudWatch Logs**:
  - Enable CloudWatch Logs: **✓**
  - Log level: **INFO** (for dev, use **ERROR** for prod)
  - Log full requests/responses data: **✓** (dev only)

- **CloudWatch Metrics**:
  - Enable Detailed CloudWatch Metrics: **✓**

- **X-Ray Tracing**:
  - Enable X-Ray Tracing: **✓** (optional but recommended)

#### Settings Tab

- **Throttle**:
  - Rate: `1000` requests per second
  - Burst: `2000` requests

- **Cache Settings**:
  - Enable API cache: Leave disabled for dev
  - TTL: N/A

3. **Click Save Changes**

### Step 4: Create Staging Stage

1. **Create New Stage**:
   - Actions → **Create Stage**
   - Or: Stages → **Create**

2. **Stage Configuration**:
   - **Stage name**: `staging`
   - **Stage description**: `Staging environment for pre-production testing`
   - **Deployment**: Select latest deployment

3. **Configure Settings**:
   - CloudWatch Logs: INFO
   - Detailed Metrics: ✓
   - Throttle: 1000/2000

4. **Click Create**

### Step 5: Create Production Stage

1. **Create New Stage**:
   - **Stage name**: `prod`
   - **Stage description**: `Production environment`
   - **Deployment**: Select latest deployment

2. **Configure Production Settings**:
   - **CloudWatch Logs**: ERROR only
   - **Log full requests/responses**: ✗ (security/performance)
   - **Detailed Metrics**: ✓
   - **X-Ray Tracing**: ✓
   - **Throttle**: Adjust based on needs (e.g., 5000/10000)
   - **Cache Settings**: Consider enabling (e.g., 300 seconds)

3. **Click Create**

## 🔧 Stage Variables (Advanced)

Stage variables allow environment-specific configuration.

### Create Stage Variable

1. **Select Stage** (e.g., dev)

2. **Variables Tab**

3. **Add Variable**:
   - Name: `lambdaAlias`
   - Value: `dev`

4. **Click Save**

### Use in Lambda Integration

When configuring Lambda integration, use:
```
personal-finance-api-${stageVariables.lambdaAlias}
```

This allows different Lambda versions per stage.

## 📊 Stage URLs

After creating stages, you'll have:

```
Development:
https://{api-id}.execute-api.{region}.amazonaws.com/dev

Staging:
https://{api-id}.execute-api.{region}.amazonaws.com/staging

Production:
https://{api-id}.execute-api.{region}.amazonaws.com/prod
```

## 🔄 Deploying Changes

When you make changes to your API:

1. **Make Changes** in Resources

2. **Test Changes** using Test feature

3. **Deploy to Dev**:
   - Actions → Deploy API
   - Stage: `dev`
   - Description: "Added new endpoint for..."
   - Deploy

4. **Test in Dev Stage**

5. **Promote to Staging**:
   - Actions → Deploy API
   - Stage: `staging`
   - Deploy

6. **Test in Staging**

7. **Promote to Production**:
   - Actions → Deploy API
   - Stage: `prod`
   - Deploy

> **Important**: Changes in Resources are NOT live until deployed!

## 🧪 Testing Different Stages

### Test Dev Stage

```bash
curl https://{api-id}.execute-api.us-east-1.amazonaws.com/dev/v1/transactions \
  -H "Authorization: Bearer $DEV_TOKEN"
```

### Test Prod Stage

```bash
curl https://{api-id}.execute-api.us-east-1.amazonaws.com/prod/v1/transactions \
  -H "Authorization: Bearer $PROD_TOKEN"
```

## 📋 Checklist

- [ ] API deployed to `dev` stage
- [ ] Dev invoke URL tested and works
- [ ] CloudWatch logging enabled for dev
- [ ] `staging` stage created
- [ ] `prod` stage created
- [ ] Different throttling configured per stage
- [ ] All stage URLs documented

## 🚨 Troubleshooting

### Changes Not Reflected
**Problem**: Made changes but they don't work
**Solution**:
- Remember to deploy after making changes
- Actions → Deploy API → Select stage

### 403 Forbidden
**Problem**: Deployed API returns 403
**Solution**:
1. Check Lambda permissions are set
2. Verify Cognito authorizer configuration
3. Check stage-level resource policy

### Different Stage Same Behavior
**Problem**: All stages behave identically
**Solution**:
- Use stage variables to point to different Lambda versions
- Configure stage-specific settings

## 💡 Best Practices

### Deployment Strategy

1. **Always test in dev first**
2. **Use deployment descriptions** - Document what changed
3. **Promote gradually**: dev → staging → prod
4. **Monitor after deployment**: Check CloudWatch metrics
5. **Keep prod conservative**: Lower log levels, enable caching

### Stage Configuration

| Setting | Dev | Staging | Prod |
|---------|-----|---------|------|
| Log Level | INFO | INFO | ERROR |
| Full Request/Response | ✓ | ✗ | ✗ |
| Detailed Metrics | ✓ | ✓ | ✓ |
| X-Ray Tracing | ✓ | ✓ | ✓ |
| Throttle Rate | 1000 | 2000 | 5000 |
| Cache | ✗ | ✗ | ✓ |

### Rollback Strategy

If deployment issues occur:

1. **Go to Deployments** in stage
2. **Select previous deployment**
3. **Change Deployment** to rollback

## 📚 Additional Resources

- [API Gateway Stages](https://docs.aws.amazon.com/apigateway/latest/developerguide/stages.html)
- [Stage Variables](https://docs.aws.amazon.com/apigateway/latest/developerguide/stage-variables.html)
- [Deployment Best Practices](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-known-issues.html)

## ✅ Completion

You've successfully deployed your API to multiple stages!

**What's Next**: Configure custom domain (optional) or proceed to monitoring setup.

---

**Next Step**: [Custom Domain](./08-custom-domain.md) → (Optional)

**Previous Step**: [← CORS Configuration](./06-cors-configuration.md)

**Back to**: [Manual Setup Guide](./README.md)

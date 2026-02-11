# Monitoring and Logging

This guide walks through setting up comprehensive monitoring and logging for your API Gateway.

## 📋 Overview

In this step, you will:
1. Configure CloudWatch Logs
2. Set up CloudWatch Metrics and Dashboards
3. Create CloudWatch Alarms
4. Enable X-Ray tracing
5. Monitor API performance

**Estimated Time**: 20-30 minutes

## 📊 CloudWatch Logs

### Enable Logging (Per Stage)

1. **Go to Stages**
   - Select your API
   - Click **Stages**
   - Select stage (e.g., `prod`)

2. **Logs/Tracing Tab**

3. **CloudWatch Settings**:
   - **Enable CloudWatch Logs**: ✓
   - **Log Level**: 
     - `ERROR` for production
     - `INFO` for development
   - **Log full requests/responses**: 
     - ✓ for dev (helpful for debugging)
     - ✗ for prod (security and performance)
   - **Data Trace**: ✗ (contains sensitive data)

4. **Save Changes**

### View Logs

1. **Go to CloudWatch Console**

2. **Log Groups**
   - Navigate to: `/aws/apigateway/personal-finance-api`
   - Or: `API-Gateway-Execution-Logs_{api-id}/{stage}`

3. **View Log Streams**
   - Each request creates log entries
   - Filter by error, request ID, or time range

### Example Log Entry

```
(request-id) Endpoint request headers: {Authorization=Bearer eyJ..., Content-Type=application/json}
(request-id) Endpoint response body: {"data":[...]}
(request-id) Method response body: {"data":[...]}
```

## 📈 CloudWatch Metrics

### Available Metrics

API Gateway automatically publishes metrics:

- **Count**: Total API requests
- **4XXError**: Client errors (e.g., 400, 401, 403)
- **5XXError**: Server errors (e.g., 500, 502, 504)
- **Latency**: Time to process request
- **IntegrationLatency**: Time spent calling Lambda
- **CacheHitCount**: Cache hit rate
- **CacheMissCount**: Cache miss rate

### View Metrics

1. **Go to CloudWatch Console**

2. **Metrics → All Metrics**

3. **Select ApiGateway**

4. **View by**:
   - API Name
   - API Name, Method, Resource, Stage
   - API Name, Stage

### Create Dashboard

1. **CloudWatch Console → Dashboards**

2. **Create Dashboard**:
   - Name: `personal-finance-api-dashboard`

3. **Add Widgets**:

#### API Request Count

- Widget type: **Line**
- Metric: `AWS/ApiGateway → Count`
- Filter: API Name = `personal-finance-api`
- Statistic: Sum
- Period: 5 minutes

#### Error Rate

- Widget type: **Line**
- Metrics:
  - `4XXError` (Sum)
  - `5XXError` (Sum)
- Period: 5 minutes

#### Latency

- Widget type: **Line**
- Metrics:
  - `Latency` (Average, p50, p99)
  - `IntegrationLatency` (Average)
- Period: 5 minutes

4. **Save Dashboard**

## 🚨 CloudWatch Alarms

### Create Error Rate Alarm

1. **CloudWatch Console → Alarms**

2. **Create Alarm**

3. **Select Metric**:
   - Namespace: **AWS/ApiGateway**
   - Metric: **5XXError**
   - API Name: `personal-finance-api`
   - Stage: `prod`

4. **Conditions**:
   - Threshold type: **Static**
   - Whenever 5XXError is: **Greater than** `10`
   - Period: **5 minutes**
   - Datapoints to alarm: **2 out of 3**

5. **Actions**:
   - Create SNS topic: `api-gateway-alerts`
   - Email endpoints: Your email
   - Confirm subscription

6. **Name**: `personal-finance-api-prod-high-errors`

7. **Create Alarm**

### Create Latency Alarm

1. **Create Alarm**

2. **Select Metric**: `Latency`

3. **Conditions**:
   - Threshold: **Greater than** `3000` (milliseconds)
   - Period: **5 minutes**

4. **Actions**: Same SNS topic

5. **Name**: `personal-finance-api-prod-high-latency`

### Recommended Alarms

- [ ] High 5XX error rate
- [ ] High 4XX error rate (adjust threshold)
- [ ] High latency (p99 > 3 seconds)
- [ ] High throttle count
- [ ] Lambda function errors

## 🔍 X-Ray Tracing

### Enable X-Ray

1. **Go to Stages**

2. **Select Stage** (e.g., `prod`)

3. **Logs/Tracing Tab**

4. **Enable X-Ray Tracing**: ✓

5. **Save Changes**

### View X-Ray Traces

1. **Go to X-Ray Console**

2. **Service Map**:
   - Visual representation of API → Lambda → DynamoDB flow
   - Shows latency and error rates

3. **Traces**:
   - View individual request traces
   - See detailed timing breakdown
   - Identify bottlenecks

### X-Ray Benefits

- **End-to-end tracing**: See entire request path
- **Performance analysis**: Identify slow components
- **Error debugging**: Pinpoint error sources
- **Service dependencies**: Understand system architecture

## 📝 Lambda Function Logging

Ensure Lambda functions log properly:

```python
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info(f"Request received: {event['path']}")
    
    try:
        # Process request
        result = process_request(event)
        
        logger.info(f"Request successful: {event['requestContext']['requestId']}")
        return result
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        return error_response(500, "Internal server error")
```

### View Lambda Logs

- Log Group: `/aws/lambda/personal-finance-api-dev`
- Use CloudWatch Insights for advanced queries

## 📊 Monitoring Best Practices

### What to Monitor

1. **Request Volume**: Track API usage trends
2. **Error Rates**: Monitor 4XX and 5XX errors
3. **Latency**: Ensure good performance
4. **Cache Performance**: Optimize cache hit rate
5. **Throttling**: Detect rate limit issues
6. **Lambda Performance**: Monitor cold starts, duration

### Logging Best Practices

1. **Structured Logging**: Use JSON format
2. **Request IDs**: Log correlation IDs
3. **Sanitize Data**: Never log sensitive information (tokens, passwords)
4. **Appropriate Levels**: ERROR for issues, INFO for important events
5. **Cost Management**: Reduce logging in production

### Alert Thresholds

- **5XX Errors**: > 1% of requests
- **4XX Errors**: > 10% of requests (adjust based on your API)
- **Latency**: p99 > 3 seconds
- **Throttles**: > 5% of requests

## 📋 Checklist

- [ ] CloudWatch Logs enabled for all stages
- [ ] Log levels configured appropriately
- [ ] CloudWatch Dashboard created
- [ ] Error rate alarms configured
- [ ] Latency alarms configured
- [ ] X-Ray tracing enabled
- [ ] Lambda functions log properly
- [ ] SNS topic created for alerts
- [ ] Email notifications working

## 🚨 Troubleshooting

### No Logs Appearing
**Solution**:
1. Check CloudWatch Logs permission in API Gateway settings
2. Verify IAM role has logging permissions
3. Check Log Group exists

### Metrics Not Showing
**Solution**:
1. Wait 5-10 minutes for metrics to appear
2. Ensure Detailed CloudWatch Metrics are enabled
3. Check metric dimensions (API name, stage)

### X-Ray Not Working
**Solution**:
1. Verify X-Ray tracing is enabled in stage settings
2. Check Lambda execution role has X-Ray permissions
3. Ensure X-Ray daemon is running (handled by Lambda automatically)

## 💡 Cost Optimization

### Reduce Logging Costs

1. **Production**: Log ERROR only
2. **Disable Full Request/Response**: Saves storage
3. **Set Log Retention**: 7-30 days for most logs
4. **Use Sampling**: X-Ray sampling rate < 100%

### Monitor Costs

- CloudWatch → Billing dashboard
- Set budget alerts
- Review log group storage monthly

## 📚 Additional Resources

- [API Gateway Logging](https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-logging.html)
- [CloudWatch Metrics](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-metrics-and-dimensions.html)
- [X-Ray with API Gateway](https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-xray.html)

## ✅ Completion

You've successfully set up comprehensive monitoring and logging!

**What's Next**: Test and validate your complete API Gateway setup.

---

**Next Step**: [Testing and Validation](./10-testing-validation.md) →

**Previous Step**: [← Custom Domain](./08-custom-domain.md)

**Back to**: [Manual Setup Guide](./README.md)

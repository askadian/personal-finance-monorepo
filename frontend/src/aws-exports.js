// AWS Amplify configuration
// This file should be updated with actual AWS Cognito values during deployment
const awsmobile = {
  aws_project_region: process.env.REACT_APP_AWS_REGION || 'us-east-1',
  aws_cognito_region: process.env.REACT_APP_AWS_REGION || 'us-east-1',
  aws_user_pools_id: process.env.REACT_APP_USER_POOL_ID || '',
  aws_user_pools_web_client_id: process.env.REACT_APP_USER_POOL_CLIENT_ID || '',
  oauth: {},
  Auth: {
    region: process.env.REACT_APP_AWS_REGION || 'us-east-1',
    userPoolId: process.env.REACT_APP_USER_POOL_ID || '',
    userPoolWebClientId: process.env.REACT_APP_USER_POOL_CLIENT_ID || '',
  },
};

export default awsmobile;

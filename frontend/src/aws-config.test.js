/**
 * AWS Configuration Test
 * 
 * This test validates that the AWS Cognito configuration structure is correct.
 */

import awsConfig from './aws-config';

describe('AWS Configuration', () => {
  test('awsConfig should have Auth.Cognito structure', () => {
    expect(awsConfig).toHaveProperty('Auth');
    expect(awsConfig.Auth).toHaveProperty('Cognito');
  });

  test('awsConfig should have required Cognito fields', () => {
    const cognitoConfig = awsConfig.Auth.Cognito;
    
    expect(cognitoConfig).toHaveProperty('region');
    expect(cognitoConfig).toHaveProperty('userPoolId');
    expect(cognitoConfig).toHaveProperty('userPoolClientId');
  });

  test('awsConfig should have optional userPoolClientSecret field', () => {
    const cognitoConfig = awsConfig.Auth.Cognito;
    
    // The field should exist (even if it's a placeholder value)
    expect(cognitoConfig).toHaveProperty('userPoolClientSecret');
  });

  test('awsConfig should have proper cookieStorage configuration', () => {
    const cognitoConfig = awsConfig.Auth.Cognito;
    
    expect(cognitoConfig).toHaveProperty('cookieStorage');
    expect(cognitoConfig.cookieStorage).toHaveProperty('domain');
    expect(cognitoConfig.cookieStorage).toHaveProperty('path');
    expect(cognitoConfig.cookieStorage).toHaveProperty('expires');
    expect(cognitoConfig.cookieStorage).toHaveProperty('secure');
  });

  test('awsConfig should have OAuth configuration', () => {
    const cognitoConfig = awsConfig.Auth.Cognito;
    
    expect(cognitoConfig).toHaveProperty('loginWith');
    expect(cognitoConfig.loginWith).toHaveProperty('oauth');
    expect(cognitoConfig.loginWith.oauth).toHaveProperty('domain');
    expect(cognitoConfig.loginWith.oauth).toHaveProperty('scopes');
    expect(cognitoConfig.loginWith.oauth).toHaveProperty('redirectSignIn');
    expect(cognitoConfig.loginWith.oauth).toHaveProperty('redirectSignOut');
    expect(cognitoConfig.loginWith.oauth).toHaveProperty('responseType');
  });
});

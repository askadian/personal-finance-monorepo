import React from 'react';
import { createRoot } from 'react-dom/client';
import { Amplify } from 'aws-amplify';
import awsConfig from './aws-config';
import App from './App';

// Configure AWS Amplify with Cognito settings
Amplify.configure(awsConfig);

const root = createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

import React from 'react';
import { Navigate } from 'react-router-dom';

const ProtectedRoute = ({ children }) => {
  // Check if user is authenticated
  // NOTE: In production, this should validate authentication with AWS Amplify's getCurrentUser()
  // or server-side token validation. localStorage is used here only for demo mode.
  const isAuthenticated = localStorage.getItem('isAuthenticated') === 'true';

  if (!isAuthenticated) {
    // Redirect to sign in page if not authenticated
    return <Navigate to="/" replace />;
  }

  return children;
};

export default ProtectedRoute;

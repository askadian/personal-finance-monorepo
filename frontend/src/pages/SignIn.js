import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { signIn } from 'aws-amplify/auth';
import './SignIn.css';

const SignIn = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSignIn = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      // If AWS Cognito is not configured, simulate sign in for demo
      if (!process.env.REACT_APP_USER_POOL_ID) {
        console.warn('AWS Cognito not configured. Using demo mode.');
        // Store demo user in localStorage
        localStorage.setItem('isAuthenticated', 'true');
        localStorage.setItem('username', username);
        navigate('/dashboard');
      } else {
        await signIn({ username, password });
        localStorage.setItem('isAuthenticated', 'true');
        localStorage.setItem('username', username);
        navigate('/dashboard');
      }
    } catch (err) {
      setError(err.message || 'Failed to sign in. Please check your credentials.');
    } finally {
      setLoading(false);
    }
  };

  const handleForgotPassword = () => {
    // Navigate to password reset page
    alert('Password reset functionality will be implemented with AWS Cognito. Please contact administrator.');
  };

  return (
    <div className="signin-container">
      <div className="signin-card">
        <div className="signin-header">
          <h2>Personal Finance Tracker</h2>
          <p>Sign in to your account</p>
        </div>
        
        <form onSubmit={handleSignIn} className="signin-form">
          {error && <div className="alert alert-danger">{error}</div>}
          
          <div className="form-group">
            <label htmlFor="username">Username or Email</label>
            <input
              type="text"
              id="username"
              className="form-control"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Enter your username or email"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              className="form-control"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter your password"
              required
            />
          </div>

          <button 
            type="submit" 
            className="btn btn-primary btn-block"
            disabled={loading}
          >
            {loading ? 'Signing in...' : 'Sign In'}
          </button>

          <div className="forgot-password-container">
            <button
              type="button"
              className="btn btn-link"
              onClick={handleForgotPassword}
            >
              Forgot Password?
            </button>
          </div>
        </form>

        <div className="signin-footer">
          <p>Secured by AWS Cognito</p>
        </div>
      </div>
    </div>
  );
};

export default SignIn;

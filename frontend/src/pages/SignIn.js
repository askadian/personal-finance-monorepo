import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Lock, Mail, AlertCircle } from 'lucide-react';
import { loginUser } from '../services/authService';
import './SignIn.css';

function SignIn() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSignIn = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      // Authenticate with AWS Cognito
      const result = await loginUser(email, password);
      
      if (result.success) {
        console.log('Sign in successful, redirecting to dashboard');
        navigate('/dashboard');
      } else {
        setError(result.error || 'Failed to sign in. Please check your credentials.');
      }
    } catch (err) {
      console.error('Unexpected error during sign in:', err);
      setError('An unexpected error occurred. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleResetPassword = () => {
    // Placeholder for password reset
    console.log('Password reset requested for:', email);
    alert('Password reset functionality will be implemented with AWS Cognito forgot password flow.');
  };

  return (
    <div className="signin-container">
      <div className="signin-card">
        <h1 className="signin-title">Personal Finance Tracker</h1>
        <h2 className="signin-subtitle">Sign In</h2>
        
        {error && (
          <div className="error-message">
            <AlertCircle size={18} />
            <span>{error}</span>
          </div>
        )}
        
        <form onSubmit={handleSignIn} className="signin-form">
          <div className="form-group">
            <label htmlFor="email">
              <Mail size={18} />
              <span>Email / Username</span>
            </label>
            <input
              type="text"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Enter your email or username"
              required
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">
              <Lock size={18} />
              <span>Password</span>
            </label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter your password"
              required
              disabled={loading}
            />
          </div>

          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? 'Signing In...' : 'Sign In'}
          </button>
        </form>

        <button 
          type="button" 
          className="btn-link"
          onClick={handleResetPassword}
          disabled={loading}
        >
          Forgot Password?
        </button>
      </div>
    </div>
  );
}

export default SignIn;

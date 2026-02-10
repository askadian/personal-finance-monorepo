import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Lock, Mail } from 'lucide-react';
import './SignIn.css';

function SignIn() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleSignIn = (e) => {
    e.preventDefault();
    // Placeholder authentication logic
    console.log('Sign in attempt with email:', email);
    // Simulate successful login and redirect to dashboard
    navigate('/dashboard');
  };

  const handleResetPassword = () => {
    // Placeholder for password reset
    console.log('Password reset requested for:', email);
    alert('Password reset link would be sent to your email. (Placeholder functionality)');
  };

  return (
    <div className="signin-container">
      <div className="signin-card">
        <h1 className="signin-title">Personal Finance Tracker</h1>
        <h2 className="signin-subtitle">Sign In</h2>
        
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
            />
          </div>

          <button type="submit" className="btn-primary">
            Sign In
          </button>
        </form>

        <button 
          type="button" 
          className="btn-link"
          onClick={handleResetPassword}
        >
          Forgot Password?
        </button>
      </div>
    </div>
  );
}

export default SignIn;

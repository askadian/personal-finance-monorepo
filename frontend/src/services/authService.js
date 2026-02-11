/**
 * Authentication Service
 * 
 * This service provides authentication utilities using AWS Amplify and Cognito.
 * It abstracts AWS Amplify authentication operations for easier use throughout the app.
 */

import { signIn, signOut, getCurrentUser, fetchUserAttributes, fetchAuthSession } from 'aws-amplify/auth';

/**
 * Signs in a user with username/email and password
 * @param {string} username - The user's username or email
 * @param {string} password - The user's password
 * @returns {Promise<object>} - Sign in result with user information
 */
export const loginUser = async (username, password) => {
  try {
    const signInResult = await signIn({ username, password });
    console.log('Sign in successful:', signInResult);
    return {
      success: true,
      isSignedIn: signInResult.isSignedIn,
      nextStep: signInResult.nextStep
    };
  } catch (error) {
    console.error('Error signing in:', error);
    return {
      success: false,
      error: error.message || 'Failed to sign in'
    };
  }
};

/**
 * Signs out the current user
 * @returns {Promise<object>} - Sign out result
 */
export const logoutUser = async () => {
  try {
    await signOut();
    console.log('Sign out successful');
    return {
      success: true
    };
  } catch (error) {
    console.error('Error signing out:', error);
    return {
      success: false,
      error: error.message || 'Failed to sign out'
    };
  }
};

/**
 * Gets the current authenticated user
 * @returns {Promise<object>} - Current user object or null if not authenticated
 */
export const getCurrentAuthUser = async () => {
  try {
    const user = await getCurrentUser();
    console.log('Current user:', user);
    return {
      success: true,
      user: user
    };
  } catch (error) {
    console.error('Error getting current user:', error);
    return {
      success: false,
      user: null,
      error: error.message
    };
  }
};

/**
 * Gets the current user's attributes
 * @returns {Promise<object>} - User attributes or null if not authenticated
 */
export const getUserAttributes = async () => {
  try {
    const attributes = await fetchUserAttributes();
    console.log('User attributes:', attributes);
    return {
      success: true,
      attributes: attributes
    };
  } catch (error) {
    console.error('Error fetching user attributes:', error);
    return {
      success: false,
      attributes: null,
      error: error.message
    };
  }
};

/**
 * Checks if a user is currently authenticated
 * @returns {Promise<boolean>} - True if user is authenticated, false otherwise
 */
export const isAuthenticated = async () => {
  try {
    await getCurrentUser();
    return true;
  } catch (error) {
    return false;
  }
};

/**
 * Gets the current authentication session with tokens
 * @returns {Promise<object>} - Session object with tokens or null if not authenticated
 */
export const getAuthSession = async () => {
  try {
    const session = await fetchAuthSession();
    console.log('Auth session:', session);
    return {
      success: true,
      session: session,
      tokens: session.tokens
    };
  } catch (error) {
    console.error('Error fetching auth session:', error);
    return {
      success: false,
      session: null,
      error: error.message
    };
  }
};

/**
 * Gets the ID token for API requests
 * @returns {Promise<string|null>} - ID token string or null if not authenticated
 */
export const getIdToken = async () => {
  try {
    const session = await fetchAuthSession();
    return session.tokens?.idToken?.toString() || null;
  } catch (error) {
    console.error('Error getting ID token:', error);
    return null;
  }
};

/**
 * Gets the access token for API requests
 * @returns {Promise<string|null>} - Access token string or null if not authenticated
 */
export const getAccessToken = async () => {
  try {
    const session = await fetchAuthSession();
    return session.tokens?.accessToken?.toString() || null;
  } catch (error) {
    console.error('Error getting access token:', error);
    return null;
  }
};

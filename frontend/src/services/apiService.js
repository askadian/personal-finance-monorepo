/**
 * API Service
 * 
 * Base service for making authenticated API requests to the Personal Finance API.
 * Handles authentication, error handling, and request/response formatting.
 */

import { getIdToken } from './authService';

/**
 * Get the API endpoint from environment variables
 * Falls back to a default value if not set
 */
const getApiEndpoint = () => {
  const endpoint = process.env.REACT_APP_API_ENDPOINT;
  
  if (!endpoint || endpoint === 'https://your-api-id.execute-api.us-east-1.amazonaws.com/prod') {
    console.warn('API endpoint not configured. Please set REACT_APP_API_ENDPOINT in your .env file');
    return null;
  }
  
  return endpoint;
};

/**
 * Makes an authenticated API request
 * @param {string} path - API path (e.g., '/v1/transactions')
 * @param {object} options - Fetch options
 * @returns {Promise<object>} - Response data
 */
export const apiRequest = async (path, options = {}) => {
  const apiEndpoint = getApiEndpoint();
  
  if (!apiEndpoint) {
    throw new Error('API endpoint not configured');
  }
  
  try {
    // Get ID token for authentication
    const idToken = await getIdToken();
    
    if (!idToken) {
      throw new Error('Not authenticated');
    }
    
    // Construct full URL
    const url = `${apiEndpoint}${path}`;
    
    // Merge default headers with provided headers
    const headers = {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${idToken}`,
      ...options.headers
    };
    
    // Make the request
    const response = await fetch(url, {
      ...options,
      headers
    });
    
    // Parse response
    const data = await response.json();
    
    // Handle HTTP errors
    if (!response.ok) {
      throw new Error(data.error?.message || `HTTP ${response.status}: ${response.statusText}`);
    }
    
    return data;
  } catch (error) {
    console.error('API request failed:', error);
    throw error;
  }
};

/**
 * Makes a GET request to the API
 * @param {string} path - API path
 * @param {object} queryParams - Query parameters
 * @returns {Promise<object>} - Response data
 */
export const apiGet = async (path, queryParams = {}) => {
  // Build query string
  const params = new URLSearchParams();
  Object.entries(queryParams).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== '') {
      params.append(key, value);
    }
  });
  
  const queryString = params.toString();
  const fullPath = queryString ? `${path}?${queryString}` : path;
  
  return apiRequest(fullPath, {
    method: 'GET'
  });
};

/**
 * Makes a POST request to the API
 * @param {string} path - API path
 * @param {object} body - Request body
 * @returns {Promise<object>} - Response data
 */
export const apiPost = async (path, body = {}) => {
  return apiRequest(path, {
    method: 'POST',
    body: JSON.stringify(body)
  });
};

/**
 * Checks if API is configured
 * @returns {boolean} - True if API endpoint is configured
 */
export const isApiConfigured = () => {
  const endpoint = getApiEndpoint();
  return endpoint !== null;
};

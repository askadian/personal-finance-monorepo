/**
 * Finance Service
 *
 * This service handles fetching financial data (transactions, income, expenses, net worth)
 * from the decoupled HTTP API Gateway.
 */

import { fetchAuthSession } from 'aws-amplify/auth';

/**
 * Base helper for making authorized API requests
 * @param {string} path - API path (e.g., '/v1/transactions')
 * @param {object} params - Query parameters
 * @returns {Promise<object>} - API response
 */
const apiRequest = async (path, params = {}) => {
  try {
    const session = await fetchAuthSession();
    const idToken = session.tokens?.idToken?.toString();

    if (!idToken) {
      throw new Error('User not authenticated');
    }

    const apiEndpoint = process.env.REACT_APP_FINANCE_API_URL;

    if (!apiEndpoint) {
      throw new Error('Finance API endpoint not configured. Please check your .env.local file.');
    }

    // Build URL with query parameters
    const url = new URL(`${apiEndpoint}${path}`);
    Object.keys(params).forEach(key => {
      if (params[key] !== undefined && params[key] !== null) {
        url.searchParams.append(key, params[key]);
      }
    });

    const response = await fetch(url.toString(), {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${idToken}`
      }
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error?.message || `API request failed with status ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error(`Error fetching ${path}:`, error);
    throw error;
  }
};

/**
 * Get all transactions
 * @param {object} filters - Filtering and pagination parameters
 * @returns {Promise<object>} - Transactions data
 */
export const getTransactions = async (filters = {}) => {
  return apiRequest('/v1/transactions', filters);
};

/**
 * Get a specific transaction by ID
 * @param {string} transactionId - Transaction ID
 * @returns {Promise<object>} - Transaction data
 */
export const getTransactionById = async (transactionId) => {
  return apiRequest(`/v1/transactions/${transactionId}`);
};

/**
 * Get income records
 * @param {object} filters - Filtering parameters
 * @returns {Promise<object>} - Income data
 */
export const getIncome = async (filters = {}) => {
  return apiRequest('/v1/income', filters);
};

/**
 * Get income summary
 * @returns {Promise<object>} - Income summary data
 */
export const getIncomeSummary = async () => {
  return apiRequest('/v1/income/summary');
};

/**
 * Get expense records
 * @param {object} filters - Filtering parameters
 * @returns {Promise<object>} - Expenses data
 */
export const getExpenses = async (filters = {}) => {
  return apiRequest('/v1/expenses', filters);
};

/**
 * Get expenses summary
 * @returns {Promise<object>} - Expenses summary data
 */
export const getExpensesSummary = async () => {
  return apiRequest('/v1/expenses/summary');
};

/**
 * Get net worth data
 * @returns {Promise<object>} - Net worth data
 */
export const getNetWorth = async () => {
  return apiRequest('/v1/networth');
};

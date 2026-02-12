/**
 * Transaction Service
 * 
 * Service for managing financial transactions via the Personal Finance API.
 * Provides methods to fetch transactions with filtering and pagination.
 */

import { apiGet } from './apiService';

/**
 * Fetches all transactions for the authenticated user
 * @param {object} options - Query options
 * @param {string} options.startDate - Filter transactions from this date (ISO 8601 format)
 * @param {string} options.endDate - Filter transactions until this date (ISO 8601 format)
 * @param {string} options.category - Filter by transaction category
 * @param {number} options.limit - Maximum number of transactions to return (default: 50)
 * @param {number} options.offset - Number of transactions to skip for pagination (default: 0)
 * @returns {Promise<object>} - Response with transactions data and pagination info
 */
export const getTransactions = async (options = {}) => {
  try {
    const {
      startDate,
      endDate,
      category,
      limit = 50,
      offset = 0
    } = options;
    
    const queryParams = {
      startDate,
      endDate,
      category,
      limit,
      offset
    };
    
    const response = await apiGet('/v1/transactions', queryParams);
    
    return {
      success: true,
      data: response.data || [],
      pagination: response.pagination || {}
    };
  } catch (error) {
    console.error('Error fetching transactions:', error);
    return {
      success: false,
      data: [],
      pagination: {},
      error: error.message || 'Failed to fetch transactions'
    };
  }
};

/**
 * Fetches a specific transaction by ID
 * @param {string} transactionId - The transaction ID
 * @returns {Promise<object>} - Response with transaction data
 */
export const getTransactionById = async (transactionId) => {
  try {
    if (!transactionId) {
      throw new Error('Transaction ID is required');
    }
    
    const response = await apiGet(`/v1/transactions/${transactionId}`);
    
    return {
      success: true,
      data: response.data || null
    };
  } catch (error) {
    console.error('Error fetching transaction:', error);
    return {
      success: false,
      data: null,
      error: error.message || 'Failed to fetch transaction'
    };
  }
};

/**
 * Sorts transactions by date (newest first)
 * @param {Array} transactions - Array of transaction objects
 * @returns {Array} - Sorted transactions
 */
export const sortTransactionsByDate = (transactions) => {
  if (!Array.isArray(transactions)) {
    return [];
  }
  
  return [...transactions].sort((a, b) => {
    const dateA = new Date(a.date);
    const dateB = new Date(b.date);
    return dateB - dateA; // Newest first
  });
};

/**
 * Formats a transaction amount for display
 * @param {number} amount - Transaction amount
 * @returns {string} - Formatted amount with currency symbol
 */
export const formatTransactionAmount = (amount) => {
  if (typeof amount !== 'number') {
    return '$0.00';
  }
  
  const absAmount = Math.abs(amount);
  const formatted = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD'
  }).format(absAmount);
  
  return amount < 0 ? `-${formatted}` : formatted;
};

/**
 * Formats a date for display
 * @param {string} dateString - ISO date string
 * @returns {string} - Formatted date
 */
export const formatTransactionDate = (dateString) => {
  try {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    }).format(date);
  } catch (error) {
    return dateString;
  }
};

/**
 * Gets a display-friendly category name
 * @param {string} category - Category key
 * @returns {string} - Formatted category name
 */
export const getCategoryDisplayName = (category) => {
  if (!category) return 'Other';
  
  const categoryMap = {
    'groceries': 'Groceries',
    'utilities': 'Utilities',
    'entertainment': 'Entertainment',
    'healthcare': 'Healthcare',
    'transportation': 'Transportation',
    'dining': 'Dining',
    'shopping': 'Shopping',
    'other': 'Other'
  };
  
  return categoryMap[category] || category.charAt(0).toUpperCase() + category.slice(1);
};

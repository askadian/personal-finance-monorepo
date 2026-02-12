import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  LogOut, 
  Upload, 
  TrendingUp, 
  TrendingDown, 
  List, 
  DollarSign,
  AlertCircle,
  RefreshCw
} from 'lucide-react';
import { logoutUser } from '../services/authService';
import { 
  getTransactions, 
  sortTransactionsByDate,
  formatTransactionAmount,
  formatTransactionDate,
  getCategoryDisplayName
} from '../services/transactionService';
import { isApiConfigured } from '../services/apiService';
import FileUpload from '../components/FileUpload';
import './Dashboard.css';

function Dashboard() {
  const [activeTab, setActiveTab] = useState('transactions');
  const [showUpload, setShowUpload] = useState(false);
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [pagination, setPagination] = useState({ limit: 50, offset: 0, total: 0 });
  const navigate = useNavigate();

  // Fetch transactions when component mounts or tab changes
  const fetchTransactions = useCallback(async () => {
    // Check if API is configured
    if (!isApiConfigured()) {
      setError('API endpoint not configured. Please check your .env file.');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const result = await getTransactions({
        limit: pagination.limit,
        offset: 0
      });

      if (result.success) {
        // Sort transactions by date (newest first)
        const sortedTransactions = sortTransactionsByDate(result.data);
        setTransactions(sortedTransactions);
        setPagination(result.pagination);
      } else {
        setError(result.error || 'Failed to fetch transactions');
      }
    } catch (err) {
      setError(err.message || 'An unexpected error occurred');
    } finally {
      setLoading(false);
    }
  }, [pagination.limit]);

  useEffect(() => {
    if (activeTab === 'transactions') {
      fetchTransactions();
    }
  }, [activeTab, fetchTransactions]);

  const handleLoadMore = async () => {
    setLoading(true);
    setError(null);

    try {
      const result = await getTransactions({
        limit: pagination.limit,
        offset: pagination.offset + pagination.limit
      });

      if (result.success) {
        // Append new transactions and sort the entire combined array
        const combinedTransactions = [...transactions, ...result.data];
        const sortedTransactions = sortTransactionsByDate(combinedTransactions);
        setTransactions(sortedTransactions);
        setPagination(result.pagination);
      } else {
        setError(result.error || 'Failed to load more transactions');
      }
    } catch (err) {
      setError(err.message || 'An unexpected error occurred');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = async () => {
    try {
      // Sign out from AWS Cognito
      const result = await logoutUser();
      
      if (result.success) {
        console.log('User logged out successfully');
        navigate('/');
      } else {
        console.error('Logout failed:', result.error);
        // Still navigate to sign-in page even if logout fails
        navigate('/');
      }
    } catch (error) {
      console.error('Unexpected error during logout:', error);
      // Still navigate to sign-in page even if an error occurs
      navigate('/');
    }
  };

  const tabs = [
    { id: 'transactions', label: 'Transactions', icon: List },
    { id: 'income', label: 'Income', icon: TrendingUp },
    { id: 'expenses', label: 'Expenses', icon: TrendingDown },
    { id: 'networth', label: 'Net Worth', icon: DollarSign }
  ];

  const renderTabContent = () => {
    switch (activeTab) {
      case 'transactions':
        return (
          <div className="tab-content">
            <div className="content-header">
              <h2>Transactions</h2>
              <button 
                className="btn-refresh"
                onClick={fetchTransactions}
                disabled={loading}
                title="Refresh transactions"
              >
                <RefreshCw size={18} className={loading ? 'spinning' : ''} />
              </button>
            </div>

            {error && (
              <div className="error-message">
                <AlertCircle size={20} />
                <span>{error}</span>
              </div>
            )}

            {loading && transactions.length === 0 ? (
              <div className="loading-state">
                <RefreshCw size={48} className="spinning" color="#ccc" />
                <p>Loading transactions...</p>
              </div>
            ) : transactions.length > 0 ? (
              <>
                <div className="transactions-list">
                  {transactions.map((transaction) => (
                    <div key={transaction.id} className="transaction-item">
                      <div className="transaction-main">
                        <div className="transaction-info">
                          <span className="transaction-description">
                            {transaction.description}
                          </span>
                          <span className="transaction-meta">
                            {transaction.merchant && (
                              <span className="merchant">{transaction.merchant}</span>
                            )}
                            {transaction.category && (
                              <span className="category">
                                {getCategoryDisplayName(transaction.category)}
                              </span>
                            )}
                          </span>
                        </div>
                        <div className="transaction-details">
                          <span className={`transaction-amount ${transaction.amount < 0 ? 'debit' : 'credit'}`}>
                            {formatTransactionAmount(transaction.amount)}
                          </span>
                          <span className="transaction-date">
                            {formatTransactionDate(transaction.date)}
                          </span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>

                {pagination.offset + pagination.limit < pagination.total && (
                  <div className="load-more-container">
                    <button 
                      className="btn-load-more"
                      onClick={handleLoadMore}
                      disabled={loading}
                    >
                      {loading ? 'Loading...' : 'Load More'}
                    </button>
                    <p className="pagination-info">
                      Showing {transactions.length} of {pagination.total} transactions
                    </p>
                  </div>
                )}
              </>
            ) : (
              <div className="placeholder-content">
                <List size={64} color="#ccc" />
                <p>No transactions to display yet. Upload a bank statement to get started.</p>
              </div>
            )}
          </div>
        );
      case 'income':
        return (
          <div className="tab-content">
            <h2>Income</h2>
            <p>Track your income sources and trends.</p>
            <div className="placeholder-content">
              <TrendingUp size={64} color="#4ade80" />
              <p>Upload pay stubs or other income documents to see your income analysis.</p>
            </div>
          </div>
        );
      case 'expenses':
        return (
          <div className="tab-content">
            <h2>Expenses</h2>
            <p>Monitor your spending patterns and categories.</p>
            <div className="placeholder-content">
              <TrendingDown size={64} color="#f87171" />
              <p>Your expense breakdown will be displayed here once you upload statements.</p>
            </div>
          </div>
        );
      case 'networth':
        return (
          <div className="tab-content">
            <h2>Net Worth</h2>
            <p>View your estimated net worth over time.</p>
            <div className="placeholder-content">
              <DollarSign size={64} color="#fbbf24" />
              <p>Your net worth calculation will appear here based on your financial data.</p>
            </div>
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>Personal Finance Dashboard</h1>
        <div className="header-actions">
          <button 
            className="btn-upload"
            onClick={() => setShowUpload(true)}
          >
            <Upload size={18} />
            <span>Upload File</span>
          </button>
          <button 
            className="btn-logout"
            onClick={handleLogout}
          >
            <LogOut size={18} />
            <span>Logout</span>
          </button>
        </div>
      </header>

      <nav className="dashboard-tabs">
        {tabs.map(tab => {
          const Icon = tab.icon;
          return (
            <button
              key={tab.id}
              className={`tab ${activeTab === tab.id ? 'active' : ''}`}
              onClick={() => setActiveTab(tab.id)}
            >
              <Icon size={20} />
              <span>{tab.label}</span>
            </button>
          );
        })}
      </nav>

      <main className="dashboard-main">
        {renderTabContent()}
      </main>

      {showUpload && (
        <FileUpload onClose={() => setShowUpload(false)} />
      )}
    </div>
  );
}

export default Dashboard;

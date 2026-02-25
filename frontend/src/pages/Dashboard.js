import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  LogOut, 
  Upload, 
  TrendingUp, 
  TrendingDown, 
  List, 
  DollarSign,
  Loader2,
  AlertCircle
} from 'lucide-react';
import { logoutUser } from '../services/authService';
import * as financeService from '../services/financeService';
import FileUpload from '../components/FileUpload';
import './Dashboard.css';

function Dashboard() {
  const [activeTab, setActiveTab] = useState('transactions');
  const [showUpload, setShowUpload] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [data, setData] = useState({
    transactions: [],
    income: [],
    incomeSummary: null,
    expenses: [],
    expensesSummary: null,
    networth: null
  });

  const navigate = useNavigate();

  useEffect(() => {
    fetchTabData(activeTab);
  }, [activeTab]);

  const fetchTabData = async (tab) => {
    setLoading(true);
    setError(null);
    try {
      let result;
      switch (tab) {
        case 'transactions':
          result = await financeService.getTransactions();
          setData(prev => ({ ...prev, transactions: result.data || [] }));
          break;
        case 'income':
          const incomeData = await financeService.getIncome();
          const incomeSummary = await financeService.getIncomeSummary();
          setData(prev => ({
            ...prev,
            income: incomeData.data || [],
            incomeSummary: incomeSummary.data
          }));
          break;
        case 'expenses':
          const expensesData = await financeService.getExpenses();
          const expensesSummary = await financeService.getExpensesSummary();
          setData(prev => ({
            ...prev,
            expenses: expensesData.data || [],
            expensesSummary: expensesSummary.data
          }));
          break;
        case 'networth':
          result = await financeService.getNetWorth();
          setData(prev => ({ ...prev, networth: result.data }));
          break;
        default:
          break;
      }
    } catch (err) {
      console.error(`Error fetching ${tab} data:`, err);
      setError(`Failed to load ${tab} data. Please try again later.`);
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

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(amount);
  };

  const renderLoading = () => (
    <div className="loading-state">
      <Loader2 className="animate-spin" size={48} color="#667eea" />
      <p>Loading your financial data...</p>
    </div>
  );

  const renderError = () => (
    <div className="error-state">
      <AlertCircle size={48} />
      <p>{error}</p>
      <button onClick={() => fetchTabData(activeTab)} className="btn-logout" style={{marginTop: '20px'}}>
        Retry
      </button>
    </div>
  );

  const renderTransactions = () => {
    if (data.transactions.length === 0) {
      return (
        <div className="placeholder-content">
          <List size={64} color="#ccc" />
          <p>No transactions to display yet. Upload a bank statement to get started.</p>
        </div>
      );
    }

    return (
      <div className="data-table-container">
        <table className="data-table">
          <thead>
            <tr>
              <th>Date</th>
              <th>Description</th>
              <th>Category</th>
              <th>Merchant</th>
              <th className="amount-cell">Amount</th>
            </tr>
          </thead>
          <tbody>
            {data.transactions.map(txn => (
              <tr key={txn.id}>
                <td>{txn.date}</td>
                <td>{txn.description}</td>
                <td>{txn.category}</td>
                <td>{txn.merchant}</td>
                <td className={`amount-cell ${txn.amount < 0 ? 'amount-negative' : 'amount-positive'}`}>
                  {formatCurrency(txn.amount)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  };

  const renderIncome = () => {
    if (data.income.length === 0) {
      return (
        <div className="placeholder-content">
          <TrendingUp size={64} color="#4ade80" />
          <p>Upload pay stubs or other income documents to see your income analysis.</p>
        </div>
      );
    }

    return (
      <>
        {data.incomeSummary && (
          <div className="summary-grid">
            <div className="summary-card">
              <h3>Total Income</h3>
              <div className="summary-value amount-positive">
                {formatCurrency(data.incomeSummary.totalIncome)}
              </div>
            </div>
            <div className="summary-card">
              <h3>Avg Monthly</h3>
              <div className="summary-value">
                {formatCurrency(data.incomeSummary.averageMonthly)}
              </div>
            </div>
          </div>
        )}
        <div className="data-table-container">
          <table className="data-table">
            <thead>
              <tr>
                <th>Date</th>
                <th>Source</th>
                <th>Employer</th>
                <th className="amount-cell">Tax Withheld</th>
                <th className="amount-cell">Amount</th>
              </tr>
            </thead>
            <tbody>
              {data.income.map(inc => (
                <tr key={inc.id}>
                  <td>{inc.date}</td>
                  <td>{inc.source}</td>
                  <td>{inc.employer}</td>
                  <td className="amount-cell">{formatCurrency(inc.taxWithheld)}</td>
                  <td className="amount-cell amount-positive">{formatCurrency(inc.amount)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </>
    );
  };

  const renderExpenses = () => {
    if (data.expenses.length === 0) {
      return (
        <div className="placeholder-content">
          <TrendingDown size={64} color="#f87171" />
          <p>Your expense breakdown will be displayed here once you upload statements.</p>
        </div>
      );
    }

    return (
      <>
        {data.expensesSummary && (
          <div className="summary-grid">
            <div className="summary-card">
              <h3>Total Expenses</h3>
              <div className="summary-value amount-negative">
                {formatCurrency(data.expensesSummary.totalExpenses)}
              </div>
            </div>
            <div className="summary-card">
              <h3>Avg Monthly</h3>
              <div className="summary-value">
                {formatCurrency(data.expensesSummary.averageMonthly)}
              </div>
            </div>
          </div>
        )}
        <div className="data-table-container">
          <table className="data-table">
            <thead>
              <tr>
                <th>Date</th>
                <th>Description</th>
                <th>Category</th>
                <th>Merchant</th>
                <th className="amount-cell">Amount</th>
              </tr>
            </thead>
            <tbody>
              {data.expenses.map(exp => (
                <tr key={exp.id}>
                  <td>{exp.date}</td>
                  <td>{exp.description}</td>
                  <td>{exp.category}</td>
                  <td>{exp.merchant}</td>
                  <td className="amount-cell amount-negative">{formatCurrency(exp.amount)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </>
    );
  };

  const renderNetWorth = () => {
    if (!data.networth) {
      return (
        <div className="placeholder-content">
          <DollarSign size={64} color="#fbbf24" />
          <p>Your net worth calculation will appear here based on your financial data.</p>
        </div>
      );
    }

    const { breakdown } = data.networth;

    return (
      <>
        <div className="summary-grid">
          <div className="summary-card">
            <h3>Total Assets</h3>
            <div className="summary-value amount-positive">
              {formatCurrency(data.networth.totalAssets)}
            </div>
          </div>
          <div className="summary-card">
            <h3>Total Liabilities</h3>
            <div className="summary-value amount-negative">
              {formatCurrency(data.networth.totalLiabilities)}
            </div>
          </div>
          <div className="summary-card" style={{borderColor: '#667eea', borderWidth: '2px'}}>
            <h3>Current Net Worth</h3>
            <div className="summary-value" style={{color: '#667eea'}}>
              {formatCurrency(data.networth.netWorth)}
            </div>
          </div>
        </div>

        <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '30px', marginTop: '30px'}}>
          <div>
            <h3>Assets Breakdown</h3>
            <ul style={{listStyle: 'none', padding: 0}}>
              {Object.entries(breakdown.assets).map(([key, val]) => (
                <li key={key} style={{display: 'flex', justifyContent: 'space-between', padding: '10px 0', borderBottom: '1px solid #f3f4f6'}}>
                  <span style={{textTransform: 'capitalize'}}>{key}</span>
                  <span className="amount-positive">{formatCurrency(val)}</span>
                </li>
              ))}
            </ul>
          </div>
          <div>
            <h3>Liabilities Breakdown</h3>
            <ul style={{listStyle: 'none', padding: 0}}>
              {Object.entries(breakdown.liabilities).map(([key, val]) => (
                <li key={key} style={{display: 'flex', justifyContent: 'space-between', padding: '10px 0', borderBottom: '1px solid #f3f4f6'}}>
                  <span style={{textTransform: 'capitalize'}}>{key}</span>
                  <span className="amount-negative">{formatCurrency(val)}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </>
    );
  };

  const renderTabContent = () => {
    if (loading) return renderLoading();
    if (error) return renderError();

    switch (activeTab) {
      case 'transactions':
        return (
          <div className="tab-content">
            <h2>Transactions</h2>
            <p>Your transaction history fetched from the Finance API.</p>
            {renderTransactions()}
          </div>
        );
      case 'income':
        return (
          <div className="tab-content">
            <h2>Income</h2>
            <p>Track your income sources and trends.</p>
            {renderIncome()}
          </div>
        );
      case 'expenses':
        return (
          <div className="tab-content">
            <h2>Expenses</h2>
            <p>Monitor your spending patterns and categories.</p>
            {renderExpenses()}
          </div>
        );
      case 'networth':
        return (
          <div className="tab-content">
            <h2>Net Worth</h2>
            <p>View your estimated net worth over time.</p>
            {renderNetWorth()}
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

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { signOut } from 'aws-amplify/auth';
import { 
  LogOut, 
  TrendingUp, 
  TrendingDown, 
  DollarSign, 
  BarChart3,
  Upload
} from 'lucide-react';
import FileUpload from '../components/FileUpload';
import './Dashboard.css';

const Dashboard = () => {
  const [activeTab, setActiveTab] = useState('transactions');
  const [showUploadModal, setShowUploadModal] = useState(false);
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      if (process.env.REACT_APP_USER_POOL_ID) {
        await signOut();
      }
      // Always clear local storage for both demo and real mode
      localStorage.removeItem('isAuthenticated');
      localStorage.removeItem('username');
      navigate('/');
    } catch (error) {
      console.error('Error signing out:', error);
      // Force logout even if there's an error
      localStorage.removeItem('isAuthenticated');
      localStorage.removeItem('username');
      navigate('/');
    }
  };

  const tabs = [
    { id: 'transactions', label: 'Transactions', icon: <BarChart3 size={20} /> },
    { id: 'income', label: 'Income', icon: <TrendingUp size={20} /> },
    { id: 'expenses', label: 'Expenses', icon: <TrendingDown size={20} /> },
    { id: 'networth', label: 'Net Worth', icon: <DollarSign size={20} /> },
  ];

  const renderTabContent = () => {
    switch (activeTab) {
      case 'transactions':
        return (
          <div className="tab-content-wrapper">
            <h3>Recent Transactions</h3>
            <p className="text-muted">Upload your bank statements to view transactions here.</p>
            <div className="empty-state">
              <BarChart3 size={64} className="empty-state-icon" />
              <p>No transactions yet. Upload a file to get started.</p>
              <button 
                className="btn btn-primary"
                onClick={() => setShowUploadModal(true)}
              >
                <Upload size={18} />
                Upload File
              </button>
            </div>
          </div>
        );
      
      case 'income':
        return (
          <div className="tab-content-wrapper">
            <h3>Income</h3>
            <p className="text-muted">Track your income sources and amounts.</p>
            <div className="empty-state">
              <TrendingUp size={64} className="empty-state-icon" />
              <p>No income data available. Upload pay stubs to track income.</p>
            </div>
          </div>
        );
      
      case 'expenses':
        return (
          <div className="tab-content-wrapper">
            <h3>Expenses</h3>
            <p className="text-muted">Monitor your spending and expense categories.</p>
            <div className="empty-state">
              <TrendingDown size={64} className="empty-state-icon" />
              <p>No expense data available. Upload statements to track expenses.</p>
            </div>
          </div>
        );
      
      case 'networth':
        return (
          <div className="tab-content-wrapper">
            <h3>Net Worth</h3>
            <p className="text-muted">View your estimated net worth over time.</p>
            <div className="empty-state">
              <DollarSign size={64} className="empty-state-icon" />
              <p>Net worth calculation requires transaction data.</p>
            </div>
          </div>
        );
      
      default:
        return null;
    }
  };

  return (
    <div className="dashboard-container">
      {/* Header */}
      <header className="dashboard-header">
        <div className="header-content">
          <h1>Personal Finance Dashboard</h1>
          <div className="header-actions">
            <button 
              className="btn btn-upload"
              onClick={() => setShowUploadModal(true)}
            >
              <Upload size={18} />
              Upload File
            </button>
            <button 
              className="btn btn-logout"
              onClick={handleLogout}
            >
              <LogOut size={18} />
              Log Out
            </button>
          </div>
        </div>
      </header>

      {/* Tabs Navigation */}
      <div className="tabs-container">
        <div className="tabs-wrapper">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              className={`tab-button ${activeTab === tab.id ? 'active' : ''}`}
              onClick={() => setActiveTab(tab.id)}
            >
              {tab.icon}
              <span>{tab.label}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Main Content */}
      <main className="dashboard-main">
        <div className="dashboard-content">
          {renderTabContent()}
        </div>
      </main>

      {/* File Upload Modal */}
      {showUploadModal && (
        <FileUpload onClose={() => setShowUploadModal(false)} />
      )}
    </div>
  );
};

export default Dashboard;

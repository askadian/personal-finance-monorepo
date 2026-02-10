import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  LogOut, 
  Upload, 
  TrendingUp, 
  TrendingDown, 
  List, 
  DollarSign 
} from 'lucide-react';
import FileUpload from '../components/FileUpload';
import './Dashboard.css';

function Dashboard() {
  const [activeTab, setActiveTab] = useState('transactions');
  const [showUpload, setShowUpload] = useState(false);
  const navigate = useNavigate();

  const handleLogout = () => {
    // Placeholder logout logic
    console.log('User logged out');
    navigate('/');
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
            <h2>Transactions</h2>
            <p>Your transaction history will appear here.</p>
            <div className="placeholder-content">
              <List size={64} color="#ccc" />
              <p>No transactions to display yet. Upload a bank statement to get started.</p>
            </div>
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

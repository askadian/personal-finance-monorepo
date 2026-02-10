import React, { useState } from 'react';
import { X, Upload, File } from 'lucide-react';
import './FileUpload.css';

function FileUpload({ onClose }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [fileType, setFileType] = useState('');

  const fileTypes = [
    'Bank Statement',
    'Pay Stub',
    '1099-INT',
    '1099-DIV',
    'W-2',
    'Credit Card Statement',
    'Investment Statement',
    'Other'
  ];

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedFile(file);
    }
  };

  const handleUpload = () => {
    if (!selectedFile || !fileType) {
      alert('Please select a file and file type');
      return;
    }

    // Placeholder upload logic
    console.log('Uploading file:', {
      file: selectedFile.name,
      type: fileType,
      size: selectedFile.size
    });
    
    alert(`File "${selectedFile.name}" would be uploaded as "${fileType}". (Placeholder functionality)`);
    
    // Reset and close
    setSelectedFile(null);
    setFileType('');
    onClose();
  };

  return (
    <div className="upload-overlay" onClick={onClose}>
      <div className="upload-modal" onClick={(e) => e.stopPropagation()}>
        <div className="upload-header">
          <h2>Upload Financial Document</h2>
          <button className="btn-close" onClick={onClose}>
            <X size={24} />
          </button>
        </div>

        <div className="upload-body">
          <div className="file-select-area">
            <input
              type="file"
              id="file-input"
              onChange={handleFileSelect}
              accept=".pdf,.csv,.xlsx,.xls"
              style={{ display: 'none' }}
            />
            <label htmlFor="file-input" className="file-select-label">
              {selectedFile ? (
                <div className="file-selected">
                  <File size={48} color="#667eea" />
                  <p className="file-name">{selectedFile.name}</p>
                  <p className="file-size">
                    {(selectedFile.size / 1024).toFixed(2)} KB
                  </p>
                </div>
              ) : (
                <div className="file-placeholder">
                  <Upload size={48} color="#ccc" />
                  <p>Click to select a file</p>
                  <p className="file-hint">Supported formats: PDF, CSV, XLSX, XLS</p>
                </div>
              )}
            </label>
          </div>

          <div className="file-type-select">
            <label htmlFor="file-type">File Type</label>
            <select
              id="file-type"
              value={fileType}
              onChange={(e) => setFileType(e.target.value)}
            >
              <option value="">Select file type...</option>
              {fileTypes.map(type => (
                <option key={type} value={type}>
                  {type}
                </option>
              ))}
            </select>
          </div>
        </div>

        <div className="upload-footer">
          <button className="btn-cancel" onClick={onClose}>
            Cancel
          </button>
          <button 
            className="btn-upload-submit" 
            onClick={handleUpload}
            disabled={!selectedFile || !fileType}
          >
            Upload
          </button>
        </div>
      </div>
    </div>
  );
}

export default FileUpload;

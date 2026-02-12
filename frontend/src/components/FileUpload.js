import React, { useState } from 'react';
import { X, Upload, File, CheckCircle, AlertCircle } from 'lucide-react';
import './FileUpload.css';
import { uploadFile, validateFile } from '../services/uploadService';

function FileUpload({ onClose }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [fileType, setFileType] = useState('');
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [uploadStatus, setUploadStatus] = useState(null); // 'success', 'error', or null
  const [errorMessage, setErrorMessage] = useState('');

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
      // Validate file immediately
      const validation = validateFile(file);
      if (!validation.valid) {
        setErrorMessage(validation.error);
        setUploadStatus('error');
        return;
      }
      setSelectedFile(file);
      setErrorMessage('');
      setUploadStatus(null);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile || !fileType) {
      setErrorMessage('Please select a file and file type');
      setUploadStatus('error');
      return;
    }

    setUploading(true);
    setUploadProgress(0);
    setUploadStatus(null);
    setErrorMessage('');

    try {
      // Upload file to S3
      await uploadFile(selectedFile, fileType, (progress) => {
        setUploadProgress(Math.round(progress));
      });

      // Success
      setUploadStatus('success');
      setUploadProgress(100);
      
      // Auto-close after success
      setTimeout(() => {
        setSelectedFile(null);
        setFileType('');
        setUploading(false);
        setUploadProgress(0);
        setUploadStatus(null);
        onClose();
      }, 2000);

    } catch (error) {
      // Error
      console.error('Upload failed:', error);
      setUploadStatus('error');
      setErrorMessage(error.message || 'Failed to upload file. Please try again.');
      setUploading(false);
      setUploadProgress(0);
    }
  };

  const handleRetry = () => {
    setUploadStatus(null);
    setErrorMessage('');
    setUploadProgress(0);
  };

  const handleClose = () => {
    if (!uploading) {
      onClose();
    }
  };

  return (
    <div className="upload-overlay" onClick={handleClose}>
      <div className="upload-modal" onClick={(e) => e.stopPropagation()}>
        <div className="upload-header">
          <h2>Upload Financial Document</h2>
          <button className="btn-close" onClick={handleClose} disabled={uploading}>
            <X size={24} />
          </button>
        </div>

        <div className="upload-body">
          {/* Success Message */}
          {uploadStatus === 'success' && (
            <div className="upload-message upload-success">
              <CheckCircle size={48} color="#10b981" />
              <h3>Upload Successful!</h3>
              <p>Your file has been uploaded and will be processed shortly.</p>
            </div>
          )}

          {/* Error Message */}
          {uploadStatus === 'error' && (
            <div className="upload-message upload-error">
              <AlertCircle size={48} color="#ef4444" />
              <h3>Upload Failed</h3>
              <p>{errorMessage}</p>
              <button className="btn-retry" onClick={handleRetry}>
                Try Again
              </button>
            </div>
          )}

          {/* Upload Form */}
          {!uploadStatus && (
            <>
              <div className="file-select-area">
                <input
                  type="file"
                  id="file-input"
                  onChange={handleFileSelect}
                  accept=".pdf,.csv,.xlsx,.xls"
                  style={{ display: 'none' }}
                  disabled={uploading}
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
                      <p className="file-hint">Maximum size: 10MB</p>
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
                  disabled={uploading}
                >
                  <option value="">Select file type...</option>
                  {fileTypes.map(type => (
                    <option key={type} value={type}>
                      {type}
                    </option>
                  ))}
                </select>
              </div>

              {/* Upload Progress */}
              {uploading && (
                <div className="upload-progress">
                  <div className="progress-bar">
                    <div 
                      className="progress-fill" 
                      style={{ width: `${uploadProgress}%` }}
                    />
                  </div>
                  <p className="progress-text">Uploading... {uploadProgress}%</p>
                </div>
              )}
            </>
          )}
        </div>

        <div className="upload-footer">
          {!uploadStatus && (
            <>
              <button 
                className="btn-cancel" 
                onClick={handleClose}
                disabled={uploading}
              >
                Cancel
              </button>
              <button 
                className="btn-upload-submit" 
                onClick={handleUpload}
                disabled={!selectedFile || !fileType || uploading}
              >
                {uploading ? 'Uploading...' : 'Upload'}
              </button>
            </>
          )}
          {uploadStatus === 'success' && (
            <button className="btn-close-success" onClick={handleClose}>
              Close
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

export default FileUpload;

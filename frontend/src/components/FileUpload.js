import React, { useState, useRef } from 'react';
import { X, Upload, File } from 'lucide-react';
import './FileUpload.css';

const FileUpload = ({ onClose }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [fileType, setFileType] = useState('');
  const [uploading, setUploading] = useState(false);
  const [uploadSuccess, setUploadSuccess] = useState(false);
  const fileInputRef = useRef(null);

  const fileTypes = [
    { value: 'bank_statement', label: 'Bank Statement' },
    { value: 'pay_stub', label: 'Pay Stub' },
    { value: '1099_int', label: '1099-INT' },
    { value: '1099_div', label: '1099-DIV' },
    { value: 'w2', label: 'W-2' },
    { value: 'credit_card', label: 'Credit Card Statement' },
    { value: 'investment', label: 'Investment Statement' },
    { value: 'other', label: 'Other' },
  ];

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      // Validate file type
      const validTypes = ['application/pdf', 'text/csv', 'application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'];
      if (!validTypes.includes(file.type)) {
        alert('Please select a valid file type (PDF, CSV, or Excel)');
        return;
      }
      
      // Validate file size (max 10MB)
      if (file.size > 10 * 1024 * 1024) {
        alert('File size must be less than 10MB');
        return;
      }
      
      setSelectedFile(file);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile || !fileType) {
      alert('Please select both a file and file type');
      return;
    }

    setUploading(true);
    
    try {
      // Simulate upload - In production, this would use AWS S3 presigned URLs
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      console.log('Uploading file:', {
        name: selectedFile.name,
        type: fileType,
        size: selectedFile.size,
      });
      
      setUploadSuccess(true);
      
      // Reset after success
      setTimeout(() => {
        setSelectedFile(null);
        setFileType('');
        setUploadSuccess(false);
        onClose();
      }, 2000);
      
    } catch (error) {
      console.error('Upload error:', error);
      alert('Failed to upload file. Please try again.');
    } finally {
      setUploading(false);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    
    const file = e.dataTransfer.files[0];
    if (file) {
      const fakeEvent = {
        target: {
          files: [file]
        }
      };
      handleFileSelect(fakeEvent);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h3>Upload Financial Document</h3>
          <button className="close-button" onClick={onClose}>
            <X size={24} />
          </button>
        </div>

        <div className="modal-body">
          {uploadSuccess ? (
            <div className="success-message">
              <div className="success-icon">✓</div>
              <h4>Upload Successful!</h4>
              <p>Your file has been uploaded and is being processed.</p>
            </div>
          ) : (
            <>
              {/* File Type Selection */}
              <div className="form-group">
                <label htmlFor="fileType">Document Type *</label>
                <select
                  id="fileType"
                  className="form-control"
                  value={fileType}
                  onChange={(e) => setFileType(e.target.value)}
                >
                  <option value="">Select document type...</option>
                  {fileTypes.map((type) => (
                    <option key={type.value} value={type.value}>
                      {type.label}
                    </option>
                  ))}
                </select>
              </div>

              {/* File Upload Area */}
              <div 
                className="upload-area"
                onDragOver={handleDragOver}
                onDrop={handleDrop}
                onClick={() => fileInputRef.current?.click()}
              >
                <input
                  ref={fileInputRef}
                  type="file"
                  accept=".pdf,.csv,.xls,.xlsx"
                  onChange={handleFileSelect}
                  style={{ display: 'none' }}
                />
                
                {selectedFile ? (
                  <div className="file-info">
                    <File size={48} className="file-icon" />
                    <p className="file-name">{selectedFile.name}</p>
                    <p className="file-size">
                      {(selectedFile.size / 1024).toFixed(2)} KB
                    </p>
                  </div>
                ) : (
                  <div className="upload-prompt">
                    <Upload size={48} className="upload-icon" />
                    <p>Drag and drop your file here</p>
                    <p className="upload-hint">or click to browse</p>
                    <p className="file-types">Supported: PDF, CSV, Excel (max 10MB)</p>
                  </div>
                )}
              </div>

              {/* Action Buttons */}
              <div className="modal-actions">
                <button 
                  className="btn btn-secondary"
                  onClick={onClose}
                  disabled={uploading}
                >
                  Cancel
                </button>
                <button 
                  className="btn btn-primary"
                  onClick={handleUpload}
                  disabled={!selectedFile || !fileType || uploading}
                >
                  {uploading ? 'Uploading...' : 'Upload'}
                </button>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default FileUpload;

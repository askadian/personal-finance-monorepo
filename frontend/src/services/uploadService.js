/**
 * Upload Service
 * 
 * This service handles file uploads to Amazon S3 using presigned URLs.
 * Files are uploaded directly to S3 with client-side validation and progress tracking.
 */

import { fetchAuthSession } from 'aws-amplify/auth';

/**
 * Generate a unique file key for S3 storage
 * @param {string} userId - The user's unique identifier
 * @param {string} fileName - The original file name
 * @param {string} fileType - The document type (e.g., 'Bank Statement', 'Pay Stub')
 * @returns {string} - S3 object key
 */
const generateFileKey = (userId, fileName, fileType) => {
  const timestamp = Date.now();
  const sanitizedFileName = fileName.replace(/[^a-zA-Z0-9.-]/g, '_');
  const fileTypeSlug = fileType.toLowerCase().replace(/\s+/g, '-');
  
  return `users/${userId}/${fileTypeSlug}/${timestamp}-${sanitizedFileName}`;
};

/**
 * Get presigned URL from API Gateway
 * @param {string} fileKey - S3 object key
 * @param {string} contentType - File MIME type
 * @returns {Promise<object>} - Presigned URL response
 */
const getPresignedUrl = async (fileKey, contentType) => {
  try {
    // Get the current auth session to retrieve access token
    const session = await fetchAuthSession();
    const idToken = session.tokens?.idToken?.toString();
    
    if (!idToken) {
      throw new Error('User not authenticated');
    }

    const apiEndpoint = process.env.REACT_APP_UPLOAD_API_URL;
    
    if (!apiEndpoint) {
      throw new Error('Upload API endpoint not configured. Please check your .env.local file.');
    }
    
    // Make request to API Gateway to get presigned URL
    const response = await fetch(`${apiEndpoint}/v1/upload-url`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${idToken}`
      },
      body: JSON.stringify({
        fileKey,
        contentType,
        fileName: fileKey.split('/').pop()
      })
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error?.message || 'Failed to get upload URL');
    }

    return await response.json();
  } catch (error) {
    console.error('Error getting presigned URL:', error);
    throw error;
  }
};

/**
 * Upload file directly to S3 using presigned URL
 * @param {string} presignedUrl - Presigned S3 URL
 * @param {File} file - File object to upload
 * @param {Function} onProgress - Progress callback function
 * @returns {Promise<void>}
 */
const uploadToS3 = async (presignedUrl, file, onProgress) => {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();

    // Track upload progress
    if (onProgress) {
      xhr.upload.addEventListener('progress', (event) => {
        if (event.lengthComputable) {
          const percentComplete = (event.loaded / event.total) * 100;
          onProgress(percentComplete);
        }
      });
    }

    xhr.addEventListener('load', () => {
      if (xhr.status >= 200 && xhr.status < 300) {
        resolve();
      } else {
        reject(new Error(`Upload failed with status ${xhr.status}`));
      }
    });

    xhr.addEventListener('error', () => {
      reject(new Error('Network error during upload'));
    });

    xhr.addEventListener('abort', () => {
      reject(new Error('Upload aborted'));
    });

    xhr.open('PUT', presignedUrl);
    xhr.setRequestHeader('Content-Type', file.type);
    xhr.send(file);
  });
};

/**
 * Validate file before upload
 * @param {File} file - File to validate
 * @returns {object} - Validation result
 */
export const validateFile = (file) => {
  const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB
  const ALLOWED_TYPES = [
    'application/pdf',
    'text/csv',
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
  ];

  if (!file) {
    return { valid: false, error: 'No file selected' };
  }

  if (file.size > MAX_FILE_SIZE) {
    return { 
      valid: false, 
      error: `File size exceeds ${MAX_FILE_SIZE / (1024 * 1024)}MB limit` 
    };
  }

  if (!ALLOWED_TYPES.includes(file.type)) {
    return { 
      valid: false, 
      error: 'Invalid file type. Only PDF, CSV, and Excel files are allowed' 
    };
  }

  return { valid: true };
};

/**
 * Main upload function
 * @param {File} file - File to upload
 * @param {string} fileType - Document type (e.g., 'Bank Statement')
 * @param {Function} onProgress - Progress callback (optional)
 * @returns {Promise<object>} - Upload result
 */
export const uploadFile = async (file, fileType, onProgress = null) => {
  try {
    // Validate file
    const validation = validateFile(file);
    if (!validation.valid) {
      throw new Error(validation.error);
    }

    // Get current user
    const session = await fetchAuthSession();
    const userId = session.tokens?.idToken?.payload?.sub;
    
    if (!userId) {
      throw new Error('User not authenticated');
    }

    // Generate S3 key
    const fileKey = generateFileKey(userId, file.name, fileType);

    // Get presigned URL from backend API
    const { uploadUrl, fileId } = await getPresignedUrl(fileKey, file.type);

    // Upload file directly to S3
    await uploadToS3(uploadUrl, file, onProgress);
    
    return {
      success: true,
      fileId,
      fileKey,
      message: 'File uploaded successfully'
    };

  } catch (error) {
    console.error('Upload failed:', error);
    throw error;
  }
};

/**
 * Get upload configuration status
 * @returns {object} - Configuration status
 */
export const getUploadConfig = () => {
  const apiEndpoint = process.env.REACT_APP_UPLOAD_API_URL;
  const bucketName = process.env.REACT_APP_S3_BUCKET_NAME;
  const region = process.env.REACT_APP_AWS_REGION;

  return {
    configured: !!(apiEndpoint && bucketName && region),
    apiEndpoint,
    bucketName,
    region
  };
};

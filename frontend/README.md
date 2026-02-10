# Personal Finance Tracker - Frontend

This is the React-based frontend for the Personal Finance Tracker application.

## Features

- **Sign In Page**: User authentication interface with email/username and password fields
- **Forgot Password**: Password reset functionality (placeholder for AWS Cognito integration)
- **Dashboard**: Main application interface with multiple tabs
  - Transactions: View transaction history
  - Income: Track income sources and trends
  - Expenses: Monitor spending patterns
  - Net Worth: View estimated net worth over time
- **File Upload**: Upload financial documents with type selection
  - Bank Statements
  - Pay Stubs
  - Tax Documents (1099-INT, 1099-DIV, W-2)
  - Credit Card Statements
  - Investment Statements
- **Logout**: Sign out functionality

## Tech Stack

- React 19.2.4
- React Router DOM 7.13.0
- Lucide React (for icons)
- CSS3 (for styling)

## Getting Started

### Prerequisites

- Node.js (v14 or higher)
- npm or yarn

### Installation

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

   **Note:** If you encounter permission errors or other installation issues, see the [Troubleshooting Guide](../TROUBLESHOOTING.md).

### Running the Development Server

Start the development server:
```bash
npm start
```

The application will open in your browser at [http://localhost:3000](http://localhost:3000).

### Building for Production

Create an optimized production build:
```bash
npm run build
```

The build artifacts will be stored in the `build/` directory.

### Running Tests

Run the test suite:
```bash
npm test
```

## Project Structure

```
frontend/
├── public/
│   ├── favicon.ico
│   └── index.html
├── src/
│   ├── components/
│   │   ├── FileUpload.js      # File upload modal component
│   │   └── FileUpload.css
│   ├── pages/
│   │   ├── SignIn.js           # Sign-in page
│   │   ├── SignIn.css
│   │   ├── Dashboard.js        # Main dashboard with tabs
│   │   └── Dashboard.css
│   ├── App.js                  # Main app component with routing
│   ├── App.css                 # Global styles
│   └── index.js                # Application entry point
├── package.json
└── .gitignore
```

## Current Implementation

This is a **UI-only implementation** with placeholder logic for:
- User authentication
- Password reset
- File uploads

These features are designed to be integrated with AWS services in future updates:
- AWS Cognito for authentication
- S3 for file storage
- Lambda for backend processing
- DynamoDB for data storage

## Usage

1. **Sign In**: Enter any email/username and password, then click "Sign In" to access the dashboard
2. **Navigate Tabs**: Click on any tab (Transactions, Income, Expenses, Net Worth) to view different sections
3. **Upload Files**: Click the "Upload File" button, select a file, choose the file type, and click "Upload"
4. **Logout**: Click the "Logout" button to return to the sign-in page

## Troubleshooting

If you encounter issues during installation or running the application, please refer to the [Troubleshooting Guide](../TROUBLESHOOTING.md) for common solutions including:

- npm permission errors (EACCES)
- react-scripts: command not found
- npm cache issues
- Node.js version requirements

## Future Enhancements

- Integration with AWS Cognito for real authentication
- Connect to backend API for data persistence
- Implement actual file upload to S3
- Add data visualization charts
- Implement transaction filtering and search
- Add user profile management

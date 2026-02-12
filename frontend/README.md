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

This implementation includes:
- **AWS Cognito Integration**: Real authentication using AWS Cognito User Pool
- **Protected Routes**: Dashboard requires authentication to access
- **Session Management**: JWT token-based authentication
- **Error Handling**: User-friendly error messages for authentication failures

### Authentication Setup

Before using the authentication features, you need to configure AWS Cognito:
1. Create an AWS Cognito User Pool
2. Configure the App Client
3. Update the configuration in `src/aws-config.js`

See [COGNITO_SETUP.md](./COGNITO_SETUP.md) for detailed setup instructions.

### Placeholder Features

The following features still use placeholder logic:
- Password reset (to be implemented with Cognito forgot password flow)
- File uploads (to be integrated with S3)
- Data display (to be integrated with backend API)

These features are designed to be integrated with AWS services:
- S3 for file storage
- Lambda for backend processing
- DynamoDB for data storage
- API Gateway for REST API

## Usage

### Before First Use

Configure AWS Cognito by following the [COGNITO_SETUP.md](./COGNITO_SETUP.md) guide.

**Troubleshooting Login Issues?**
- If you see "SECRET_HASH was not received" error, see [IMPLEMENTATION_GUIDE.md](./IMPLEMENTATION_GUIDE.md)
- For other authentication issues, see [TROUBLESHOOTING.md](./TROUBLESHOOTING.md)

### Using the Application

1. **Sign In**: Enter your Cognito user credentials, then click "Sign In" to access the dashboard
2. **Navigate Tabs**: Click on any tab (Transactions, Income, Expenses, Net Worth) to view different sections
3. **Upload Files**: Click the "Upload File" button, select a file, choose the file type, and click "Upload"
4. **Logout**: Click the "Logout" button to sign out and return to the sign-in page

## Future Enhancements

- Implement password reset with Cognito forgot password flow
- Add user registration flow
- Connect to backend API for data persistence
- Implement actual file upload to S3
- Add data visualization charts
- Implement transaction filtering and search
- Add user profile management
- Enable MFA (Multi-Factor Authentication)

# Personal Finance Tracker - Frontend

React-based frontend application for the Personal Finance Tracker.

## Features

- **Authentication**: Secure sign-in with AWS Cognito (with demo mode fallback)
- **Dashboard**: Multi-tab interface for viewing financial data
  - Transactions
  - Income
  - Expenses
  - Net Worth
- **File Upload**: Upload financial documents (Bank Statements, Pay Stubs, Tax Documents, etc.)
- **Responsive Design**: Mobile-friendly interface

## Tech Stack

- React 18
- React Router DOM
- AWS Amplify
- Bootstrap 5
- Lucide React (Icons)

## Getting Started

### Prerequisites

- Node.js 14+ and npm

### Installation

1. Install dependencies:
```bash
npm install
```

2. Configure environment variables:
```bash
cp .env.example .env
```

Update `.env` with your AWS Cognito configuration (after infrastructure deployment).

### Development

Start the development server:
```bash
npm start
```

The application will open at [http://localhost:3000](http://localhost:3000).

### Demo Mode

If AWS Cognito is not configured, the application runs in demo mode:
- Any username/password combination will allow sign-in
- Authentication state is stored in localStorage
- File uploads are simulated

### Build

Create a production build:
```bash
npm run build
```

The build output will be in the `build/` directory.

### Test

Run the test suite:
```bash
npm test
```

## Project Structure

```
src/
├── components/
│   ├── FileUpload.js       # File upload modal component
│   ├── FileUpload.css
│   └── ProtectedRoute.js   # Route protection wrapper
├── pages/
│   ├── SignIn.js           # Sign-in page
│   ├── SignIn.css
│   ├── Dashboard.js        # Main dashboard with tabs
│   └── Dashboard.css
├── aws-exports.js          # AWS Amplify configuration
├── App.js                  # Main app component with routing
├── App.css
├── index.js                # Entry point
└── index.css
```

## Available Scripts

### `npm start`
Runs the app in development mode at [http://localhost:3000](http://localhost:3000).

### `npm test`
Launches the test runner in interactive watch mode.

### `npm run build`
Builds the app for production to the `build` folder.

### `npm run eject`
**Note: this is a one-way operation. Once you `eject`, you can't go back!**

## Features in Detail

### Sign In Page
- Username/email and password input
- Password reset link
- AWS Cognito integration
- Automatic redirect to dashboard on successful login

### Dashboard
- Header with app title and action buttons
- Tab navigation for different views
- Upload button accessible from header
- Log out functionality

### File Upload
- Drag-and-drop file upload
- File type selection (Bank Statement, Pay Stub, 1099-INT, etc.)
- File validation (type and size)
- Upload progress indication
- Success confirmation

## Deployment

The frontend is designed to be hosted on AWS S3 and served via CloudFront. See the main repository README and DEPLOYMENT.md for deployment instructions.

## Security

- Protected routes require authentication
- AWS Cognito for user management
- Secure file uploads via S3 presigned URLs (when configured)
- No sensitive data stored in localStorage (demo mode only)

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

## License

See the main repository LICENSE file.

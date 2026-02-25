# Personal Finance Tracker - Frontend

React frontend application for the Personal Finance Tracker.

## Quick Start

### Prerequisites
- Node.js 14+ 
- npm or yarn

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/askadian/personal-finance-monorepo.git
   cd personal-finance-monorepo/frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Configure environment variables**
   
   Copy the example environment file:
   ```bash
   cp .env.example .env.local
   ```
   
   The `.env.local` file should already have the correct values. If not, update it with:
   ```
   REACT_APP_UPLOAD_API_URL=https://ffcijer5wl.execute-api.us-east-1.amazonaws.com/dev
   REACT_APP_FINANCE_API_URL=https://xyz123.execute-api.us-east-1.amazonaws.com
   REACT_APP_S3_BUCKET_NAME=personal-finance-uploads-dev
   REACT_APP_AWS_REGION=us-east-1
   ```

4. **Start the development server**
   ```bash
   npm start
   ```
   
   The app will open at [http://localhost:3000](http://localhost:3000)

## Features

- **Authentication**: AWS Cognito user authentication
- **File Upload**: Upload financial documents (bank statements, pay stubs, tax forms) directly to S3
- **Dashboard**: View transactions, income, expenses, and net worth
- **Protected Routes**: Authentication-required pages

## File Upload Architecture

The application uses a secure file upload flow:

1. User selects file in React frontend
2. Frontend requests presigned URL from API Gateway
3. API Gateway validates JWT token via Cognito authorizer
4. Lambda function generates presigned S3 URL (5-minute expiration)
5. Frontend uploads file directly to S3 using presigned URL
6. File stored in S3 with path: `users/{userId}/{file-type}/{timestamp}-{filename}`

### Supported File Types
- PDF documents
- CSV files
- Excel files (.xlsx, .xls)
- Max file size: 10MB

## Project Structure

```
frontend/
├── public/
│   ├── favicon.ico
│   └── index.html
├── src/
│   ├── components/
│   │   ├── FileUpload.js       # File upload modal component
│   │   ├── FileUpload.css
│   │   └── ProtectedRoute.js   # Authentication wrapper
│   ├── pages/
│   │   ├── SignIn.js            # Login page
│   │   ├── SignIn.css
│   │   ├── Dashboard.js         # Main dashboard
│   │   └── Dashboard.css
│   ├── services/
│   │   ├── authService.js       # AWS Cognito authentication
│   │   └── uploadService.js     # S3 file upload logic
│   ├── aws-config.js            # AWS Amplify configuration
│   ├── App.js                   # Main app with routing
│   ├── App.css
│   └── index.js                 # Entry point
├── .env.example                 # Environment variables template
├── .gitignore
├── package.json
└── README.md
```

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `REACT_APP_UPLOAD_API_URL` | Upload API Gateway endpoint URL | `https://{api-id}.execute-api.{region}.amazonaws.com/{stage}` |
| `REACT_APP_FINANCE_API_URL` | Finance API Gateway endpoint URL | `https://{api-id}.execute-api.{region}.amazonaws.com` |
| `REACT_APP_S3_BUCKET_NAME` | S3 bucket for file uploads | `personal-finance-uploads-dev` |
| `REACT_APP_AWS_REGION` | AWS region | `us-east-1` |

## AWS Resources

- **API Gateway**: `ffcijer5wl` (stage: `dev`)
- **S3 Bucket**: `personal-finance-uploads-dev`
- **Lambda**: `PersonalFinanceUploadUrl`
- **Cognito User Pool**: `us-east-1_ypJY5Q49F`
- **Cognito App Client**: `26g1835ki3plirj0dsfab38vqb`

## Troubleshooting

### "API endpoint not configured" error
- Make sure `.env.local` exists and has `REACT_APP_UPLOAD_API_URL` and `REACT_APP_FINANCE_API_URL` set
- Restart the dev server after creating/modifying `.env.local`

### CORS errors on file upload
- Verify API Gateway has OPTIONS method configured
- Check that S3 bucket CORS policy allows `PUT` from `localhost:3000`

### Authentication fails
- Check AWS Cognito user pool configuration
- Verify app client is configured as "Public client" (no secret)
- See `aws-config.js` for Cognito configuration

## Available Scripts

### `npm start`
Runs the app in development mode at [http://localhost:3000](http://localhost:3000)

### `npm test`
Launches the test runner in interactive watch mode

### `npm run build`
Builds the app for production to the `build/` folder

## License

MIT

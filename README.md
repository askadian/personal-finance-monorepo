# Personal Finance Monorepo

A cloud-native, secure personal finance tracker built with React, Python, and AWS.

## Architecture

<img width="814" height="603" alt="Monorepo drawio (2)" src="https://github.com/user-attachments/assets/0436a4dd-ee47-4281-8a02-bd6fe945797f" />


The application follows a modern serverless architecture:

1.  **Front End (React):** Hosted on S3 and distributed via CloudFront. Accessed via URL / custom domain.
2.  **Authentication (AWS Cognito):** Secure login and registration using Cognito Hosted UI.
3.  **File Upload (S3):** Statements (CSV/PDF) are uploaded directly to a secure S3 bucket using presigned URLs.
4.  **Processing (AWS Lambda):** An S3 trigger invokes a Python Lambda function to parse the uploaded financial statements, pay stubs, Tax documents etc.
5.  **Data Storage (Amazon DynamoDB):** Parsed transaction records are stored in DynamoDB, in a timeseries format.
6.  **API Layer (API Gateway):** A secure REST API (integrated with Cognito) allows the frontend to fetch processed records.
7.  **Dashboard:** A React-based UI that visualizes transactions, income, expenses, and estimated net worth.

## Project Structure

- `/frontend`: React application (JavaScript).
- `/backend`: Python Lambda functions for parsing and API handling.
- `/infra`: AWS CDK (Python) for infrastructure as code.
- `/api`: OpenAPI specifications and API collections (Postman & Bruno).
- `/security`: AWS security resources documentation (Cognito User Pools).
- `/.github/workflows`: GitHub Actions for automated CI/CD.

## Tech Stack

- **Languages:** Python (Backend/Infra), JavaScript (Frontend).
- **Frontend:** React, AWS Amplify, Bootstrap, Lucide Icons.
- **Backend:** AWS Lambda (Python 3.12), Boto3, PyPDF.
- **Database:** Amazon DynamoDB.
- **Infrastructure:** AWS CDK.
- **CI/CD:** GitHub Actions.

## API Documentation

The REST API specifications and collections are available in the `/api` directory:

- **OpenAPI 3.0 Specification**: Complete API definition in OpenAPI format
- **Postman Collection**: Importable collection with mock data and parameterized environments
- **Bruno Collection**: Git-friendly collection with mock examples

See [API Documentation](./api/README.md) for detailed usage instructions.

## Security Documentation

AWS security resources documentation is available in the `/security` directory:

- **Cognito User Pools**: Complete setup guide for authentication and user management
  - Manual setup instructions with step-by-step guides
  - Automation templates for IaC (CloudFormation, Terraform - coming soon)
  - Integration with API Gateway and frontend

See [Security Documentation](./security/cognito/README.md) for detailed setup instructions.

## Getting Started

Refer to [DEPLOYMENT.md](./DEPLOYMENT.md) for step-by-step instructions on how to deploy this stack to your AWS account.

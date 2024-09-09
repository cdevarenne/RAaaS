

## Functions

1. **PDF Processor** (`lambda/pdf-processor/index.py`): Extracts text from uploaded PDF files.
2. **Summarizer** (`lambda/summarizer/index.py`): Generates summaries from extracted text.

## Setup and Deployment

### Prerequisites

- AWS CLI installed and configured with appropriate permissions
- Python 3.8 or higher
- Node.js and npm (for packaging dependencies)

### Packaging Lambda Functions

1. Install dependencies:
   ```
   cd aws/lambda/pdf-processor
   pip install -r requirements.txt -t .
   cd ../summarizer
   pip install -r requirements.txt -t .
   ```

2. Create ZIP files for each function:
   ```
   cd ../pdf-processor
   zip -r ../../../pdf-processor.zip .
   cd ../summarizer
   zip -r ../../../summarizer.zip .
   ```

### Deploying Lambda Functions

The Lambda functions are deployed as part of the CloudFormation stack. If you need to update them individually:

1. Update the function code:
   ```
   aws lambda update-function-code --function-name raas-pdf-processor --zip-file fileb://pdf-processor.zip
   aws lambda update-function-code --function-name raas-summarizer --zip-file fileb://summarizer.zip
   ```

2. Update the function configuration if necessary:
   ```
   aws lambda update-function-configuration --function-name raas-pdf-processor --handler index.lambda_handler --runtime python3.8
   aws lambda update-function-configuration --function-name raas-summarizer --handler index.lambda_handler --runtime python3.8
   ```

## Testing Lambda Functions Locally

You can use the AWS SAM CLI to test the Lambda functions locally:

1. Install AWS SAM CLI
2. Create a `template.yaml` file in the `aws/` directory with the function definitions
3. Use `sam local invoke` to test each function:
   ```
   sam local invoke PDFProcessor -e events/s3-put.json
   sam local invoke Summarizer -e events/s3-put.json
   ```

Replace `events/s3-put.json` with a file containing a sample S3 event.

## Monitoring and Logs

You can view logs for the Lambda functions in AWS CloudWatch Logs. Each function will have its own log group:

- `/aws/lambda/raas-pdf-processor`
- `/aws/lambda/raas-summarizer`

Use the AWS Management Console or AWS CLI to access these logs.

## Troubleshooting

Common issues and their solutions:

1. **Function times out**: Increase the function timeout in the CloudFormation template or using the AWS CLI
2. **Out of memory error**: Increase the allocated memory for the function
3. **Permission issues**: Check the IAM role attached to the Lambda functions and ensure it has the necessary permissions

For any persistent issues, please refer to the CloudWatch Logs for detailed error messages and open an issue in the GitHub repository if needed.


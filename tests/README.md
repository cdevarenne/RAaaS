
## Prerequisites

Before running the tests, ensure you have the following installed:

- Python 3.8 or higher
- pip (Python package installer)

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/your-username/raas.git
   cd raas
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements-test.txt
   ```

## Running Unit Tests

To run the unit tests for the PDF processor and summarizer Lambda functions:

```
python -m unittest tests/unit/test_pdf_processor.py tests/unit/test_summarizer.py
```

## Running Integration Tests

Before running the integration tests, make sure you have:

1. Deployed the RAaaS stack to AWS
2. Updated the `tests/integration/test_raas_pipeline.py` file with your actual AWS resource names and API Gateway URL
3. Created a test user in your Cognito User Pool and updated the test credentials in the integration test file

Then, run the integration tests with:

```
python -m unittest tests/integration/test_raas_pipeline.py
```

## Adding New Tests

When adding new tests:

1. For unit tests, create new test files in the `tests/unit/` directory
2. For integration tests, add new test methods to `tests/integration/test_raas_pipeline.py` or create new files in the `tests/integration/` directory
3. Ensure all new test files are prefixed with `test_`
4. Update this README if you add any new dependencies or setup steps

## Troubleshooting

If you encounter any issues:

1. Ensure all required AWS resources are properly set up and accessible
2. Check that your AWS credentials are correctly configured
3. Verify that all dependencies are installed and up to date
4. Check the AWS CloudWatch logs for any errors in the Lambda functions

For any persistent issues, please open an issue in the GitHub repository.

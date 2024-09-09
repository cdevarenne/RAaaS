import unittest
import boto3
import time
import requests

class TestRaaSPipeline(unittest.TestCase):
    def setUp(self):
        self.s3 = boto3.client('s3')
        self.input_bucket = 'raas-input-pdfs'
        self.summaries_bucket = 'raas-summaries'
        self.api_url = 'https://your-api-gateway-url.execute-api.us-east-1.amazonaws.com/prod'
        self.cognito = boto3.client('cognito-idp')
        
        # Get user pool details from CloudFormation outputs
        self.cf = boto3.client('cloudformation')
        stack_outputs = self.cf.describe_stacks(StackName='raas-stack')['Stacks'][0]['Outputs']
        self.user_pool_id = next(output['OutputValue'] for output in stack_outputs if output['OutputKey'] == 'UserPoolId')
        self.client_id = next(output['OutputValue'] for output in stack_outputs if output['OutputKey'] == 'UserPoolClientId')

    def test_raas_pipeline(self):
        # Upload a sample PDF
        with open('tests/sample-data/sample.pdf', 'rb') as f:
            self.s3.put_object(Bucket=self.input_bucket, Key='sample.pdf', Body=f.read())

        # Wait for processing (adjust time as needed)
        time.sleep(30)

        # Check if summary was created
        summaries = self.s3.list_objects_v2(Bucket=self.summaries_bucket)
        self.assertTrue(any(obj['Key'] == 'sample_summary.txt' for obj in summaries.get('Contents', [])))

        # Test API access
        token = self.get_auth_token()
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(f'{self.api_url}/summaries', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('sample_summary', response.json())

    def get_auth_token(self):
        # This is a simplified auth flow. In a real scenario, you'd use a test user or implement the full Cognito auth flow.
        auth_result = self.cognito.initiate_auth(
            ClientId=self.client_id,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': 'test_user',
                'PASSWORD': 'test_password'
            }
        )
        return auth_result['AuthenticationResult']['IdToken']

if __name__ == '__main__':
    unittest.main()

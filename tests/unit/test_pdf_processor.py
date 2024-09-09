import unittest
import boto3
from moto import mock_s3
from aws.lambda.pdf-processor.index import lambda_handler

class TestPdfProcessor(unittest.TestCase):
    @mock_s3
    def setUp(self):
        self.s3 = boto3.client('s3', region_name='us-east-1')
        self.s3.create_bucket(Bucket='input-bucket')
        self.s3.create_bucket(Bucket='output-bucket')
        
        with open('tests/sample-data/sample.pdf', 'rb') as f:
            self.s3.put_object(Bucket='input-bucket', Key='sample.pdf', Body=f.read())

    @mock_s3
    def test_pdf_processor(self):
        event = {
            'Records': [{
                's3': {
                    'bucket': {'name': 'input-bucket'},
                    'object': {'key': 'sample.pdf'}
                }
            }]
        }
        context = {}

        lambda_handler(event, context)

        result = self.s3.get_object(Bucket='output-bucket', Key='sample.txt')
        content = result['Body'].read().decode('utf-8')

        self.assertIn('Sample PDF content', content)

if __name__ == '__main__':
    unittest.main()

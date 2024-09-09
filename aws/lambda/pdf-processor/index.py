import boto3
import os
from pypdf import PdfReader
import io

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Get the source bucket and object key from the event
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    source_key = event['Records'][0]['s3']['object']['key']
    
    # Download the PDF file from S3
    response = s3.get_object(Bucket=source_bucket, Key=source_key)
    pdf_content = response['Body'].read()
    
    # Extract text from the PDF
    pdf_reader = PdfReader(io.BytesIO(pdf_content))
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    
    # Upload the extracted text to the output bucket
    output_bucket = os.environ['TEXT_OUTPUT_BUCKET']
    output_key = os.path.splitext(source_key)[0] + '.txt'
    s3.put_object(Bucket=output_bucket, Key=output_key, Body=text)
    
    return {
        'statusCode': 200,
        'body': f'Successfully processed {source_key}'
    }

import boto3
import os
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

s3 = boto3.client('s3')

def summarize_text(text, ratio=1/3):
    sentences = sent_tokenize(text)
    words = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word.isalnum() and word not in stop_words]
    
    freq_dist = FreqDist(words)
    most_freq = freq_dist.most_common(int(len(words) * ratio))
    most_freq_words = set(word for word, _ in most_freq)
    
    summary = []
    for sentence in sentences:
        if any(word.lower() in most_freq_words for word in word_tokenize(sentence) if word.isalnum()):
            summary.append(sentence)
    
    return ' '.join(summary)

def lambda_handler(event, context):
    # Get the source bucket and object key from the event
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    source_key = event['Records'][0]['s3']['object']['key']
    
    # Download the text file from S3
    response = s3.get_object(Bucket=source_bucket, Key=source_key)
    text_content = response['Body'].read().decode('utf-8')
    
    # Summarize the text
    summary = summarize_text(text_content)
    
    # Upload the summary to the output bucket
    output_bucket = os.environ['SUMMARY_OUTPUT_BUCKET']
    output_key = os.path.splitext(source_key)[0] + '_summary.txt'
    s3.put_object(Bucket=output_bucket, Key=output_key, Body=summary)
    
    return {
        'statusCode': 200,
        'body': f'Successfully summarized {source_key}'
    }

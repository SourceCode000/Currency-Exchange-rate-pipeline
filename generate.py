from dotenv import load_dotenv
import os
import requests
import json
import boto3

load_dotenv()
api_key = os.getenv("Exhange_API_Key")

url = f'https://v6.exchangerate-api.com/v6/{api_key}/latest/USD'
response = requests.get(url)
data = response.json()
print(data) 

s3 = boto3.client('s3')

s3.put_object(
    Bucket = 'exchange-rate-dump',
    Key = 'exchange_rate_data01.json',
    Body = json.dumps(data)
)

print('Transfer to S3 successful')
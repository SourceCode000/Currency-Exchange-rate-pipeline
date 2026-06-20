import boto3
import json
import psycopg2

s3 = boto3.client('s3')
bucket = 'exchange-rate-dump'

# List all JSON files in bucket
response = s3.list_objects_v2(Bucket=bucket)
files = [obj['Key'] for obj in response['Contents'] if obj['Key'].endswith('.json')]

# Connect to PostgreSQL
conn = psycopg2.connect(
    host='localhost',
    port=5432,
    database='exchange_rate_pipeline',
    user='myuser',
    password='mysecretpassword'
)
cur = conn.cursor()

for file_key in files:
    obj = s3.get_object(Bucket=bucket, Key=file_key)
    data = json.loads(obj['Body'].read())

    fetched_at = data.get('time_last_update_utc', None)

    for currency, rate in data['conversion_rates'].items():
        cur.execute(
            "INSERT INTO raw.exchange_rates (base_currency, target_currency, rate, fetched_at) VALUES (%s, %s, %s, %s)",
            (data['base_code'], currency, rate, fetched_at)
        )

conn.commit()
print(f"Loaded {len(files)} files into PostgreSQL")
cur.close()
conn.close()
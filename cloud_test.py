import boto3
s3 = boto3.client('s3')
s3.put_object( Bucket="exchange-rate-dump", Key="test.txt", Body="hello from python" )
print("success")
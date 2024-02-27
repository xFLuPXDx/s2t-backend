import boto3
import tempfile
# Let's use S3
s3 = boto3.client(
    service_name='s3',
    aws_access_key_id='zVAt4fWHpjDjr6kA',
    aws_secret_access_key='3wIgvl28dCGyrKkBKdOnigJS4DWsGLu75PhpEGac',
    endpoint_url='https://s3.tebi.io'
)
                                  

#data = open('C:/learning/project/fastmongo/venv/fastmongo/S2T/1.mpeg', 'rb')
print("start")
s3.download_file('clarity', '2', '2')
#s3.upload_file('C:/learning/project/fastmongo/venv/fastmongo/S2T/1.mpeg','clarity','2')
print("done")
s3.download_file('clarity', '2', '2')

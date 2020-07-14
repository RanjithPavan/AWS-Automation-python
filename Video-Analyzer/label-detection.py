# coding: utf-8
import boto3
session.resource('s3')
session = boto3.Session(profile_name='automation')
session.resource('s3')
for bucket in s3.buckets.all():
    print(bucket.name)
    
s3 = boto3.resource('s3')
for bucket in s3.buckets.all():
    print(bucket.name)
    
bucket 
bucket = s3.create_bucket(Bucket='ranjithvideolyzer', CreateBucketConfiguration={'LocationConstraint': session.region_name})
bucket
get_ipython().run_line_magic('ls', '')
from pathlib import Path
get_ipython().run_line_magic('ls', '~downloads/*.mp4')
get_ipython().run_line_magic('ls', '~/downloads/*.mp4')
pathname = '~/downloads/Blurry Video Of People Working.mp4'
path = Path(pathname).expanduser().resolve()
print(path)
bucket
bucket.upload_file(str(path), str(path.name))
rekognition_client = session.client('rekognition')
response = rekognition_client.start_label_detection(
    video = {'S3Object' : {'bucket' : bucket.name, 
    'Name' : path.name }
    })
response = rekognition_client.start_label_detection(
    Video = {'S3Object' : {'bucket' : bucket.name, 
    'Name' : path.name }
    })
get_ipython().run_line_magic('clear', '')
response = rekognition_client.start_label_detection(
    Video = {
        'S3Object' : {'Bucket': bucket.name, 'Name': path.name}
    }
    )
response
job_id = response['JobId']
job_id
result = rekognition_client.get_label_detection(JobId = job_id)
result
result.keys()
result['JobStatus']
result['ResponseMetadata']
result['labels']
result['Labels']
get_ipython().run_line_magic('save', 'label-detection.py 1-50')

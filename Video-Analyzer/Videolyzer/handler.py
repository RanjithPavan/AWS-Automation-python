import boto3
import os

def start_label_detection(bucket, key):
    rekognition_client = boto3.client('rekognition')
    response = rekognition_client.start_label_detection(
        Video = {
            'S3Object' : {
            'Bucket' : bucket,
            'Name' : key
            }
        },
        NotificationChannel = {
            'SNSTopicArn': os.environ['REKOGNITION_SNS_TOPIC_ARN'],
            'RoleArn': os.environ['REKOGNITION_ROLE_ARN']
            }
        )

    print(response)
    return


def start_processing_video(event, context):
    for record in event['Records']:
        start_label_detection(
        record['s3']['bucket']['name'],
        record['s3']['object']['key']
        )

    return

def handle_label_detection(event, context):
    print(event)
    return

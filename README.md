# AWS-Automation-python
**This repository is for automating AWS using Python**

=======
### 01- S3-Static-Website

This is a script that will sync a local directory to an s3 bucket, and can configure Route53 and cloudfront.


#### Features
It currently has the following Features.

- list-buckets
- list-bucket-objects
- Create and set up bucket
- Sync website directory tree to bucket
- Set AWS profile with --profile option

### 02- Notifier
It is to notify slack users of changes to AWS account using CloudWatch events

#### Features
It currently has the following features:
  Send notifications to Slack when cloudwatch events happen

### 03 - Video-Analyzer
This is a serverless project that triggers an event whenever a video is uploaded into S3 bucket. Analyze the video with rekognition and store details in dynamo DB.
**Service Information**
  service: videolyzer
  stage: dev
  region: us-east-1
  stack: videolyzer-dev
  resources: 8
  api keys:
    None
  endpoints:
    None
  functions:
    startProcessingVideo: videolyzer-dev-startProcessingVideo
  layers:
    None

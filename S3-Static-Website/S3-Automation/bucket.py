#-*- coding: utf-8 -*-
"""Classes for S3 buckets"""
import mimetypes
from pathlib import Path
import util
from botocore.exceptions import ClientError

class BucketManager:
    """Manage an S3 bucket"""


    def __init__(self, session):
        """Create a BucketManager object"""
        self.session = session
        self.s3 = self.session.resource('s3')


    def get_region_name(self, bucket):
        """Get the region name of a given bucket"""
        client = self.s3.meta.client
        bucket_location = client.get_bucket_location(Bucket=bucket.name)
        return bucket_location["LocationConstraint"] or 'us-east-1'


    def get_bucket_url(self, bucket):
        """Get the website URL for a given bucket"""
        return "http://{}.{}".format(
            bucket.name,
            util.get_endpoint(self.get_region_name(bucket)).host
            )


    def all_buckets(self):
        """Get all buckets"""
        return self.s3.buckets.all()


    def all_objects(self, bucket_name):
        """Return objects of a bucket"""
        return self.s3.Bucket(bucket_name).objects.all()


    def init_bucket(self, bucket_name):
        """ Create a new bucket or return an existing bucket """
        s3_bucket = None
        try:
            s3_bucket = self.s3.create_bucket(
                Bucket = bucket_name,
                CreateBucketConfiguration =
                    {'LocationConstraint' : self.session.region_name}
            )
        except ClientError as error:
            if error.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
                s3_bucket = self.s3.Bucket(bucket_name)
            else:
                raise error

        return s3_bucket

    def set_policy(self, bucket):
        """ Set bucket polciy for public """
        policy = """
            {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Sid": "PublicReadGetObject",
                        "Effect": "Allow",
                        "Principal": "*",
                        "Action": "s3:GetObject",
                        "Resource": "arn:aws:s3:::%s/*"
                    }
                ]
            }
            """ % bucket.name
        policy = policy.strip()
        pol = bucket.Policy()
        pol.put(Policy = policy)

    def configure_website(self, bucket):
        """ Configuring website for S3 bucket"""
        ws = bucket.Website()
        ws.put(WebsiteConfiguration={
                    'ErrorDocument' : {
                        'Key':'error.html'
                    },
                    'IndexDocument' : {
                        'Suffix':'index.html'
                    }
            })

    @staticmethod
    def upload_file(bucket, path, key):
        """ Upload path to S3 bucket. """
        content_type = mimetypes.guess_type(key)[0] or 'text/plain'
        return bucket.upload_file(
            path,
            key,
            ExtraArgs={
                'ContentType': 'content_type'
            })

    def sync(self, pathname, bucket_name):
        bucket = self.s3.Bucket(bucket_name)
        root = Path(pathname).expanduser().resolve()
        def handle_directory(target):
            for p in target.iterdir():
                if p.is_dir():
                    handle_directory(p)
                if p.is_file():
                    self.upload_file(bucket, str(p), str(p.relative_to(root)))

        handle_directory(root)

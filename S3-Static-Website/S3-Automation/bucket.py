#-*- coding: utf-8 -*-
"""Classes for S3 buckets"""
import mimetypes
import util
import boto3
from botocore.exceptions import ClientError
from pathlib import Path
from functools import reduce
from hashlib import md5

class BucketManager:
    """Manage an S3 bucket"""

    CHUNK_SIZE = 8388608

    def __init__(self, session):
        """Create a BucketManager object"""
        self.session = session
        self.s3 = self.session.resource('s3')
        self.transfer_config = boto3.s3.transfer.TransferConfig(
            multipart_chunksize = self.CHUNK_SIZE,
            multipart_threshold = self.CHUNK_SIZE
        )

        self.manifest = {}


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


    def load_manifest(self, bucket):
        """Load manifest for caching"""
        paginator = self.s3.meta.client.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket=bucket.name):
            for obj in page.get('Contents', []):
                self.manifest[obj['Key']]=obj['ETag']

    @staticmethod
    def hash_data(data):
        """ generate MD5 for data """
        hash = md5()
        hash.update(data)
        return hash

    def gen_etag(self, path):
        """ Generate Etag for data"""
        hashes = []
        with open(path, 'rb') as f:
            while True:
                data = f.read(self.CHUNK_SIZE)
                if not data:
                    break

                hashes.append(self.hash_data(data))

        if not hashes:
            return
        elif len(hashes) == 1:
            return '"{}"'.format(hashes[0].hexdigest())
        else:
            digests = (h.digest() for h in hashes)
            hash = self.hash_data(reduce(lambda x, y: x + y, digests))
            return '"{}-{}"'.format(hash.hexdigest(), len(hashes))


    def upload_file(self, bucket, path, key):
        """ Upload path to S3 bucket. """
        content_type = mimetypes.guess_type(key)[0] or 'text/plain'
        etag = self.gen_etag(path)
        if self.manifest.get(key, '') == etag:
            #print("skipping {}, etags match".format(key))
            return

        return bucket.upload_file(
            path,
            key,
            ExtraArgs={
                'ContentType': 'content_type'
            },
            Config = self.transfer_config
        )

    def sync(self, pathname, bucket_name):
        bucket = self.s3.Bucket(bucket_name)
        self.load_manifest(bucket)
        root = Path(pathname).expanduser().resolve()
        def handle_directory(target):
            for p in target.iterdir():
                if p.is_dir():
                    handle_directory(p)
                if p.is_file():
                    self.upload_file(bucket, str(p), str(p.relative_to(root)))

        handle_directory(root)

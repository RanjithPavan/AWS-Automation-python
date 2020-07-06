#!/usr/bin/Python
# -*- coding: utf-8 -*-
# Deploy websites to AWS. It automates deploying static websites to aws


import click
import boto3
from pathlib import Path
import mimetypes

from bucket import BucketManager

session = boto3.Session(profile_name='automation')
bucket_manager = BucketManager(session)
#s3 = session.resource('s3')


@click.group()
def cli():
    """Deployes websites to AWS"""
    pass


@cli.command('list-buckets')
def list_buckets():
    """List all S3 buckets"""
    for bucket in bucket_manager.all_buckets():
        print(bucket)


@cli.command('list-bucket-objects')
@click.argument('bucket')
def list_bucket_objects(bucket):
    """List objects in a given bucket"""
    for object in bucket_manager.all_objects(bucket):
        print(object)


@cli.command('setup-bucket')
@click.argument('bucket')
def setup_bucket(bucket):
    """Create and Configure S3 Bucket"""
    s3_bucket = bucket_manager.init_bucket(bucket)
    bucket_manager.set_policy(s3_bucket)
    bucket_manager.configure_website(s3_bucket)
    return


@cli.command('sync')
@click.argument('pathname', type=click.Path(exists=True))
@click.argument('bucket')
def sync(pathname, bucket):
    "Sync contents of path to S3 bucket"

    bucket_manager.sync(pathname, bucket)

if __name__== '__main__':
    cli()

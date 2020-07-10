#!/usr/bin/Python
# -*- coding: utf-8 -*-
# Deploy websites to AWS. It automates deploying static websites to aws


import click
import boto3
from pathlib import Path
import mimetypes

from bucket import BucketManager

session = None
bucket_manager = None

@click.group()
@click.option('--profile', default = None,
    help="Use a given AWS profile")
def cli(profile):
    """Deployes websites to AWS"""
    global session, bucket_manager

    session_cfg = {}
    if profile:
        session_cfg['profile_name'] = profile
    session = boto3.Session(**session_cfg)
    bucket_manager = BucketManager(session)



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
    print(bucket_manager.get_bucket_url(bucket_manager.s3.Bucket(bucket)))

if __name__== '__main__':
    cli()

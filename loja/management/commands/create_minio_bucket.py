import os

import boto3
from botocore.exceptions import ClientError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Creates the MinIO bucket defined by MINIO_BUCKET_NAME if it does not already exist.'

    def handle(self, *args, **options):
        endpoint = os.environ.get('MINIO_ENDPOINT', '')
        access_key = os.environ.get('MINIO_ACCESS_KEY', '')
        secret_key = os.environ.get('MINIO_SECRET_KEY', '')
        bucket_name = os.environ.get('MINIO_BUCKET_NAME', 'media')

        if not endpoint:
            self.stderr.write(
                self.style.WARNING('MINIO_ENDPOINT is not set — skipping bucket creation.')
            )
            return

        s3 = boto3.client(
            's3',
            endpoint_url=endpoint,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name='us-east-1',
            use_ssl=endpoint.startswith('https'),
            config=boto3.session.Config(signature_version='s3v4', s3={'addressing_style': 'path'}),
        )

        try:
            s3.head_bucket(Bucket=bucket_name)
            # Bucket already exists — nothing to do.
        except ClientError as exc:
            error_code = exc.response['Error']['Code']
            if error_code in ('404', 'NoSuchBucket'):
                try:
                    s3.create_bucket(Bucket=bucket_name)
                except ClientError as create_exc:
                    self.stderr.write(
                        self.style.ERROR(
                            f'Failed to create bucket "{bucket_name}": {create_exc}'
                        )
                    )
                    raise SystemExit(1) from create_exc
            else:
                self.stderr.write(
                    self.style.ERROR(
                        f'Unexpected error checking bucket "{bucket_name}": {exc}'
                    )
                )
                raise SystemExit(1) from exc

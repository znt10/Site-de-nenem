import os

from storages.backends.s3boto3 import S3Boto3Storage


class MinIOMediaStorage(S3Boto3Storage):
    """
    Custom storage backend for MinIO (S3-compatible).

    Reads connection credentials from environment variables:
      - MINIO_ENDPOINT      e.g. "http://minio.railway.internal:9000"
      - MINIO_ACCESS_KEY    MinIO access key / username
      - MINIO_SECRET_KEY    MinIO secret key / password
      - MINIO_BUCKET_NAME   Target bucket name

    Files are stored under the path determined by each model field's
    ``upload_to`` argument and served via the same endpoint so that
    Django can generate working URLs for the web interface.

    """

    def __init__(self, **kwargs):
        kwargs.setdefault("bucket_name", os.environ.get("MINIO_BUCKET_NAME", "media"))
        kwargs.setdefault("access_key", os.environ.get("MINIO_ACCESS_KEY", ""))
        kwargs.setdefault("secret_key", os.environ.get("MINIO_SECRET_KEY", ""))

        # Internal (private) MinIO endpoint — must include the scheme,
        # e.g. "http://minio.railway.internal:9000".
        kwargs.setdefault("endpoint_url", os.environ.get("MINIO_ENDPOINT", ""))

        # MinIO works best with path-style addressing (bucket in the URL
        # path rather than as a subdomain).
        kwargs.setdefault("addressing_style", "path")

        # Use AWS Signature Version 4, which MinIO requires.
        kwargs.setdefault("signature_version", "s3v4")

        # MinIO's default region identifier.
        kwargs.setdefault("region_name", "us-east-1")

        # The private endpoint is typically plain HTTP inside Railway's
        # internal network.
        kwargs.setdefault("use_ssl", False)

        # Do not append query-string auth tokens to URLs; the bucket
        # should be publicly readable (or access controlled at the
        # MinIO level).
        kwargs.setdefault("querystring_auth", False)

        # Overwrite files with the same name instead of appending a
        # suffix, which keeps URLs stable when an image is re-uploaded.
        kwargs.setdefault("file_overwrite", True)

        super().__init__(**kwargs)

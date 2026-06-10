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

    Files are served via the same endpoint so that Django can generate
    working URLs for the web interface. The upload path prefix is
    determined solely by each ImageField's ``upload_to`` argument —
    no ``location`` is set here to avoid duplicating the prefix.
    """

    def __init__(self, **kwargs):
        bucket = os.environ.get("MINIO_BUCKET_NAME", "media")
        kwargs.setdefault("bucket_name", bucket)
        kwargs.setdefault("access_key", os.environ.get("MINIO_ACCESS_KEY", ""))
        kwargs.setdefault("secret_key", os.environ.get("MINIO_SECRET_KEY", ""))

        # Internal (private) MinIO endpoint used for upload connections only.
        # Must include the scheme, e.g. "http://minio.railway.internal:9000".
        kwargs.setdefault("endpoint_url", os.environ.get("MINIO_ENDPOINT", ""))

        # Public endpoint used by S3Boto3Storage.url() to generate URLs that
        # browsers can reach.  When custom_domain is set, django-storages
        # builds URLs as https://<custom_domain>/<key> instead of using
        # endpoint_url, so uploads go through the private network while
        # served URLs point at the public host.
        # Format expected by S3Boto3Storage: "<host>/<bucket>" (no scheme).
        _public = os.environ.get("MINIO_PUBLIC_ENDPOINT", "").rstrip("/")
        if _public:
            # Strip the scheme so S3Boto3Storage can prepend its own.
            _public_host = _public.split("://", 1)[-1]
            kwargs.setdefault("custom_domain", f"{_public_host}/{bucket}")

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

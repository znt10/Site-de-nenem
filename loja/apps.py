from django.apps import AppConfig


class LojaConfig(AppConfig):
    name = 'loja'

    def ready(self):
        from . import signals  # noqa: F401

        # Ensure the MinIO bucket exists before the app starts handling
        # requests. This is a no-op when the bucket already exists, so it
        # is safe to run on every startup.
        try:
            from django.core.management import call_command
            call_command('create_minio_bucket')
        except Exception as exc:  # pragma: no cover
            import logging
            logging.getLogger(__name__).error(
                'Could not create MinIO bucket on startup: %s', exc
            )

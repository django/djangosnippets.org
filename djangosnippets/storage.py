from ecstatic.storage import CachedStaticFilesMixin
from storages.backends.s3boto import S3BotoStorage


class DjangoSnippetsStaticFilesStorage(CachedStaticFilesMixin,
                                       S3BotoStorage):
    pass

from ecstatic.storage import CachedStaticFilesMixin, StaticManifestMixin
from storages.backends.s3boto import S3BotoStorage


class DjangoSnippetsStaticFilesStorage(StaticManifestMixin,
                                       CachedStaticFilesMixin,
                                       S3BotoStorage):
    pass

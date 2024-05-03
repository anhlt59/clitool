from clitool.services.base import AwsService

from .bucket import S3BucketService
from .object import S3ObjectService


class S3Service(AwsService):
    def __init__(self, session):
        super().__init__(session)
        self.bucket = S3BucketService(session)
        self.object = S3ObjectService(session)


__all__ = ["S3Service"]

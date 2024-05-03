from clitool.services.base import AwsService
from clitool.types.s3 import S3Bucket, S3Buckets


class S3BucketService(AwsService):
    @property
    def client(self):
        return self.session.client("s3")

    def list(self, prefix: str = "") -> S3Buckets:
        response = self.client.list_buckets()
        buckets = S3Buckets()
        for item in response.get("Buckets"):
            if prefix and not item.get("Name", "").startswith(prefix):
                continue
            buckets.append(S3Bucket(name=item["Name"], creation_date=item.get("CreationDate")))
        return buckets

import os

from clitool.services.base import AwsService
from clitool.types.s3 import S3Bucket, S3Object, S3Objects


class S3ObjectService(AwsService):
    @property
    def client(self):
        return self.session.client("s3")

    def list(self, bucket: str, prefix: str = "") -> S3Objects:
        s3_objects = S3Objects()
        response = self.client.list_objects_v2(Bucket=bucket, Prefix=prefix)
        for item in response.get("Contents", []):
            s3_objects.append(S3Object(key=item["Key"], bucket=S3Bucket(name=bucket)))
        return s3_objects

    def put(self, bucket: str, key: str, file_path: str) -> S3Object:
        if not os.path.exists(file_path):
            raise Exception(f"File {file_path} not found")
        with open(file_path, "rb") as f:
            data = f.read()
        self.client.put_object(Bucket=bucket, Key=key, Body=data)
        return S3Object(key=key, bucket=S3Bucket(name=bucket))

import os
from io import BytesIO
from typing import BinaryIO, List

from minio import Minio

from .storage_clients_types import StorageClients


class FileStorageClient:

    def __init__(self, bucket_name: str = "flydams", client_type: StorageClients = "minio"):
        self.bucket = bucket_name
        self.client = Minio(
            os.getenv("MINIO_ENDPOINT"),
            access_key=os.getenv("MINIO_ACCESS_KEY"),
            secret_key=os.getenv("MINIO_SECRET_KEY"),
            secure=os.getenv("MINIO_SECURE_SETTING", "False").lower() in ("true", "1"),
        )

        self.createBucket(bucket_name)

    # Make the bucket if it doesn't exist.
    def createBucket(self, bucket_name: str) -> None:
        found = self.client.bucket_exists(bucket_name)
        if not found:
            self.client.make_bucket(bucket_name)
            print("Created bucket", bucket_name)
        else:
            print("Bucket", self.bucket, "already exists")

    def uploadFile(self, path: str, data: BinaryIO, size: int) -> str:
        file_identifier = self.client.put_object(self.bucket, path, data, size)
        return file_identifier.etag

    # List all files in a bucket
    def listBucketObjects(self, bucket: str = "flydams") -> List[object]:
        storage_files = self.client.list_objects(bucket)
        storage_files = [vars(storage_obj) for storage_obj in storage_files]

        filtered_files = [{"fileName": file["_object_name"]} for file in storage_files]
        return filtered_files

    def getFileByName(self, file_name: str) -> BinaryIO:
        minio_file_object = self.client.get_object(self.bucket, file_name)

        byte_stream = BytesIO(minio_file_object.read())
        byte_stream.seek(0)

        return byte_stream

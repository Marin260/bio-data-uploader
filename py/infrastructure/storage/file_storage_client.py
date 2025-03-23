from .storage_clients_types import StorageClients
from typing import BinaryIO, List
from minio import Minio


class FileStorageClient:

    def __init__(
            self, 
            bucket_name: str = "flydams",
            client_type: StorageClients = "minio"
        ):
        #TODO: Use client_type to generalize this to accept any storage client 
        
        self.bucket = bucket_name
        self.client = Minio(
            "127.0.0.1:9000", # TODO: fix this one also
            access_key="hide this one",
            secret_key="hide this one also",
            secure=False
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


    def uploadFile(self, path:str, data: BinaryIO, size: int) -> None:
        self.client.put_object(
            self.bucket, path, data, size
        )

    
    # List all files in a bucket
    def listBucketObjects(self, bucket: str = "flydams") -> List[object]:
        storage_files = self.client.list_objects(bucket)
        storage_files = [vars(storage_obj) for storage_obj in storage_files]

        filtered_files = [{"fileName": file["_object_name"]} for file in storage_files]
        return filtered_files




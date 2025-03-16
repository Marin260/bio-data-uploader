from minio import Minio

class FileStorageClient:
    def MinioClient(self) -> Minio:
        return Minio(
            "127.0.0.1:9000",
            access_key="ROOTNAME",
            secret_key="CHANGEME123",
            secure=False
        )

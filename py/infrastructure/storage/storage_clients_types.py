"""
Available storage clients
"""

from enum import StrEnum

class StorageClients(StrEnum):
    minio = "minio"
    azure = "azure"
    aws = "aws"

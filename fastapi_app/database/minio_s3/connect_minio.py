from minio import Minio

from config import minio_settings

minio_client = Minio(**minio_settings)

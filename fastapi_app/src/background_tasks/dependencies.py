from config import minio_bucket
from database import minio_client


def save_file_in_minio(
        file_data: str,
        file_size: int,
        file_format: str,
        file_key: str,
        content_type: str,
) -> None:
    """
    Функция сохранения файла в бэкраунде
    """
    minio_client.put_object(
        **minio_bucket,
        object_name=file_key + file_format,
        data=file_data,
        content_type=content_type,
        length=file_size
    )

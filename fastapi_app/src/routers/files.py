import uuid
import re

from fastapi import APIRouter, UploadFile, status, HTTPException, Depends

from config import minio_bucket, ResponseFile
from database import Images
from src import GetUser, UserStatus
from database import minio_client

router = APIRouter(
    prefix='/files',
    tags=['Files'],
    responses={422: {'description': 'Uncorrected format'}},
)


@router.post(
    '/upload',
    response_model=ResponseFile,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(GetUser(UserStatus.DEFAULT_USER.value))]
)
async def upload_files(file: UploadFile):
    """
    Закрузка файла в minio
    """
    # Продумать что делать с ошибками
    error = HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    regex = re.compile(r'\.(jpg|png|gif)$', re.IGNORECASE).search(file.filename)
    print(regex.string)
    if not regex:
        raise error

    image_key = str(uuid.uuid4())

    try:
        minio_client.put_object(
            **minio_bucket,
            object_name=image_key + file.filename,
            data=file.file,
            content_type=file.content_type,
            length=file.size
        )

    except Exception:
        raise error

    save_info_in_db = await Images.create(image_key=image_key, name=file.filename)

    return save_info_in_db

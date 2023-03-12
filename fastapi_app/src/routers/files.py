import uuid
import re

from fastapi import APIRouter, UploadFile, status, HTTPException, Depends, Path, File
from fastapi.responses import StreamingResponse

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
    error = HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    regex = re.compile(r'\.(jpg|png|gif)$', re.IGNORECASE)
    file_format = '.' + regex.findall(file.filename)[0]

    if not file_format:
        raise error

    image_key = str(uuid.uuid4())

    try:
        minio_client.put_object(
            **minio_bucket,
            object_name=image_key + file_format,
            data=file.file,
            content_type=file.content_type,
            length=file.size
        )
        print(file.content_type)
    except Exception:
        raise error

    save_info_in_db = await Images.create(
        image_key=image_key,
        name=file.filename,
        file_format=file_format,
        content_type=file.content_type
    )

    return save_info_in_db


@router.get(
    '/upload/{uuid_file}',
    response_model=bytes,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(GetUser(UserStatus.DEFAULT_USER.value))]
)
async def get_file(uuid_file: str = Path(...)):
    """
    Получение файла из minio и отдаем его
    """
    image_data = await Images.get(image_key=uuid_file)

    if not image_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    image_name = uuid_file + image_data.file_format

    image = minio_client.get_object(
        **minio_bucket,
        object_name=image_name
    )

    return StreamingResponse(image, media_type=image_data.content_type)

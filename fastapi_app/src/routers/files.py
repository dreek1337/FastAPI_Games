import re
import uuid

from fastapi import APIRouter, UploadFile, status, HTTPException, Depends, Path, BackgroundTasks
from fastapi.responses import StreamingResponse

from config import minio_bucket, ResponseFile
from database import Files
from src import GetUser, UserStatus, save_file_in_minio
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
    dependencies=[Depends(GetUser(UserStatus.DEFAULT_USER))]
)
async def upload(file: UploadFile, background_task: BackgroundTasks):
    """
    Закрузка файла в minio
    """
    error = HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    regex = re.compile(r'\.(jpg|png|gif|mp4|avg)$', re.IGNORECASE)
    file_format = '.' + regex.findall(file.filename)[0]

    if not file_format:
        raise error

    file_key = str(uuid.uuid4())

    info_for_save = {
        'file_format': file_format,
        'file_key': file_key,
        'content_type': file.content_type,
    }

    background_task.add_task(
        save_file_in_minio,
        file_data=file.file,
        file_size=file.size,
        **info_for_save
    )

    save_info_in_db = await Files.create(
        name=file.filename,
        **info_for_save
    )

    return save_info_in_db


@router.get(
    '/get_file/{uuid_file}',
    response_model=bytes,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(GetUser(UserStatus.DEFAULT_USER))]
)
async def get_file(uuid_file: str = Path(...)):
    """
    Получение файла из minio и отдаем его
    """
    file_data = await Files.get(file_key=uuid_file)

    if not file_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    file_name = uuid_file + file_data.file_format

    file = minio_client.get_object(
        **minio_bucket,
        object_name=file_name
    )

    return StreamingResponse(file, media_type=file_data.content_type)

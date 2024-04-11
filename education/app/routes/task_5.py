import os
import shutil
import zipfile

from fastapi import APIRouter, UploadFile, HTTPException
from fastapi.responses import StreamingResponse

router = APIRouter(tags=["API для хранения файлов"])

"""
Задание_5. API для хранения файлов

a.	Написать API для добавления(POST) "/upload_file" и скачивания (GET) "/download_file/{id}" файлов. 
В ответ на удачную загрузку файла должен приходить id для скачивания. 
b.	Добавить архивирование к post запросу, то есть файл должен сжиматься и сохраняться в ZIP формате.
с*.Добавить аннотации типов.
"""

upload_dir = "uploaded_files"
if not os.path.exists(upload_dir):
    os.makedirs(upload_dir)

async def get_file_path(file_id: str) -> str:
    file_path = f"uploaded_files/{file_id}.zip"
    return file_path

@router.post("/upload_file", description="Задание_5. API для хранения файлов")
async def upload_file(file: UploadFile) -> str:
    try:
        file_path = os.path.join(upload_dir, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        zip_file_path = f"{file_path}.zip"
        with zipfile.ZipFile(zip_file_path, "w") as zipf:
            zipf.write(file_path, arcname=file.filename)

        os.remove(file_path)
        return file.filename
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/download_file/{file_id}", description="Задание_5. API для хранения файлов")
async def download_file(file_id: str) -> StreamingResponse:
    try:
        file_path = await get_file_path(file_id)
        file_name = file_path.split("/")[-1]

        return StreamingResponse(open(file_path, "rb"), media_type="application/octet-stream",
                                 headers={"Content-Disposition": f"attachment; filename={file_name}"})
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

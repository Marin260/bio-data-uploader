from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile
from fastapi.responses import StreamingResponse

from api.dependencies import require_bearer
from api.services import SleepAnalysisService
from infrastructure import FileStorageClient

router = APIRouter(prefix="/files", tags=["Files"], dependencies=[Depends(require_bearer)])


@router.get("/")
def getAllFiles():
    storage_client = FileStorageClient()

    return storage_client.listBucketObjects()


@router.get("/getFileByName/{file_name}")
def getFileByName(file_name: str):
    storage_client = FileStorageClient()

    requested_file = storage_client.getFileByName(file_name)

    return StreamingResponse(
        content=iter([requested_file.getvalue()]),
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={file_name}"},
    )


@router.post("/generateZip/")
def generateZip(
    file: UploadFile,
    start: Annotated[str, Form()],
    end: Annotated[str, Form()],
    file_name: Annotated[str, Form()],
):
    # TODO: cretae validators, separate them in a different file
    if file.size > 3000000:
        raise HTTPException(status_code=400, detail="File size too big")

    sleep_analysis_service = SleepAnalysisService()
    storage_client = FileStorageClient()

    zip_buffer, zip_data_len = sleep_analysis_service.generate_zip_buffer(file.file, start, end)

    storage_client.uploadFile(f"{file_name}.zip", zip_buffer, zip_data_len)

    return StreamingResponse(
        content=iter([zip_buffer.getvalue()]),
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={file_name}.zip"},
    )

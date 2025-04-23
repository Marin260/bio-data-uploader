from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException, Request, UploadFile
from fastapi.responses import StreamingResponse

from api.dependencies import require_bearer
from api.services import AuthorizationService, SleepAnalysisService
from infrastructure import FileStorageClient
from persistence.entities import File
from persistence.repository import FileQueries, UserQueries, file_repo, user_repo

router = APIRouter(prefix="/files", tags=["Files"], dependencies=[Depends(require_bearer)])


@router.get("/")
def getAllFiles():
    storage_client = FileStorageClient()

    return storage_client.listBucketObjects()


@router.get("/{file_name}")
def getFileByName(file_name: str):
    storage_client = FileStorageClient()

    requested_file = storage_client.getFileByName(file_name)

    return StreamingResponse(
        content=iter([requested_file.getvalue()]),
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={file_name}"},
    )


@router.post("/generate-zip/")
def generateZip(
    request: Request,
    file: UploadFile,
    start: Annotated[str, Form()],
    end: Annotated[str, Form()],
    file_name: Annotated[str, Form()],
    file_queries: FileQueries = Depends(file_repo),
    user_queries: UserQueries = Depends(user_repo),
):
    # TODO: create validators, separate them in a different module
    # TODO: check if file already exists in db or storage (file_name) should i overwrite in storage or db?
    if file.size > 3000000:
        raise HTTPException(status_code=400, detail="File size too big")

    sleep_analysis_service = SleepAnalysisService()
    storage_client = FileStorageClient()
    authz_service = AuthorizationService()

    zip_buffer, zip_data_len = sleep_analysis_service.generate_zip_buffer(file.file, start, end)
    file_identifier = storage_client.uploadFile(f"{file_name}.zip", zip_buffer, zip_data_len)

    current_user = user_queries.select_user_by_email(authz_service.get_loged_in_user(request))

    file_queries.insert_file(
        File(
            file_name=file_name,
            file_storage_identifier=file_identifier,
            file_size=file.size,
            user_id=current_user.user_id,
        )
    )

    return StreamingResponse(
        content=iter([zip_buffer.getvalue()]),
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={file_name}.zip"},
    )

from fastapi import FastAPI, Form, UploadFile, HTTPException
from infrastructure import FileStorageClient
from services import SleepAnalysisService
from typing import Annotated
from time import time


app = FastAPI()


@app.get("/ping")
def healthCheck():
    return {"Hello": "World"}

@app.post("/file-upload")
def fileUpload(
    file: UploadFile, 
    start: Annotated[str, Form()], 
    end: Annotated[str, Form()]
):
    file_client = FileStorageClient()

    uploaded_file = file.filename.split('.')
    epoch = str(time()).split('.')
    destination_file = f"{uploaded_file[0]}_{'_'.join(epoch)}.{uploaded_file[-1]}"

    # don't accept files bigger than 3MB
    if file.size > 3000000:
        raise HTTPException(status_code=400, detail="File size too big")        
    
    # Upload the file, renaming it in the process
    file_client.uploadFile(
        destination_file, file.file, file.size
    )

    return {
        "filename": file.filename,
        "size": file.size,
    }


@app.post("/generateZip")
def generateZip(
    file: UploadFile, 
    start: Annotated[str, Form()], 
    end: Annotated[str, Form()],
    file_name: Annotated[str, Form()]
):
    if file.size > 3000000:
        raise HTTPException(status_code=400, detail="File size too big")   
    
    sleep_service = SleepAnalysisService()
    file_client = FileStorageClient()

    zip_buffer, zip_data = sleep_service.generate_zip_buffer(file.file, start, end)
    
    file_client.uploadFile(f"{file_name}.zip", zip_buffer, zip_data)

    return {
        "minio_path": f"{file_name}.zip"
    }

@app.get("/getAllFiles")
def getAllFiles():
    storage_client = FileStorageClient()
    
    return storage_client.listBucketObjects()
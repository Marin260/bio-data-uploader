import os
from time import time
from typing import Annotated

from dotenv import load_dotenv
from fastapi import FastAPI, Form, HTTPException, UploadFile

from infrastructure import FileStorageClient
from routes.files import files

# load the env file
ENVIRONMENT = os.getenv("FLY_DAMS_ENVIRONMENT")
if os.getenv("FLY_DAMS_ENVIRONMENT"):
    load_dotenv(f"settings/{ENVIRONMENT}/.env")
else:
    load_dotenv(f"settings/.env")


app = FastAPI()

app.include_router(files.router)


@app.get("/ping")
def healthCheck():
    return {"Hello": "World"}


@app.post("/file-upload")
def fileUpload(
    file: UploadFile, start: Annotated[str, Form()], end: Annotated[str, Form()]
):
    file_client = FileStorageClient()

    uploaded_file = file.filename.split(".")
    epoch = str(time()).split(".")
    destination_file = f"{uploaded_file[0]}_{'_'.join(epoch)}.{uploaded_file[-1]}"

    # don't accept files bigger than 3MB
    if file.size > 3000000:
        raise HTTPException(status_code=400, detail="File size too big")

    # Upload the file, renaming it in the process
    file_client.uploadFile(destination_file, file.file, file.size)

    return {
        "filename": file.filename,
        "size": file.size,
    }

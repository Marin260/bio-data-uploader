from typing import Union, Annotated

from fastapi import FastAPI, Form, UploadFile, HTTPException

from infrastructure.storage.minio import FileStorageClient

from time import time
app = FastAPI()


@app.get("/ping")
def healthCheck():
    return {"Hello": "World"}


@app.get("/zip/{file_name}")
def zipFiles(file_name: str, q: Union[str, None] = None):
    return {"item_id": file_name, "q": q}


@app.post("/file-upload")
def fileUpload(
    file: UploadFile, 
    start: Annotated[str, Form()], 
    end: Annotated[str, Form()]
):
    fileClient = FileStorageClient().MinioClient()


    source_file = "./tmbcMFCtM008.txt"

    bucket_name = "flydams"
    uploaded_file = file.filename.split('.')
    epoch = str(time()).split('.')
    destination_file = f"{uploaded_file[0]}_{'_'.join(epoch)}.{uploaded_file[-1]}"


    # Make the bucket if it doesn't exist.
    found = fileClient.bucket_exists(bucket_name)
    if not found:
        fileClient.make_bucket(bucket_name)
        print("Created bucket", bucket_name)
    else:
        print("Bucket", bucket_name, "already exists")

    # Upload the file, renaming it in the process
    fileClient.put_object(
        bucket_name, destination_file, file.file, file.size
    )
    print(
        source_file, "successfully uploaded as object",
        destination_file, "to bucket", bucket_name,
    )


    # don't accept files bigger than 3MB
    if file.size > 3000000:
        raise HTTPException(status_code=400, detail="File size too big")
    
    
        
    
    return {
        "filename": file.filename,
        "size": file.size,
    }
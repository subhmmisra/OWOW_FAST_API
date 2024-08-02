import os
import uuid
from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.security import HTTPBasicCredentials
from pydantic import BaseModel, Field
import uuid

from app.utils.auth import authenticate
from services.summary_service import (
    save_file,
    extract_text,
    get_summary,
    collection,
    uuid_to_bson_binary,
    bson_binary_to_uuid,
)

from app.models.file_model import FileModel, FileUploadResponse

# from app.schemas import FileUploadResponse
from pymongo.errors import DuplicateKeyError

app = FastAPI()


@app.post("/v1/files", response_model=FileUploadResponse)
async def upload_file(
    file: UploadFile = File(...),
    credentials: HTTPBasicCredentials = Depends(authenticate),
):
    """
    Endpoint for uploading files.

    This endpoint accepts a file of type .docx, .pptx or .pdf and saves it to the database.
    The file is first checked for its extension, and if it is not a valid type, an HTTPException is raised.
    Then, the file is checked against the database to see if it already exists. If it does, an HTTPException is raised.
    If the file passes these checks, a new UUID is generated for the file, the file is saved to disk, and its content is extracted.
    A summary of the extracted text is then generated using a machine learning model.
    The file data is then inserted into the database, and a response is returned with the file's ID, name and summary.

    Args:
        file (UploadFile): The file to be uploaded.
        credentials (HTTPBasicCredentials): The credentials of the user.

    Returns:
        FileUploadResponse: A response containing the file's ID, name and summary.

    Raises:
        HTTPException: If the file type is not valid, or if the file already exists in the database.
    """

    # Check file extension
    if not file.filename.endswith((".docx", ".pptx", ".pdf")):
        raise HTTPException(
            status_code=400,
            detail="Invalid file extension. Only .docx, .pptx and .pdf are allowed.",
        )

    # Check if file already exists in the database
    file_exists = await collection.find_one({"file_name": file.filename})
    if file_exists:
        raise HTTPException(status_code=400, detail="File already exists.")

    # Generate new UUID for the file
    file_id = str(uuid.uuid4())

    # Save file to disk
    file_path = await save_file(file, file.filename, os.path.splitext(file.filename)[1])

    # Extract text from file
    text = extract_text(file_path, os.path.splitext(file.filename)[1])

    # Generate summary of text
    summary = get_summary(text)

    # Insert file data into the database
    file_data = {
        "_id": uuid_to_bson_binary(uuid.UUID(file_id)),
        "file_name": file.filename,
        "file_summary": summary,
    }

    try:
        await collection.insert_one(file_data)
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="File with this ID already exists.")

    # Return file ID, name and summary in a response
    return FileUploadResponse(
        file_id=file_id, file_name=file.filename, file_summary=summary
    )


@app.get("/v1/files")
async def list_files(credentials: HTTPBasicCredentials = Depends(authenticate)):
    """
    Endpoint to list all files stored in the database.

    Returns a list of dictionaries containing the file_id and file_name of each file.
    """

    # Retrieve all files from the database
    files = await collection.find().to_list(1000)

    # Create a list of dictionaries containing the file_id and file_name of each file
    return [
        {
            "file_id": str(bson_binary_to_uuid(file["_id"])),  # Convert UUID to string
            "file_name": file["file_name"],  # Extract file_name from file dictionary
            "file_id": str(bson_binary_to_uuid(file["_id"])),
            "file_name": file["file_name"],
        }
        for file in files
    ]


@app.get("/v1/files/{file_id}")
async def get_file_summary(
    file_id: str, credentials: HTTPBasicCredentials = Depends(authenticate)
):
    """
    Endpoint to retrieve the summary of a specific file.

    Args:
        file_id (str): The ID of the file to retrieve.
        credentials (HTTPBasicCredentials, optional): The credentials of the user. Defaults to Depends(authenticate).

    Returns:
        dict: A dictionary containing the file_id, file_name, and file_summary of the file.

    Raises:
        HTTPException: If the file is not found.
    """
    # Retrieve the file from the database based on the file_id
    file = await collection.find_one({"_id": uuid_to_bson_binary(uuid.UUID(file_id))})
    # If the file is not found, raise an HTTPException
    file = await collection.find_one({"_id": uuid_to_bson_binary(uuid.UUID(file_id))})
    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    # Return a dictionary containing the file_id, file_name, and file_summary of the file
    return {
        "file_id": file_id,
        "file_name": file["file_name"],
        "file_summary": file["file_summary"],
    }

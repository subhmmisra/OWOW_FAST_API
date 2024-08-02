# OWOW FastAPI File Upload and Summary Project

This project is a FastAPI application that allows users to upload files, list files, and retrieve file summaries. 
The files are stored on the server and their metadata, including summaries, is stored in a MongoDB database. The project uses HTTP Basic Authentication for secure access.

## Features

- **File Upload**: Upload files with extensions `.docx`, `.pptx`, or `.pdf`.
- **File Listing**: Retrieve a list of all uploaded files.
- **File Summary**: Get a summary of a specific file.
- **Authentication**: Basic HTTP authentication for secure access.

## Endpoints

### Upload File

- **URL**: `/v1/files`
- **Method**: `POST`
- **Description**: Upload a file. Only `.docx`, `.pptx`, and `.pdf` files are accepted.
- **Request Body**: 
  - `file`: The file to be uploaded.
- **Response**: 
  - `file_id`: UUID of the uploaded file.
  - `file_name`: Name of the uploaded file.
  - `file_summary`: Summary of the file's content.

### List Files

- **URL**: `/v1/files`
- **Method**: `GET`
- **Description**: List all uploaded files.
- **Response**: 
  - A list of files with their `file_id` and `file_name`.

### Get File Summary

- **URL**: `/v1/files/{file_id}`
- **Method**: `GET`
- **Description**: Retrieve the summary of a specific file by its `file_id`.
- **Path Parameters**: 
  - `file_id`: The ID of the file to retrieve.
- **Response**: 
  - `file_id`: UUID of the file.
  - `file_name`: Name of the file.
  - `file_summary`: Summary of the file's content.

## Authentication

This project uses HTTP Basic Authentication. Use the following credentials:

- **Username**: `admin`
- **Password**: `admin123`

## Setup

### Prerequisites

- Python 3.7+
- MongoDB
- FastAPI
- Pydantic
- Pymongo

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/subhmmisra/OWOW_FAST_API.git
    ```

2. Navigate to the project directory:
    ```sh
    cd <project-directory>
    ```

3. Create and activate a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  (on mac)
    ```

4. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

5. Start MongoDB (if not already running):
    ```sh
    brew services start mongodb-community (on mac)
    ```

6. Run the FastAPI application:
    ```sh
    uvicorn app.main:app --reload
    ```

The application will be running at `http://127.0.0.1:8000`.

The Swagger docs will be available at `http://127.0.0.1:8000/docs`.

## Development

- To modify the file summary extraction logic, update the `summary_service.py` file.
- To update the file model or database schema, modify the `file_model.py` file.

## Acknowledgements

- FastAPI for building the API
- MongoDB for database management
- Predibase for text summarization
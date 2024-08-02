from pydantic import BaseModel, Field
from bson import ObjectId
import uuid


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")


class FileModel(BaseModel):
    file_id: str = Field(..., alias="_id")
    file_name: str
    file_summary: str


class FileUploadResponse(BaseModel):
    file_id: str
    file_name: str
    file_summary: str

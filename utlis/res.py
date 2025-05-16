
from typing import Any, Dict
from fastapi.responses import JSONResponse
from bson import ObjectId
from pydantic import BaseModel
from datetime import datetime

class MyResponse(BaseModel):
    success: bool
    error: str
    message: str
    content: Any



class DotDict:
    def __init__(self, dictionary: Dict[str, Any]):
        self.__dict__ = dictionary

def create_success_response(status_code,content: Dict[str, Any]) -> JSONResponse:
    return JSONResponse(
        status_code=status_code or 200,
        content=content
    )

def create_error_response(error: str) -> JSONResponse:
    """Create a standardized error response."""
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": error,
            "message": "Error processing request",
            "content": {}
        }
    )

def convert_objectid_to_str(data):
    if isinstance(data, list):
        return [convert_objectid_to_str(item) for item in data]
    elif isinstance(data, dict):
        return {key: convert_objectid_to_str(value) for key, value in data.items()}
    elif isinstance(data, ObjectId):
        return str(data)
    elif isinstance(data, datetime):
        return data.isoformat()
    else:
        return data
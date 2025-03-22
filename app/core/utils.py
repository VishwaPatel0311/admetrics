import typing
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
import constants
from core.error_code import err

def create_response(data: dict):
    return {"data": data, "status": constants.SUCCESS_STATUS_CODE}

def create_error_response(error: int = 100, msg: str = None):
    message = err[error]
    if msg:
        for arg in msg:
            message += str(arg)
    data = {"error_code": error, "error_message": message}
    status = "failure"
    return {"data": data, "status": status}


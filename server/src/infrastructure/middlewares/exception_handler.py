from httpx import HTTPStatusError
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from infrastructure.exception import ValidationException


async def generic_request_exception_handler(request: Request, exc: HTTPStatusError):
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'message': str(exc)})


async def selenium_not_found_element_exception_handler(request: Request, exc: HTTPStatusError):
    error_message = str(exc).split("\n")[0]
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'message': error_message})


async def validation_exception_handler(request: Request, exc: ValidationException):
    return JSONResponse(
        status_code=400,
        content={"message": f"Validation error: {exc.message}"}
    )
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from loguru import logger
from pydantic import ValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.routers import calculate, exceptions


async def handle_exceptions(request: Request, call_next):
    try:
        return await call_next(request)

    except Exception as e:
        logger.error(msg := f'Internal Server Error: {e}')
        return JSONResponse(content={'error': msg}, status_code=500)


logger.remove()
logger.add(sink='logs/app_{time}.log')

app = FastAPI()
app.middleware('http')(handle_exceptions)
app.include_router(calculate.router)
app.include_router(exceptions.router)


@app.exception_handler(RequestValidationError)
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    logger.error(f'Validation error!\n\t{exc}')
    return JSONResponse({'error': str(exc)}, status_code=400)

from pydantic import BaseModel


class ErrorResponseDto(BaseModel):
    error: str

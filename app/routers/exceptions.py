from fastapi import APIRouter

from app.models.error import ErrorResponseDto

router = APIRouter(tags=['Exception'])


@router.get(
    '/exception',
    response_model=ErrorResponseDto,
    responses={500: {'model': ErrorResponseDto, 'description': 'Internal Server Error'}}
)
async def deposit(q: str):
    raise Exception(q)

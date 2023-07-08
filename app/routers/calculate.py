import datetime

from fastapi import APIRouter
from loguru import logger

from app.models.calculate.deposit import DepositRequestDto, DATE_FORMAT, DepositResponseDto
from app.models.error import ErrorResponseDto

router = APIRouter(prefix='/calculate', tags=['Calculate'])


@router.post(
    '/deposit',
    response_model=None,
    responses={
        400: {'model': ErrorResponseDto, 'description': 'Request error'},
        500: {'model': ErrorResponseDto, 'description': 'Server Error'},
        200: {
            'description': 'Successful calculate',
            'model': DepositResponseDto,
            'content': {
                'application/json': {
                    'example': {
                        '31.01.2021': 10050.0,
                        '28.02.2021': 10100.25,
                        '31.03.2021': 10150.75,
                        '30.04.2021': 10201.51,
                        '31.05.2021': 10252.51,
                        '30.06.2021': 10303.78,
                        '31.07.2021': 10355.29
                    },
                }
            }
        }
    }
)
async def deposit(request: DepositRequestDto):
    result: dict = {}

    logger.info(f'Calculating Deposit...\n\t{request}')

    for _ in range(request.periods):
        request.date = get_date_last_day_of_month(request.date)
        request.amount += calculate_income_from_period(amount=request.amount, rate=request.rate)
        result[request.date.strftime(DATE_FORMAT)] = round(request.amount, 2)
        request.date = (request.date + datetime.timedelta(days=1))

    logger.success(f'Finish Calculate\n\t{result}')

    return result


def get_date_last_day_of_month(date: datetime.date) -> datetime.date:
    """Получить дату последнего дня месяца

    Args:
        date: Дата от которой будет считаться дата последнего дня месяца
    """
    next_month = date.replace(day=4) + datetime.timedelta(days=28)
    return next_month - datetime.timedelta(days=next_month.day)


def calculate_income_from_period(amount: int | float, rate: float) -> float:
    """Высчитать прибыль для одного месяца

    Args:
        amount: Текущий депозит
        rate: Годовая процентная ставка
    """
    return amount * (rate / 12 / 100)

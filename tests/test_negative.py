from allure import dynamic, epic, feature, step, story, title
from fastapi.testclient import TestClient
from loguru import logger
from pydantic import ValidationError
from pytest import mark, raises

from app.models.calculate.deposit import DepositRequestDto
from tests.allure_constants import AllureConstants


@epic(AllureConstants.Epic.CALCULATE)
@feature(AllureConstants.Feature.DEPOSIT)
@story(AllureConstants.Story.NEGATIVE)
class TestNegativeDeposit:

    @staticmethod
    @mark.parametrize(
        'amount, periods, rate, date, title_, error',
        [
            (9_999, 2, 1.0, '02.03.2008', 'deposit <', 'is greater than or equal to 10000'),
            (3_000_001, 2, 1.0, '02.03.2008', 'deposit >', 'is less than or equal to 3000000'),
            (3_000_000, 0, 8.0, '15.07.2021', 'period <', 'is greater than or equal to 1'),
            (3_000_000, 61, 8.0, '15.07.2021', 'period >', 'is less than or equal to 60'),
            (10_000, 60, 2.0, '32.13.2021', 'date (day)', "does not match format '%d.%m.%Y'"),
            (10_000, 60, 2.0, '31.13.2021', 'date (moth)', "does not match format '%d.%m.%Y'"),
            (10_000, 60, 0.9, '31.12.2021', 'rate <', 'is greater than or equal to 1'),
            (10_000, 60, 8.1, '31.12.2021', 'rate >', 'is less than or equal to 8'),
        ]
    )
    def test_negative(api: TestClient, amount: int, periods: int, rate: float, date: str, title_: str, error: str):
        dynamic.title(f'Incorrect {title}')

        with raises(ValidationError) as e:
            DepositRequestDto(amount=amount, periods=periods, rate=rate, date=date)
            logger.success(f'Модель отработала\n\t{e}')

        with step('Отправить запрос с неверными данными'):
            response = api.post(
                url='/calculate/deposit',
                json=dict(amount=amount, periods=periods, rate=rate, date=date)
            )
            assert response.status_code == 400
            assert error in response.json()['error']

    @staticmethod
    @title('DepositRequestDto validator date')
    def test_validator_deposit_dto():
        with raises(ValueError) as e:
            DepositRequestDto(amount=10_000, rate=2.0, periods=20, date=1)
            assert e.value == 'Date must be str! Format: dd.mm.YYYY'

    @staticmethod
    def test_unhandled_exceptions(api: TestClient):
        response = api.get(url='/exception', params={'q': 'Test Exception'})
        assert response.status_code == 500
        assert response.json()['error'] == 'Internal Server Error: Test Exception'

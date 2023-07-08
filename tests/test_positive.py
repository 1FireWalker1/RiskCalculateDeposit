import datetime

from allure import epic, feature, step, title
from fastapi.testclient import TestClient
from pytest import mark
from random import randint

from app.models.calculate.deposit import DepositRequestDto, DATE_FORMAT
from tests.allure_constants import AllureConstants


@epic(AllureConstants.Epic.CALCULATE)
@feature(AllureConstants.Feature.DEPOSIT)
@epic(AllureConstants.Story.POSITIVE)
class TestDepositPositive:

    @staticmethod
    @title('Валидные значения, граничные + рандомные')
    @mark.parametrize('amount', [10_000, 3_000_000, randint(10_000, 3_000_000)])
    @mark.parametrize('periods', [1, 60, randint(1, 60)])
    @mark.parametrize('rate', [1.0, 8.0, float(randint(1, 8))])
    @mark.parametrize('date', ['28.02.2000', '15.03.1999', '01.01.2019'])
    def test_positive_cases(api: TestClient, amount: int, periods: int, rate: float, date: str):
        with step('Отправить запрос на расчёт депозита'):
            response = api.post(
                url='/calculate/deposit',
                json=(dto := DepositRequestDto(amount=amount, periods=periods, rate=rate, date=date)).dict()
            )
            assert response.status_code == 200

        with step('Провалидировать расчёт'):
            date_prev, deposit_prev = (content := response.json()).popitem()

            for _ in range(len(content)):
                date_str, deposit = content.popitem()

                date_current, date_prev = map(lambda x: datetime.datetime.strptime(x, DATE_FORMAT), [date_str, date_prev])

                assert (date_current - date_prev).days < 31
                assert abs(round((deposit_prev - deposit) / deposit_prev * 100, 4) - round(dto.rate / 12, 4)) < 0.005
                date_prev, deposit_prev = date_str, deposit

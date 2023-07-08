from datetime import date

from allure import epic, feature, story, title
from pytest import mark

from app.routers.calculate import get_date_last_day_of_month, calculate_income_from_period
from tests.allure_constants import AllureConstants


@epic(AllureConstants.Epic.CALCULATE)
@feature(AllureConstants.Feature.DEPOSIT)
@story(AllureConstants.Story.TOOLS)
class TestDepositTools:

    @staticmethod
    @title('Last day of the current month')
    @mark.parametrize(
        'date_in, expected',
        [
            (date(day=1, month=1, year=1999), date(day=31, month=1, year=1999)),
            (date(day=31, month=12, year=2000), date(day=31, month=12, year=2000)),
            (date(day=15, month=6, year=2010), date(day=30, month=6, year=2010)),
            (date(day=4, month=2, year=2100), date(day=28, month=2, year=2100)),
        ]
    )
    def test_get_last_day_of_month(date_in: date, expected: date):
        assert get_date_last_day_of_month(date=date_in) == expected

    @staticmethod
    @title('Calculate income from period')
    @mark.parametrize(
        'amount, rate, expected',
        [
            (10_000, 1.0, 8.33),
            (10_000, 8.0, 66.67),
            (3_000_000, 4.43, 11_075),
        ]
    )
    def test_calculate_income_from_period(amount, rate, expected):
        assert round(calculate_income_from_period(amount=amount, rate=rate), 2) == expected

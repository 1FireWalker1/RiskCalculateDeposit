import datetime

from pydantic import BaseModel, confloat, conint, validator

DATE_FORMAT = '%d.%m.%Y'


class DepositRequestDto(BaseModel):
    amount: conint(strict=True, ge=10_000, le=3_000_000)
    date: datetime.date
    periods: conint(strict=True, ge=1, le=60)
    rate: confloat(strict=True, ge=1, le=8)

    @validator('date', pre=True)
    def date_validate_format(cls, date: str) -> datetime.date:
        if not isinstance(date, str):
            raise ValueError('Date must be str! Format: dd.mm.YYYY')

        return datetime.datetime.strptime(date, DATE_FORMAT).date()

    def dict(self, *args, **kwargs):
        self.date = self.date.strftime(DATE_FORMAT)
        return super().dict(*args, **kwargs)


class DepositResponseDto(BaseModel):
    __root__: dict[str, float]

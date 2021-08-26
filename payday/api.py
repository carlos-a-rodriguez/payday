"""payday APIs"""
import datetime
from functools import lru_cache
from typing import Generator, List

from dateutil.rrule import MONTHLY, rrule
import numpy as np

from payday.lib.holidays.bank import USBankHolidays


def adjusted_date(date: datetime.date) -> datetime.date:
    """date adjusted for weekends and holidays"""
    return np.busday_offset(
        dates=date,
        offsets=0,
        roll="preceding",
        holidays=bank_holidays(date.year),
    ).astype(datetime.date)


@lru_cache(maxsize=16)
def bank_holidays(year: int) -> List[datetime.date]:
    """all the bank holidays for a given year"""
    return [holiday for holiday in USBankHolidays(years=[year]).keys()]


def is_pay_day(date: datetime.date) -> bool:
    """is date a pay day?"""
    return next_pay_day(date) == date


def next_pay_day(date: datetime.date) -> datetime.date:
    """next pay day from the date provided (inclusive)"""
    return next(pay_days_gen(date=date))


def pay_days_gen(date: datetime.date) -> Generator[datetime.date, None, None]:
    """all pay days from start (inclusive)"""
    for dt in rrule(freq=MONTHLY, bymonthday=(15, -1), dtstart=date):
        if (pay_day := adjusted_date(dt.date())) >= date:
            yield pay_day

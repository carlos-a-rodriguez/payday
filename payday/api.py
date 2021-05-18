"""payday APIs"""
import datetime
from typing import Generator

from dateutil.rrule import MONTHLY, rrule
import numpy as np

from payday.lib.holidays.bank import USBankHolidays


BANK_HOLIDAYS = USBankHolidays()


def adjusted_date(date: datetime.datetime) -> datetime.date:
    """ date adjusted for weekends and holidays """
    return np.busday_offset(
        dates=date.strftime("%Y-%m-%d"),
        offsets=0,
        roll="preceding",
        holidays=bank_holidays(date.year),
    ).astype(datetime.date)


def bank_holidays(year: int) -> [datetime.date]:
    """ all the bank holidays for a given year """
    _ = datetime.date(year=year, month=1, day=1) in BANK_HOLIDAYS  # cache holidays
    return [holiday for holiday in BANK_HOLIDAYS.keys()]


def pay_days_gen(start: datetime.date) -> Generator[datetime.date, None, None]:
    """ all pay days from start (inclusive) """
    for pay_day in rrule(freq=MONTHLY, bymonthday=(15, -1), dtstart=start):
        yield adjusted_date(pay_day)


def is_pay_day(date: datetime.date) -> bool:
    """ is date a pay day? """
    for pay_day in pay_days_gen(start=date):
        return date == pay_day

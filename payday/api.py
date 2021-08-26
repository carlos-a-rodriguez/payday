"""payday APIs"""
import datetime
from itertools import dropwhile
from typing import Generator, List, Optional

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


def bank_holidays(year: int) -> List[datetime.date]:
    """all the bank holidays for a given year"""
    return [holiday for holiday in USBankHolidays(years=[year]).keys()]


def is_pay_day(date: datetime.date) -> bool:
    """is date a pay day?"""
    return next_pay_day(date) == date


def next_pay_day(date: datetime.date) -> datetime.date:
    """next pay day from the date provided (inclusive)"""
    return next(pay_days_gen(start=date))


def pay_days_gen(
    start: datetime.date,
    until: Optional[datetime.date] = None,
) -> Generator[datetime.date, None, None]:
    """generator for pay days from start and stopping at until"""
    iterator = dropwhile(
        lambda date: date < start, adjusted_pay_days_gen(start, until)
    )

    for date in iterator:
        yield date


def adjusted_pay_days_gen(
    start: datetime.date, until: Optional[datetime.date] = None
) -> Generator[datetime.date, None, None]:
    """pay day (adjusted for weekends and holidays) generator"""
    for date in unadjusted_pay_days_gen(start, until):
        yield adjusted_date(date)


def unadjusted_pay_days_gen(
    start: datetime.date, until: Optional[datetime.date] = None
) -> Generator[datetime.date, None, None]:
    """unadjusted pay day generator"""
    for dt in rrule(
        freq=MONTHLY, bymonthday=(15, -1), dtstart=start, until=until
    ):
        yield dt.date()

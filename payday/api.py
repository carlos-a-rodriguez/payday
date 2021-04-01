"""payday APIs"""
import calendar
import datetime
from typing import Generator, Tuple

import dateutil.rrule
import numpy as np

from payday.lib.holidays.bank import USBankHolidays


MID_MONTH_DAY = 15


def adjusted_eom_pay_day(year: int, month: int) -> datetime.date:
    return np.busday_offset(
        unadjusted_eom_pay_day(year, month).strftime("%Y-%m-%d"),
        0,
        roll="preceding",
        holidays=us_bank_holidays(year),
    ).astype(datetime.date)


def adjusted_mom_pay_day(year: int, month: int) -> datetime.date:
    return np.busday_offset(
        unadjusted_mom_pay_day(year, month).strftime("%Y-%m-%d"),
        0,
        roll="preceding",
        holidays=us_bank_holidays(year),
    ).astype(datetime.date)


def eom_day(year: int, month: int) -> int:
    _, day = calendar.monthrange(year, month)
    return day


def us_bank_holidays(year: int) -> np.ndarray:
    holidays = USBankHolidays(years=[year])
    return np.array(
        [
            np.datetime64(
                date.strftime("%Y-%m-%d")
            )
            for date, _ in holidays.items()
        ]
    )


def unadjusted_mom_pay_day(year: int, month: int) -> datetime.date:
    return datetime.date(year, month, day=MID_MONTH_DAY)


def unadjusted_eom_pay_day(year: int, month: int) -> datetime.date:
    return datetime.date(
        year,
        month,
        eom_day(year, month)
    )


def _is_pay_day(date: datetime.date) -> bool:
    if date.day > MID_MONTH_DAY:
        return date == adjusted_eom_pay_day(date.year, date.month)
    return date == adjusted_mom_pay_day(date.year, date.month)


def _backward_pay_day_generator(date: datetime.date) -> Generator[datetime.date, None, None]:
    # current month
    for pay_day in reversed(pay_days(date.year, date.month)):
        if pay_day < date:
            yield pay_day

    # previous months
    while date.year >= datetime.date.min.year:
        date -= datetime.timedelta(days=date.day)
        yield adjusted_eom_pay_day(date.year, date.month)
        yield adjusted_mom_pay_day(date.year, date.month)


def _forward_pay_day_generator(date: datetime.date) -> Generator[datetime.date, None, None]:
    # current month
    for pay_day in pay_days(date.year, date.month):
        if pay_day > date:
            yield pay_day

    # subsequent months
    start = datetime.date(date.year, date.month, day=1)
    for dt in dateutil.rrule.rrule(freq=dateutil.rrule.MONTHLY, dtstart=start):
        yield adjusted_mom_pay_day(dt.year, dt.month)
        yield adjusted_eom_pay_day(dt.year, dt.month)


def _next_pay_day(date: datetime.date) -> datetime.date:
    return next(
        _forward_pay_day_generator(date)
    )


def _previous_pay_day(date: datetime.date) -> datetime.date:
    return next(
        _backward_pay_day_generator(date)
    )


def is_pay_day(date: datetime.date) -> bool:
    return _is_pay_day(date)


def next_pay_day(date: datetime.date) -> datetime.date:
    return _next_pay_day(date)


def pay_days(year: int, month: int) -> Tuple[datetime.date, datetime.date]:
    return (
        adjusted_mom_pay_day(year, month),
        adjusted_eom_pay_day(year, month)
    )


def previous_pay_day(date: datetime.date) -> datetime.date:
    return _previous_pay_day(date)

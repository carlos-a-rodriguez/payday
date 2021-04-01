"""payday APIs"""
import calendar
import datetime
from typing import Generator, Iterator, Tuple

import dateutil.relativedelta
import dateutil.rrule
import numpy as np

from payday.lib.holidays.bank import USBankHolidays


MID_MONTH_DAY = 15


def _adjusted_month_end_pay_day(year: int, month: int) -> datetime.date:
    return np.busday_offset(
        _unadjusted_month_end_pay_day(year, month).strftime("%Y-%m-%d"),
        0,
        roll="preceding",
        holidays=_us_bank_holidays(year),
    ).astype(datetime.date)


def _adjusted_mid_month_pay_day(year: int, month: int) -> datetime.date:
    return np.busday_offset(
        _unadjusted_mid_month_pay_day(year, month).strftime("%Y-%m-%d"),
        0,
        roll="preceding",
        holidays=_us_bank_holidays(year),
    ).astype(datetime.date)


def _last_day_of_month(year: int, month: int) -> int:
    _, day = calendar.monthrange(year, month)
    return day


def _us_bank_holidays(year: int) -> np.ndarray:
    holidays = USBankHolidays(years=[year])
    return np.array(
        [
            np.datetime64(
                date.strftime("%Y-%m-%d")
            )
            for date, _ in holidays.items()
        ]
    )


def _unadjusted_mid_month_pay_day(year: int, month: int) -> datetime.date:
    return datetime.date(year, month, day=MID_MONTH_DAY)


def _unadjusted_month_end_pay_day(year: int, month: int) -> datetime.date:
    return datetime.date(
        year,
        month,
        _last_day_of_month(year, month)
    )


def _is_pay_day(date: datetime.date) -> bool:
    if date.day > MID_MONTH_DAY:
        return date == _adjusted_month_end_pay_day(date.year, date.month)
    return date == _adjusted_mid_month_pay_day(date.year, date.month)


def _backward_pay_day_generator(date: datetime.date) -> Generator[datetime.date, None, None]:
    # current month
    for pay_day in reversed(pay_days(date.year, date.month)):
        if pay_day < date:
            yield pay_day

    # previous months
    while date.year >= datetime.date.min.year:
        date -= datetime.timedelta(days=date.day)
        yield _adjusted_month_end_pay_day(date.year, date.month)
        yield _adjusted_mid_month_pay_day(date.year, date.month)


def _forward_pay_day_generator(date: datetime.date) -> Generator[datetime.date, None, None]:
    # current month
    for pay_day in pay_days(date.year, date.month):
        if pay_day > date:
            yield pay_day

    # subsequent months
    start = date + dateutil.relativedelta.relativedelta(months=1, day=1)
    for dt in dateutil.rrule.rrule(freq=dateutil.rrule.MONTHLY, dtstart=start):
        yield _adjusted_mid_month_pay_day(dt.year, dt.month)
        yield _adjusted_month_end_pay_day(dt.year, dt.month)


def pay_day_iter(date: datetime.date, days=1, reverse=False) -> Iterator[datetime.date]:
    generator = _backward_pay_day_generator(date) if reverse else _forward_pay_day_generator(date)
    return iter(
        next(generator)
        for day in range(days)
    )


def is_pay_day(date: datetime.date) -> bool:
    return _is_pay_day(date)


def next_pay_day(date: datetime.date) -> datetime.date:
    return next(
        pay_day_iter(date, days=1, reverse=False)
    )


def pay_days(year: int, month: int) -> Tuple[datetime.date, datetime.date]:
    return (
        _adjusted_mid_month_pay_day(year, month),
        _adjusted_month_end_pay_day(year, month)
    )


def previous_pay_day(date: datetime.date) -> datetime.date:
    return next(
        pay_day_iter(date, days=1, reverse=True)
    )

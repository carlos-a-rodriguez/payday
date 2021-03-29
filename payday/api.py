"""payday APIs"""
import calendar
import datetime
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


def _next_pay_day(date: datetime.date) -> datetime.date:
    mom_pay_day = adjusted_mom_pay_day(date.year, date.month)
    if date < mom_pay_day:  # TODO: what happens if today is a pay day?
        return mom_pay_day
    return adjusted_eom_pay_day(date.year, date.month)


def _previous_pay_day(date: datetime.date) -> datetime.date:
    mom_pay_day = adjusted_mom_pay_day(date.year, date.month)
    if date > mom_pay_day:  # TODO: what happens if today is a pay day?
        return mom_pay_day
    pre_eom_day = mom_pay_day - datetime.timedelta(days=mom_pay_day.day)
    return adjusted_eom_pay_day(pre_eom_day.year, pre_eom_day.month)


def is_pay_day(date: datetime.date) -> bool:
    return _is_pay_day(date)


def next_pay_day(date: datetime.date) -> datetime.date:
    return _next_pay_day(date)


def previous_pay_day(date: datetime.date) -> datetime.date:
    return _previous_pay_day(date)

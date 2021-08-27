# payday

Generate pay day schedule.

## Installation

```commandline
pip install git+https://github.com/carlos-a-rodriguez/payday.git
```

## Info

- Two dates per month
    - 15th
    - End of Month
- If date falls on weekend or holiday, previous non-holiday weekday is chosen
- Uses U.S. federal holidays

## Usage

Check whether a particular date is a pay day or not:

```shell
>>> import datetime
>>> import payday
>>> payday.is_pay_day(datetime.date(2021, 5, 7))
False
>>> payday.is_pay_day(datetime.date(2021, 5, 14))
True
```

Ask for the next pay day starting from a specified date (inclusive):

```shell
>>> import datetime
>>> import payday
>>> payday.next_pay_day(datetime.date(2021, 5, 28))
datetime.date(2021, 5, 28)
>>> payday.next_pay_day(datetime.date(2022, 3, 2))
datetime.date(2022, 3, 15)
```

Generate the next 5 pay days starting from a particular date (inclusive):

```shell
>>> import datetime
>>> import payday
>>> generator = payday.pay_days_gen(datetime.date(2021, 1, 1))
>>> for _ in range(5):
...     next(generator)
... 
datetime.date(2021, 1, 15)
datetime.date(2021, 1, 29)
datetime.date(2021, 2, 12)
datetime.date(2021, 2, 26)
datetime.date(2021, 3, 15)
```

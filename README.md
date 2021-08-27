# payday

Python library to calculate pay dates. There are two pay days per month: the first on the 15th of the month and the
second on the last day of the month. Should the date fall on a weekend or holiday, the previous non-holiday business
date is chosen.

## Installation

```commandline
pip install https://github.com/carlos-a-rodriguez/payday.git
```

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
>>> payday.next_pay_day(datetime.date.today())
datetime.date(2021, 5, 28)
>>> payday.next_pay_day(datetime.date(2022, 3, 2))
datetime.date(2022, 3, 15)
```

Generate the next 5 pay days starting from a particular date (inclusive):

```shell
>>> import datetime
>>> import payday
>>> generator = payday.pay_days_gen(datetime.date(2021, 5, 16))
>>> for _ in range(5):
...   next(generator)
datetime.date(2021, 5, 28)
datetime.date(2021, 6, 15)
datetime.date(2021, 6, 30)
datetime.date(2021, 7, 15)
datetime.date(2021, 7, 30)
```

# payday

Python library to calculate pay dates. There are two pay days per month: the first on the 15th of the month and the
second on the last day of the month. Should the date fall on a weekend or holiday, the previous non-holiday business
date is chosen.

## Installation

```commandline
pip install https://gitlab.com/carlos_rodriguez/payday.git
```

## Usage

There are two main functions. The first checks whether the specified date is a pay day or not.

```shell
>>> import datetime
>>> import payday
>>> payday.is_pay_day(datetime.date(2021, 5, 7))
False
>>> payday.is_pay_day(datetime.date(2021, 5, 14))
True
```

The second is a pay day generator.

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
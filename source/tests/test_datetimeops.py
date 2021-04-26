from datetime import datetime

from source.logic.datetime_ops import DatetimeOps


def test_check_day():
    date1 = datetime.strptime('2021-04-25 08:00:00', '%Y-%m-%d %H:%M:%S')
    date2 = datetime.strptime('2021-04-26 08:00:00', '%Y-%m-%d %H:%M:%S')
    result1 = DatetimeOps().check_day(date1)
    result2 = DatetimeOps().check_day(date2)
    assert result1 == 'w'
    assert result2 == 'Work'


def test_date_converter():
    str_date = '2021-04-26 08:00:00'
    date_obj = datetime.strptime('2021-04-26 08:00:00', '%Y-%m-%d %H:%M:%S')
    result = DatetimeOps().date_converter(str_date)
    assert result == date_obj
    assert type(result) == datetime


def test_calc_worktime(one_day_rows):
    expected = 37625
    result = DatetimeOps().calc_work_time(one_day_rows)
    assert result.seconds == expected


def test_convert_seconds():
    seconds1 = 3600
    expected1 = '01:00:00'
    seconds2 = 1234
    expected2 = '00:20:34'
    result1 = DatetimeOps().convert_seconds(seconds1)
    result2 = DatetimeOps().convert_seconds(seconds2)
    assert result1 == expected1
    assert result2 == expected2

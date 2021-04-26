import datetime

from source.logic.data_ops import DataOps


def test_validate_data(list_of_files):
    results = [DataOps().validate_data(f) for f in list_of_files]
    expected = [True, True, False, False]
    assert results == expected


def test_split_lines():
    line = '2019-02-04 09:05:58 ;Reader entry;E/0/KD1/7-9'
    expected = ['2019-02-04 09:05:58 ', 'Reader entry', 'E/0/KD1/7-9']
    result = DataOps().split_lines(line)
    assert result == expected


def test_get_unique_dates(single_file):
    expected = ['2019-02-06', '2019-02-07']
    result = DataOps().get_unique_dates(single_file)
    assert result == expected


def test_match_dates_lines(single_file):
    expected = [
        {'date': '2019-02-06',
         'lines': [['2019-02-06 09:21:57 ', 'Reader entry', 'E/0/KD1/7-9'],
                   ['2019-02-06 09:22:27 ', 'Reader entry', 'E/3/KD1/3-8'],
                   ['2019-02-06 12:07:06 ', 'Reader exit', 'E/3/KD1/3-8'],
                   ['2019-02-06 12:07:54 ', 'Reader entry', 'E/0/KD1/7-8'],
                   ['2019-02-06 12:23:43 ', 'Reader entry', 'E/0/KD1/7-9'],
                   ['2019-02-06 12:24:31 ', 'Reader entry', 'E/3/KD1/3-8'],
                   ['2019-02-06 16:09:44 ', 'Reader exit', 'E/0/KD1/8-8']]},
        {'date': '2019-02-07',
         'lines': [['2019-02-07 09:09:57 ', 'Reader entry', 'E/0/KD1/7-9'],
                   ['2019-02-07 09:10:27 ', 'Reader entry', 'E/3/KD1/3-8'],
                   ['2019-02-07 10:56:26 ', 'Reader exit', 'E/3/KD1/3-8'],
                   ['2019-02-07 10:57:18 ', 'Reader entry', 'E/0/KD1/7-8'],
                   ['2019-02-07 11:05:01 ', 'Reader entry', 'E/0/KD1/7-9'],
                   ['2019-02-07 11:06:40 ', 'Reader exit', 'E/2/KD1/4-8'],
                   ['2019-02-07 12:33:01 ', 'Reader entry', 'E/3/KD1/3-8'],
                   ['2019-02-07 18:33:50 ', 'Reader exit', 'E/0/KD1/7-8']]}]
    result = DataOps().match_dates_lines(single_file)
    assert result == expected


def test_check_overtime():
    worktime1 = 5*3600
    worktime2 = 8*3600
    worktime3 = 10*3600
    result1 = DataOps().check_overtime(worktime1)
    result2 = DataOps().check_overtime(worktime2)
    result3 = DataOps().check_overtime(worktime3)
    assert result1 == 'ut'
    assert result2 == ''
    assert result3 == 'ot'


def test_line_generator():
    date = {'date': '2019-02-04',
            'lines': [['2019-02-04 09:05:58 ', 'Reader entry', 'E/0/KD1/7-9'],
                      ['2019-02-04 09:07:03 ', 'Reader entry', 'E/3/KD1/3-8'],
                      ['2019-02-04 17:32:34 ', 'Reader exit', 'E/3/KD1/3-8'],
                      ['2019-02-04 19:33:03 ', 'Reader exit', 'E/0/KD1/7-8']]}
    last_record = False
    results = []
    result = DataOps().line_generator(date, last_record, results)
    expected = 'Day 2019-02-04 Work 10:27:05 ot'
    assert result == expected


def test_calc_weekly_time():
    week_number = 6
    results = [
        {'date': datetime.datetime(2019, 2, 4, 0, 0), 'week_number': 6,
         'work_time': datetime.timedelta(seconds=37625), 'overtime': 8825},
        {'date': datetime.datetime(2019, 2, 5, 0, 0), 'week_number': 6,
         'work_time': datetime.timedelta(seconds=22562), 'overtime': -6238},
        {'date': datetime.datetime(2019, 2, 6, 0, 0), 'week_number': 6,
         'work_time': datetime.timedelta(seconds=24467), 'overtime': -4333},
        {'date': datetime.datetime(2019, 2, 7, 0, 0), 'week_number': 6,
         'work_time': datetime.timedelta(seconds=33833), 'overtime': 5033}]
    results = DataOps().calc_weekly_time(week_number, results)
    expected = ('32:54:47', '00:54:47')
    assert results == expected

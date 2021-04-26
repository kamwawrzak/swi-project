import pytest


@pytest.fixture
def one_day_rows():
    rows = [['2019-02-04 09:05:58 ', 'Reader entry', 'E/0/KD1/7-9'],
            ['2019-02-04 09:07:03 ', 'Reader entry', 'E/3/KD1/3-8'],
            ['2019-02-04 17:32:34 ', 'Reader exit', 'E/3/KD1/3-8'],
            ['2019-02-04 19:33:03 ', 'Reader exit', 'E/0/KD1/7-8']]
    return rows


@pytest.fixture
def list_of_files():
    files_names = ['test_input1.csv', 'test_input2.csv',
                   'incorrect_input1.csv', 'incorrect_input1.csv']
    files = [open('source/tests/test_files/'+f, 'r') for f in files_names]
    return files


@pytest.fixture
def single_file():
    return open('source/tests/test_files/test_input2.csv', 'r')

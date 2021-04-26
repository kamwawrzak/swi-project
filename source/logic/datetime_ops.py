from datetime import datetime
import sys


class DatetimeOps:

    def check_day(self, date):
        """
        It checks what day of week has been passed to the function and returns
        'w' for Saturday or Sunday and 'Work' for other days.
        :param date: Datetime object
        :return: if its weekend day it returns 'w' otherwise it returns 'Work'
        """
        week_day = date.weekday()
        if week_day in (5, 6):
            return 'w'
        else:
            return 'Work'

    def date_converter(self, str_date):
        """
        It converts date string to Datetime object.
        :param str_date: date string in 'YYYY-MM-DD hh:mm:ss' format
        :return: Datetime object
        """
        if str_date[-1] == ' ':
            str_date = str_date[:-1]
        try:
            date = datetime.strptime(str_date, '%Y-%m-%d %H:%M:%S')
            return date
        except ValueError:
            print(f'Incorrect datetime format. Received date {str_date},'
                  f' required format: YYYY-MM-DD hh:mm:ss')
            sys.exit(1)

    def calc_work_time(self, day_rows):
        """
        It calculates work time by differing time of last and first record for
        specific date.
        :param day_rows: list of all rows for specific date
        :return: datetime object representing work time for specific day
        """
        start_time = DatetimeOps().date_converter(day_rows[0][0])
        end_time = DatetimeOps().date_converter(day_rows[-1][0])
        work_time = end_time - start_time
        if work_time.seconds < 0:
            print('Working time cannot be less than 0. Check if provided work'
                  'data is correct.')
        else:
            return work_time

    def convert_seconds(self, seconds):
        """
        It converts number of seconds to string time.
        :param seconds: int number representing time expressed in seconds
        :return: string showing time in format hh:mm:ss
        """
        hours = seconds // 3600
        seconds = seconds % 3600
        minutes = seconds // 60
        seconds = seconds % 60
        t = f'{hours:02d}:{minutes:02d}:{seconds:02d}'
        return t

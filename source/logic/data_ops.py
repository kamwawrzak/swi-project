import csv
import re

from datetime import datetime

from source.logic.datetime_ops import DatetimeOps

class DataOps:

    def validate_data(self, file):
        """
        It takes csv files and checks if every line matches to pattern and
        stops running program if any line does not match.
        :param file: .csv file
        :return: boolean - True if data are correct, False if any line does not
                 match the pattern.
        """
        pattern = '[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} ' \
                  ';Reader (entry|exit);.+'
        csv_reader = csv.reader(file)
        next(csv_reader)
        line_num = 0
        for line in csv_reader:
            line_num += 1
            check = re.match(pattern, line[0])
            if check is None:
                print(f'Incorrect data format in line {line_num}: {line[0]}')
                file.seek(0)
                return False
            else:
                continue
        file.seek(0)
        return True

    def split_lines(self, line):
        """
        It accepts string of semicolon separated values, splits it and returns
        as list of strings.
        :param line: string of semicolon separated values
        :return: list of values strings
        """
        data = line.split(';')
        return data

    def get_unique_dates(self, file):
        """
        It accepts csv file and returns set of dates from first column of the
        file.
        :param file: .csv file
        :return: sorted set of unique dates in the file
        """
        csv_reader = csv.reader(file, delimiter=';')
        dates = []
        for line in csv_reader:
            if line[0].split(' ')[0] == 'Date':
                continue
            else:
                dates.append(line[0].split(' ')[0])
        return sorted(set(dates))

    def match_dates_lines(self, file):
        """
        It matches lines from passed file to specific dates.
        :param file: .csv file containing records for specific dates
        :return: list of dictionaries containing dates and lists of lines
                 assigned to the dates.
        """
        csv_reader = csv.reader(file, delimiter=';')
        dates = DataOps().get_unique_dates(file)
        file.seek(0)
        all_days_lines = []
        for date in dates:
            day_lines = []
            for line in csv_reader:
                if line[0].split(' ')[0] == date:
                    day_lines.append(line)
            all_days_lines.append({'date': date, 'lines': day_lines})
            file.seek(0)
        return all_days_lines

    def check_overtime(self, work_time):
        """
        It takes work time and returns appropriate flag if overtime or
        undertime occurred.
        :param work_time: work time expressed in seconds
        :return: 'ot' flag for overtime 'ut' flag for undertime
        """
        if work_time/3600 > 9:
            return 'ot'
        elif work_time/3600 < 6:
            return 'ut'
        else:
            return ''

    def line_generator(self, date_lines, if_last, results):
        """
        It takes list of records for specific date, calculates work time and
        work time and save it as dictionary in results list. Also it creates
        line including these information and returns it.
        :param date_lines: list of record for specific date
        :param if_last: boolean flag confirming if its last date in a file
        :param results: list storing data for all dates.
        :return: string presenting all calculated information's
        """
        work_time = DatetimeOps().calc_work_time(date_lines['lines'])
        overtime = work_time.seconds - 8*3600
        date = datetime.strptime(date_lines['date'], '%Y-%m-%d')
        week_number = date.isocalendar()[1]
        day_type = DatetimeOps().check_day(date)
        ot_flag = DataOps().check_overtime(work_time.seconds)
        line = f'Day {date.date()} {day_type} {work_time} {ot_flag}'
        if date_lines['lines'][-1][1] != 'Reader exit':
            line += ' i'
        results.append({'date': date, 'week_number': week_number,
                        'work_time': work_time, 'overtime': overtime})
        if date.weekday() == 4 or if_last:
            totals = DataOps().calc_weekly_time(week_number, results)
            line += ' ' + str(totals[0]) + ' ' + str(totals[1])
        return line

    def calc_weekly_time(self, week_number, results):
        """
        It sums up work time and overtime of all days in specified week.
        :param week_number: int number pointing on week of the year
        :param results: list of calculated data for all dates in the passed
               work time records file
        :return: tuple including total work time and overtime in the specific
                 week
        """
        week_lines = [line for line in results
                      if line['week_number'] == week_number]
        total_work_time = 0
        total_overtime = 0
        for w in week_lines:
            total_work_time += w['work_time'].seconds
            total_overtime += w['overtime']
        total_work_time = DatetimeOps().convert_seconds(total_work_time)
        total_overtime = DatetimeOps().convert_seconds(total_overtime)
        return total_work_time, total_overtime

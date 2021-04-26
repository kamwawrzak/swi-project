import sys

from source.logic.data_ops import DataOps


class FilesOps:

    def generate_all_rows(self, file_path):
        """
        It calculates all required data for all included dates in passed file
        and saves it in results list. Also it generates and returns list of
        strings presenting these data.
        :param: file_path: relative path to file including input data
        :return: List of strings presenting required data
        """
        results = []
        lines = []
        with open(file_path, 'r') as file:
            validated = DataOps().validate_data(file)
            if validated:
                specific_dates_lines = DataOps().match_dates_lines(file)
                last_record = False
                for date in specific_dates_lines:
                    if date == specific_dates_lines[-1]:
                        last_record = True
                    line = DataOps().line_generator(date, last_record, results)
                    lines.append(line)
                return lines
            else:
                sys.exit(1)

    def save_to_file(self, lines):
        """
        It saves all lines generated by the program in separated rows in
        'result' file
        :param lines: list of strings presenting data for all dates
        :return:
        """
        with open('./result', 'w') as file:
            for line in lines:
                file.write(line + '\n')
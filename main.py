from source.logic.files_ops import FilesOps


def main():
    try:
        lines = FilesOps().generate_all_rows('./input.csv')
        FilesOps().save_to_file(lines)
        print('Work times calculated successfully.')
    except FileNotFoundError:
        print('File not found. Check if the file path is correct.')


if __name__ == '__main__':
    main()

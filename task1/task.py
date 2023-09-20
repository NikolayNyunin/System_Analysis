import sys
import argparse
import csv


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('file_path', type=str)
    parser.add_argument('row_index', type=int)
    parser.add_argument('col_index', type=int)

    return parser


def main() -> None:
    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])

    with open(namespace.file_path) as file:
        reader = csv.reader(file)
        print(list(reader)[namespace.row_index][namespace.col_index])


if __name__ == '__main__':
    main()

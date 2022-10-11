import csv
from typing import List


Data = List[List[str]]


def grab_data(file_path: str, column_indices: List[int], delimiter: str = ";", skip_first_row: bool = False) -> Data:
    data = []

    with open(file_path, encoding='utf-8') as f:
        file_reader = csv.reader(f, delimiter=delimiter)

        i = 0
        row: str
        for row in file_reader:
            if not skip_first_row or i > 0:
                try:
                    entries = []
                    for idx in column_indices:
                        entries.append(row[idx])
                    data.append(entries)
                except Exception as err:
                    print(err)
            i += 1

    return data

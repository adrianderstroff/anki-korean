import csv


def grab_data(file_path, fields, delimiter=";", skipFirstRow=False):
    data = []

    with open(file_path, encoding='utf-8') as f:
        file_reader = csv.reader(f, delimiter=delimiter)

        i = 0
        row: str
        for row in file_reader:
            if not skipFirstRow or i > 0:
                try:
                    entries = []
                    for idx in fields:
                        entries.append(row[idx])
                    data.append(entries)
                except Exception as err:
                    print(err)
            i += 1

    return data

import csv

from anki import generate_deck


def grab_data(file_path, fields, delimiter=";", skipFirstRow=False):
    file_reader = csv.reader(file_path, delimiter=delimiter)
    data = []

    i = 0
    row: str
    for row in file_reader:
        if not skipFirstRow or i > 0:
            entries = []
            tokens = delimiter.split(row)
            for idx in fields:
                entries.append(tokens[idx])
            data.append(entries)
        i += 1

    return data


def create_fields():
    return [
            {'name': 'Hanzi'},
            {'name': 'Pinyin'},
            {'name': 'Translation'}
        ]


def create_css():
    css = """
            #answer {
                width: 33%;
            }
            .gap {
                height: 2em;
            }
            .center {
                text-align: center;
            }
            .hanzi {
                font-size: 3em;
            }
            .left {
                margin-left: 10%;
            }
            .space {
                display: inline-block;
                width: 2em;
            }
        """
    return css


def create_template():
    question_page = """
        <div class="center hanzi">{{Hanzi}}</div>
    """

    answer_page = """
        {{FrontSide}}
        <div class="center">{{Pinyin}}</div>
        <div class="gap"></div>
        <hr id="answer">
        <div class="gap"></div>
        <div class="center">{{Translation}}</div>
    """

    return {
        'name': 'HSK: radicals',
        'qfmt': question_page,
        'afmt': answer_page
    }


if __name__ == '__main__':
    csv_path = "data/korean2b.csv"
    file_name = "data/anki-korean2b.apkg"
    data = grab_data(csv_path, [0, 1, 2])
    title = "150 most common radicals"
    fields = create_fields()
    css = create_css()
    template = create_template()

    generate_deck(
        output_file_name=file_name,
        data=data,
        deck_title="Korean 2B",
        deck_id=1234678910,
        model_name="korean",
        model_id=12345678910,
        fields=fields,
        css=css,
        templates=[template]
    )
import re

from src.data import Data
from src.logger import Logger
from src.type import Fields, Template, Model
from src.util import create_id, wrap_template


def create_fields() -> Fields:
    return [
        {'name': 'English'},
        {'name': 'Japanese'},
        {'name': 'Romaji'},
        {'name': 'Explanation'}
    ]


def create_css() -> str:
    css = """
        .card{
            background-color: #e9ebee;
        }
        .question {
            width: calc(100% - 30px - 30px);
            padding: 15px;
            margin-top: 15px;
            margin-left: 15px;
            margin-right: 15px;
            font-size: 2em;
            color: black;
            border-radius: 2px;
        }
        #answer {
            display: none;
        }
        .japanese {
            width: calc(100% - 30px - 30px);
            margin-top: 10px;
            margin-left: 15px;
            margin-right: 15px;
            padding: 15px;
            font-size: 2em;
            color: black;
        }
        .explanation {
            width: calc(100% - 30px - 30px);
            margin-top: 10px;
            margin-left: 15px;
            margin-right: 15px;
            padding: 15px;
            font-size: 1em;
            color: black;
        }
        .center {
            text-align: center;
        }
        rt {
            color: gray;
        }
        .romaji {
            color: gray;
        }
    """
    return css


def create_english_template() -> Template:
    question_page = """
        <div class="center question">{{English}}</div>
    """

    answer_page = """
        {{FrontSide}}
        <hr id="answer">
        <div class="center japanese">{{Japanese}}</div>
        <div class="center romaji">{{Romaji}}</div>
        <div class="explanation">{{Explanation}}</div>
    """

    return wrap_template('English-Japanese', question_page, answer_page)


def check_data(data: Data):
    existing_vocab = {}
    for j, row in enumerate(data):
        # make sure rows have only 4 entries
        if len(row) != 4:
            Logger.error(f'line {j+1}: number of entries is not 4: {row}')

        # check for duplicates
        japanese = row[1]
        if japanese in existing_vocab:
            other = existing_vocab[japanese]
            line = other[0]
            other_vocab = other[1]
            Logger.warn(f'line {j+1}: {row} already existed in {line+1}: {other_vocab}')
        else:
            existing_vocab[japanese] = [j, row]


def extract_furikana(data: Data):
    for j, row in enumerate(data):
        japanese = row[1]

        pattern = r'([\u4e00-\u9faf\u3040-\u309f\u30a0-\u30ff])\[(.*?)\]'
        replacement = lambda m: f"<ruby>{m.group(1)}<rt>{m.group(2)}</rt></ruby>"
        result = re.sub(pattern, replacement, japanese)
        row[1] = result


def remove_dummy_explanation(data: Data):
    for j, row in enumerate(data):
        explanation = row[3]
        if len(explanation) < 2:
            row[3] = ''


def post_process(data: Data):
    check_data(data)
    extract_furikana(data)
    remove_dummy_explanation(data)


def create_model() -> Model:
    return {
        'name': 'japanese',
        'id': create_id('japanese'),
        'gui_field': 1,
        'fields': create_fields(),
        'css': create_css(),
        'template': [create_english_template()],
        'post_process': post_process
    }

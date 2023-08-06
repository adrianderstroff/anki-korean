from colorama import Fore, Style

from src.data import Data
from src.logger import Logger
from src.type import Fields, Template, Model
from src.util import create_id, wrap_template


def create_fields() -> Fields:
    return [
        {'name': 'English'},
        {'name': 'Korean'}
    ]


def create_css() -> str:
    css = """
        @font-face {
            font-family: UhBeeSehyun;
            src: url(./_UhBee-Se_hyun.ttf);
        }
        .card{
            background-color: #e9ebee;
        }
        .question {
            width: calc(100% - 30px - 30px);
            padding: 15px;
            margin-top: 15px;
            margin-left: 15px;
            margin-right: 15px;
            font-size: 1em;
            background: steelblue;
            color: white;
            border-radius: 2px;
        }
        #answer {
            display: none;
        }
        .explanation {
            width: calc(100% - 30px - 30px);
            margin-top: 10px;
            margin-left: 15px;
            margin-right: 15px;
            padding: 15px;
            font-size: 1em;
            color: black;
            background: white;
        }
        .examples-header {
            width: calc(100% - 30px - 4px - 2px);
            height: 1em;
            line-height: 1em;
            margin-top: 40px;
            margin-left: 15px;
            margin-right: 15px;
            padding-left: 2px;
            border-left: 2px solid steelblue;
            border-right: 2px solid steelblue;
            border-bottom: 2px solid steelblue;
            border-top-right-radius: 2px;
            border-top-left-radius: 2px;
            background: steelblue;
            color: white;
            font-size: 1em;
        }
        .examples {
            width: calc(100% - 30px - 4px - 30px);
            margin-left: 15px;
            margin-right: 15px;
            padding: 15px;
            border-top: 1px solid steelblue;
            border-left: 2px solid steelblue;
            border-right: 2px solid steelblue;
            border-bottom: 2px solid steelblue;
            border-bottom-right-radius: 2px;
            border-bottom-left-radius: 2px;
            background: white;
            color: black;
            font-size: 1em;
        }
        .hangeul {
            font-family: UhBeeSehyun;
        }
        .small {
            font-size: 0.7em;
        }
        .center {
            text-align: center;
        }
    """
    return css


def create_english_template() -> Template:
    question_page = """
        <div class="center question">{{English}}</div>
    """

    answer_page = """
        {{FrontSide}}
        <div class="center explanation hangeul">{{Korean}}</div>
    """

    return wrap_template('Travel English-Korean', question_page, answer_page)


def create_korean_template() -> Template:
    question_page = """
        <div class="center question hangeul">{{Korean}}</div>
    """

    answer_page = """
        {{FrontSide}}
        <div class="center explanation">{{English}}</div>
    """

    return wrap_template('Travel Korean-English', question_page, answer_page)


def check_data(data: Data):
    existing_vocab = {}
    for j, row in enumerate(data):
        # make sure rows have only 2 entries
        if len(row) != 2:
            Logger.error(f'line {j+1}: number of entries is not 2: {row}')

        # check if first entry contains only english characters
        contains_korean = False
        for char in row[0]:
            # Get the Unicode code point of the character
            code_point = ord(char)
            # Check if the code point falls within the Korean character ranges
            if (0xAC00 <= code_point <= 0xD7A3) or (0x1100 <= code_point <= 0x11FF) or (0x3130 <= code_point <= 0x318F):
                contains_korean = True
                break
        if contains_korean:
            Logger.error(f'line {j + 1}: first entry contains korean characters: {row}')

        # check for duplicates
        korean = row[1]
        if korean in existing_vocab:
            other = existing_vocab[korean]
            line = other[0]
            other_vocab = other[1]
            Logger.warn(f'line {j+1}: {row} already existed in {line+1}: {other_vocab}')
        else:
            existing_vocab[korean] = [j, row]


def post_process(data: Data):
    check_data(data)


def create_model() -> Model:
    return {
        'name': 'travel-vocab',
        'id': create_id('travel-vocab'),
        'gui_field': 1,
        'fields': create_fields(),
        'css': create_css(),
        'template': [create_english_template(), create_korean_template()],
        'post_process': post_process
    }

from colorama import Fore, Style

from src.data import Data
from src.logger import Logger
from src.type import Fields, Template, Model
from src.util import create_id, wrap_template


def create_fields() -> Fields:
    return [
        {'name': 'English'},
        {'name': 'Korean'},
        {'name': 'Sentences'}
    ]


def create_css() -> str:
    css = """
        @font-face {
            font-family: UhBeeSehyun;
            src: url(./_UhBee-Se_hyun.ttf);
        }
        @font-face {
            font-family: Eunjin;
            src: url(./_eunjinnakseo.ttf);
        }
        @font-face {
            font-family: HoonGothic;
            src: url(./_1HoonGothicgulim-Regular.ttf);
        }
        @font-face {
            font-family: BareunBatang;
            src: url(./_BareunBatang-1Light.ttf);
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
        .hangeul2 {
            font-family: HoonGothic;
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
        <div class="examples-header">Sentences</div>
        <div class="examples">{{Sentences}}</div>
    """

    return wrap_template('English-Korean', question_page, answer_page)


def create_korean_template() -> Template:
    question_page = """
        <div class="center question hangeul">{{Korean}}</div>
    """

    answer_page = """
        {{FrontSide}}
        <div class="center explanation">{{English}}</div>
        <div class="examples-header">Sentences</div>
        <div class="examples">{{Sentences}}</div>
    """

    return wrap_template('Korean-English', question_page, answer_page)


def check_data(data: Data):
    existing_vocab = {}
    for j, row in enumerate(data):
        # make sure rows have only 3 entries
        if len(row) != 3:
            Logger.error(f'line {j+1}: number of entries is not 3: {row}')

        # check for duplicates
        korean = row[1]
        if korean in existing_vocab:
            other = existing_vocab[korean]
            line = other[0]
            other_vocab = other[1]
            Logger.warn(f'line {j+1}: {row} already existed in {line+1}: {other_vocab}')
        else:
            existing_vocab[korean] = [j, row]


def extract_examples(data: Data):
    for j, row in enumerate(data):
        examples = row[2]
        examples_list = examples.split(";")

        result = '<b class="hangeul2">'+examples_list[0]+"</b>" if len(examples_list) > 0 else ""
        for i, example in enumerate(examples_list[1:]):
            if i % 2 == 1:
                result += "<br><br>" + '<b class="hangeul2">'+example+"</b>"
            else:
                result += "<br>" + '<i class="small">'+example+"</i>"
        row[2] = result

        # check if examples were formatted properly
        if len(examples_list) % 2 == 1:
            Logger.error(f'Line {j+1}: Wrong number of example pairs. {len(examples_list)}: {examples_list}')


def post_process(data: Data):
    check_data(data)
    extract_examples(data)


def create_model() -> Model:
    return {
        'name': 'korean',
        'id': create_id('korean'),
        'gui_field': 1,
        'fields': create_fields(),
        'css': create_css(),
        'template': [create_english_template(), create_korean_template()],
        'post_process': post_process
    }

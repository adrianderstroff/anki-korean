from src.util import create_id


def create_fields():
    return [
        {'name': 'English'},
        {'name': 'Korean'},
        {'name': 'Sentence Korean'},
        {'name': 'Sentence English'}
    ]


def create_css():
    css = """
        .card{
            background-color: #c2c1c1;
        }
        .question {
            width: 70%;
            height: 3em;
            margin-top: 15px;
            margin-left: 15%;
            margin-right: 15%;
            font-size: 2em;
            line-height: 3em;
            background: steelblue;
            color: white;
            border-top-right-radius: 15px;
            border-top-left-radius: 15px;
        }
        .dummy {
            width: 70%;
            height: calc(100% - 6em - 30px);
            margin-bottom: 15px;
            margin-left: 15%;
            margin-right: 15%;
            background: white;
            color: white;
            border-bottom-right-radius: 15px;
            border-bottom-left-radius: 15px;
        }
        #answer {
            display: none;
            width: 33%;
            height: 0px;
        }
        .answer {
            width: 70%;
            height: 3em;
            margin-left: 15%;
            margin-right: 15%;
            border-bottom-right-radius: 15px;
            border-bottom-left-radius: 15px;
            font-size: 2em;
            line-height: 3em;
            background: white;
            color: steelblue;
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
        <div class="center question">{{English}}</div>
        <div class="answer"></div>
    """

    answer_page = """
        <div class="center question">{{English}}</div>
        <hr id="answer">
        <div class="center answer">{{Korean}}</div>
        <div class="gap"></div>
        <div class="center">{{Sentence Korean}}</div>
        <div class="center">{{Sentence English}}</div>
    """

    return {
        'name': 'HSK: radicals',
        'qfmt': question_page,
        'afmt': answer_page
    }


def create_model():
    return {
        'name': 'korean',
        'id': create_id('korean'),
        'fields': create_fields(),
        'css': create_css(),
        'template': create_template()
    }
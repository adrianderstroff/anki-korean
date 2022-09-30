from src.util import create_id


def create_fields():
    return [
        {'name': 'Grammar'},
        {'name': 'Explanation'},
        {'name': 'Examples'}
    ]


def create_css():
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
            font-size: 0.7em;
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
            font-size: 0.5em;
        }
        .center {
            text-align: center;
        }
    """
    return css


def create_template():
    question_page = """
        <div class="center question hangeul">{{Grammar}}</div>
    """

    answer_page = """
        {{FrontSide}}
        <div class="explanation">{{Explanation}}</div>
        <div class="examples-header">Examples</div>
        <div class="examples">{{Examples}}</div>
    """

    return {
        'name': 'Korean Grammar',
        'qfmt': question_page,
        'afmt': answer_page
    }


def create_media_files():
    return [
        {
            'paths': [
                './assets/_UhBee-Se_hyun.ttf',
                './assets/_eunjinnakseo.ttf',
                './assets/_1HoonGothicgulim-Regular.ttf',
                './assets/_BareunBatang-1Light.ttf',
            ]
        }
    ]


def create_model():
    return {
        'name': 'korean-grammar',
        'id': create_id('korean-grammar'),
        'fields': create_fields(),
        'css': create_css(),
        'template': create_template(),
        'media': create_media_files()
    }
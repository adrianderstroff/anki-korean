from src.util import create_id


def create_fields():
    return [
        {'name': 'English'},
        {'name': 'Korean'},
        {'name': 'Sentences'}
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
        .answer {
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


def create_english_template():
    question_page = """
        <div class="center question">{{English}}</div>
    """

    answer_page = """
        {{FrontSide}}
        <div class="center answer hangeul">{{Korean}}</div>
        <div class="examples-header">Sentences</div>
        <div class="examples">{{Sentences}}</div>
    """

    return {
        'name': 'English-Korean',
        'qfmt': question_page,
        'afmt': answer_page
    }


def create_korean_template():
    question_page = """
        <div class="center question hangeul">{{Korean}}</div>
    """

    answer_page = """
        {{FrontSide}}
        <div class="center answer">{{English}}</div>
        <div class="examples-header">Sentences</div>
        <div class="examples">{{Sentences}}</div>
    """

    return {
        'name': 'Korean-English',
        'qfmt': question_page,
        'afmt': answer_page
    }


def extract_examples(data):
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

        # check if examples were formated properly
        if len(examples_list) % 2 == 1:
            print(f'Line {j+1}: Wrong number of example pairs. {len(examples_list)}: {examples_list}')


def create_model():
    return {
        'name': 'korean',
        'id': create_id('korean'),
        'gui_field': 1,
        'fields': create_fields(),
        'column_indices': create_fields(),
        'css': create_css(),
        'template': [create_english_template(), create_korean_template()],
        'post_process': extract_examples
    }

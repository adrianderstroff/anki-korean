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
        @font-face {
            font-family: UhBeeSehyun;
            src: url(./UhBee-Se_hyun.ttf);
        }
        @font-face {
            font-family: Eunjin;
            src: url(./eunjinnakseo.ttf);
        }
        .card{
            background-image: url("bg5.jpg");
            background-color: white;
            background-repeat: no-repeat;
            background-size: 100% 140%;
        }
        .question {
            width: calc(100% - 30px);
            height: 2.5em;
            margin-top: 15px;
            margin-left: 15px;
            margin-right: 15px;
            font-size: 1.5em;
            line-height: 2.5em;
            background: steelblue;
            color: white;
            border-top-right-radius: 5px;
            border-top-left-radius: 5px;
        }
        #answer {
            display: none;
            width: 33%;
            height: 0px;
        }
        .answer {
            width: calc(100% - 30px - 4px);
            height: 2.5em;
            margin-left: 15px;
            margin-right: 15px;
            border: 2px solid steelblue;
            border-top: none;
            border-bottom-right-radius: 5px;
            border-bottom-left-radius: 5px;
            font-size: 1.5em;
            line-height: 2.5em;
            color: steelblue;
            background: rgba(255, 255, 255, 0.5);
            backdrop-filter: blur(4px);
        }
        .sentence-header {
            width: calc(100% - 30px - 4px - 2px);
            height: 1.4em;
            line-height: 1.4em;
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
            font-size: 0.9em;
        }
        .sentence1 {
            width: calc(100% - 30px - 4px - 10px);
            height: 2.5em;
            margin-left: 15px;
            margin-right: 15px;
            padding-left: 10px;
            line-height: 2.5em;
            border-left: 2px solid steelblue;
            border-right: 2px solid steelblue;
            background: rgba(255, 255, 255, 0.5);
            backdrop-filter: blur(4px);
            color: black;
        }
        .sentence2 {
            width: calc(100% - 30px - 4px - 10px);
            height: 2.5em;
            margin-left: 15px;
            margin-right: 15px;
            padding-left: 10px;
            line-height: 2.5em;
            border-top: 1px solid steelblue;
            border-left: 2px solid steelblue;
            border-right: 2px solid steelblue;
            border-bottom: 2px solid steelblue;
            border-bottom-right-radius: 2px;
            border-bottom-left-radius: 2px;
            background: rgba(255, 255, 255, 0.5);
            backdrop-filter: blur(4px);
            color: black;
        }
        .hangeul {
            font-family: UhBeeSehyun;
        }
        .hangeul2 {
            font-family: Eunjin;
        }
        .gap {
            height: 2em;
        }
        .center {
            text-align: center;
        }
        .left {
            margin-left: 10%;
        }
        .space {
            display: inline-block;
            width: 2em;
        }
        .bg {
            background-image: url("bg.jpg");
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
        <div class="center answer hangeul">{{Korean}}</div>
        <div class="gap"></div>
        <div class="sentence-header">Sentence</div>
        <div class="sentence1 hangeul2">{{Sentence Korean}}</div>
        <div class="sentence2">{{Sentence English}}</div>
    """

    return {
        'name': 'Korean',
        'qfmt': question_page,
        'afmt': answer_page
    }


def create_model():
    return {
        'name': 'korean',
        'id': create_id('korean'),
        'column_indices': create_fields(),
        'css': create_css(),
        'template': create_template()
    }

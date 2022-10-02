import random
import re

import dash_dangerously_set_inner_html
from dash import Dash, html, dcc, Output, Input, State


def count_matches(matches):
    num = len(matches)
    for match in matches:
        if len(match) == 0:
            num = num - 1
    return num


def extract_line_data(matches):
    tag_name = matches[0]
    tag_attr = matches[1]
    children = matches[2]
    if tag_name != matches[3] and len(matches[3]) > 0:
        print(f"Tags '{tag_name}' and '{matches[3]}' don't match")

    return tag_name, tag_attr, children


def match_element(tag_name):
    # match element
    if tag_name == "div":
        elem = html.Div
    elif tag_name == "hr":
        elem = html.Hr
    elif tag_name == "h1":
        elem = html.H1
    elif tag_name == "h2":
        elem = html.H2
    elif tag_name == "h3":
        elem = html.H3
    elif tag_name == "h4":
        elem = html.H4
    elif tag_name == "h5":
        elem = html.H5
    elif tag_name == "h6":
        elem = html.H6
    else:
        print(f"No match for tag '{tag_name}', used Div instead")
        elem = html.Div

    return elem


def match_attributes(tag_attr):
    pattern = '([^> =]+\s*=\s*"[^>"]+")'
    matches = re.findall(pattern, tag_attr)
    attributes = {}
    for match in matches:
        pattern = '([^> =]+)\s*=\s*"([^>"]+)"'
        m = re.findall(pattern, match)
        if len(m) == 0:
            print(f"No match found for tag '{match}'")
        if len(m[0]) != 2:
            print(f"Match doesn't have exactly 2 entries {m[0]}. Ignored.")
            continue
        attributes[m[0][0]] = m[0][1]
    return attributes


def process_children(children_info, content):
    pattern = '{{([^{}]+)}}'

    children_out = children_info
    while True:
        matches = re.search(pattern, children_out)
        if not matches:
            break

        placeholder = children_out[matches.start(1):matches.end(1)]
        replacement = content[placeholder] if placeholder in content else ""
        start = children_out[:matches.start(1)-2]
        end = children_out[matches.end(1)+2:]

        if placeholder == "FrontSide":
            children_out = replacement
            break
        else:
            children_out = start + replacement + end

    return children_out


def add_children(children):
    return dash_dangerously_set_inner_html.DangerouslySetInnerHTML(children)


def construct_result_element(elem, className, elemID, style, children):
    if className and elemID:
        if len(children) > 0:
            result = elem(className=className, id=elemID, style=style, children=add_children(children))
        else:
            result = elem(className=className, id=elemID, style=style)
    elif className:
        if len(children) > 0:
            result = elem(className=className, style=style, children=add_children(children))
        else:
            result = elem(className=className, style=style)
    elif elemID:
        if len(children) > 0:
            result = elem(id=elemID, style=style, children=add_children(children))
        else:
            result = elem(id=elemID, style=style)
    else:
        if len(children) > 0:
            result = elem(style=style, children=add_children(children))
        else:
            result = elem(style=style)
    return result


def parse_line(line: str, content):
    pattern = '<([^> ]+)\s*(\s*[^> ]+\s*=\s*"[^>]+")?\s*>(?:([^<>]*)<\/\s*([^> ]+)\s*>)?'
    matches = re.findall(pattern, line)

    if len(matches) == 0:
        return process_children(line, content)

    # extract infos to create the tag together with its attributes and content
    tag_name, tag_attr, children_info = extract_line_data(matches[0])

    # grab the right dash element
    elem = match_element(tag_name)

    # extract the tag attributes like class name, id and style
    attributes = match_attributes(tag_attr)
    className = attributes["class"] if "class" in attributes else None
    elemID = attributes["id"] if "id" in attributes else None
    style = {key: val for key, val in attributes.items() if key != "class" and key != "id"}

    # process children
    children = process_children(children_info, content)

    # construct the actual element
    result = construct_result_element(elem, className, elemID, style, children)

    return result


def create_card(data, fields, question_template: str, answer_template: str):
    # create content dict for lookup of data that should be replaced
    content = {}
    for i in range(len(fields)):
        if i < len(data):
            content[fields[i]['name']] = data[i]

    # parse all lines of the front template, we assume there will be only one element per line and no nesting is allowed
    elements_front = []
    for line in iter(question_template.splitlines()):
        line = line.strip()
        if len(line) == 0:
            continue
        elements_front.append(parse_line(line, content))

    # add info about front card
    content["FrontSide"] = elements_front

    # parse all lines of the back template, we assume there will be only one element per line and no nesting is allowed
    elements_back = []
    for line in iter(answer_template.splitlines()):
        line = line.strip()
        if len(line) == 0:
            continue
        children = parse_line(line, content)
        if isinstance(children, list):
            elements_back.extend(children)
        else:
            elements_back.append(children)

    return elements_front, elements_back


def get_both_card_sides(data, fields, question, answer, card_idx):
    card_idx = card_idx if card_idx >= 0 else random.randint(0, len(data) - 1)
    card = data[card_idx]
    return create_card(card, fields, question, answer)


def show_card_preview(data, fields, template, css, card_idx=-1):
    template = template[0] if isinstance(template, list) else template
    question = template['qfmt']
    answer = template['afmt']

    # for simplicity create a file containing the css
    with open('assets/.temp.css', 'w') as f:
        f.write(css)

    app = Dash(__name__)

    app.layout = html.Div(id="app", children=[
        html.Div(id="card-container", children=[
            dcc.Store(id='show_front'),
            html.Div(id="card", className="card"),
        ]),
        html.Button(id="switch", children="SHOW ANSWER")
    ])

    # grab a single card, if no index is provided then grab a random card
    question_card, answer_card = get_both_card_sides(data, fields, question, answer, card_idx)
    sides = {
        'front': question_card,
        'back': answer_card
    }

    @app.callback(
        Output('card', 'children'),
        Output('show_front', 'data'),
        Output('switch', 'children'),
        Input('switch', 'n_clicks'),
        State('show_front', 'data')
    )
    def update_geometry(n_clicks, show_front):
        show_front = show_front if show_front is not None else True
        if show_front:
            sides['front'], sides['back'] = get_both_card_sides(data, fields, question, answer, card_idx)
        card = sides['front'] if show_front else sides['back']
        title = 'SHOW ANSWER' if show_front else 'NEXT CARD'
        return card, not show_front, title

    app.run_server(debug=True)


if __name__ == '__main__':
    data = ["e-mail", "이메일", "이메일 주소가 어떻게 되세요?", "What’s your email address?"]
    fields = ["English", "Korean", "Sentence Korean", "Sentence English"]
    question = """
        <div class="center">{{English}}</div>
    """
    answer = """
        {{FrontSide}}
        <hr>
        <div class="center">{{Korean}} {{Korean}}</div>
        <div>{{Sentence Korean}}</div>
        <div>{{Sentence English}}</div>
    """
    template = {
        'qfmt': question,
        'afmt': answer
    }
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
    show_card_preview(data, fields, template, css)

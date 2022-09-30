import os
import random
from pathlib import Path

from anki import generate_deck
from src.data import grab_data
from src.models import korean, grammar
from src.preview import show_card_preview
from src.util import create_id


def generate(data_path, columns, title, model, func=None):
    # generate output path
    file_name = Path(data_path).stem
    out_path = f'../data/{file_name}.apkg'

    # extract data and apply some post-processing if necessary
    data = grab_data(data_path, columns, delimiter='\t')
    if func:
        func(data)

    generate_deck(
        output_file_name=out_path,
        data=data,
        deck_title=title,
        deck_id=create_id(title),
        model=model
    )


def preview(data_path, columns, model, card_idx=-1, func=None):
    # extract data and apply some post-processing if necessary
    data = grab_data(data_path, columns, delimiter='\t')
    if func:
        func(data)

    # display the card preview
    show_card_preview(data, model['fields'], model['template'], model['css'], card_idx)


def extract_examples(data):
    for row in data:
        examples = row[2]
        examples_list = examples.split(";")

        result = '<b class="hangeul2">'+examples_list[0]+"</b>" if len(examples_list) > 0 else ""
        for i, example in enumerate(examples_list[1:]):
            if i % 2 == 1:
                result += "<br><br>" + '<b class="hangeul2">'+example+"</b>"
            else:
                result += "<br>" + '<i class="small">'+example+"</i>"
        row[2] = result


def vocab_model():
    csv_path = "../data/korean2b.csv"
    deck_title = "Korean 2B"
    columns = [0, 1, 2, 3]
    model = korean.create_model()

    generate(csv_path, columns, deck_title, model)
    preview(csv_path, columns, model)


def grammar_model():
    csv_path = "../data/grammar2b.tsv"
    deck_title = "Korean Grammar 2B"
    columns = [1, 2, 3]
    model = grammar.create_model()

    generate(csv_path, columns, deck_title, model, func=extract_examples)
    preview(csv_path, columns, model, func=extract_examples)


if __name__ == '__main__':
    grammar_model()

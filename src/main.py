import os
from pathlib import Path

from anki import generate_deck
from src.data import grab_data
from src.models import korean
from src.preview import show_card_preview
from src.util import create_id


def generate(data_path, columns, title, model):
    file_name = Path(data_path).stem
    out_path = f'../data/{file_name}.apkg'

    data = grab_data(data_path, columns, delimiter='\t')

    generate_deck(
        output_file_name=out_path,
        data=data,
        deck_title=title,
        deck_id=create_id(title),
        model_name=model['name'],
        model_id=model['id'],
        fields=model['fields'],
        css=model['css'],
        templates=[model['template']]
    )


def preview(data_path, columns, model, card_idx=0):
    data = grab_data(csv_path, columns, delimiter='\t')
    card = data[card_idx]
    show_card_preview(card, model['fields'], model['template'], model['css'])


if __name__ == '__main__':
    csv_path = "../data/korean2b.csv"
    deck_title = "Korean 2B"
    columns = [0, 1, 2, 3]
    model = korean.create_model()

    preview(csv_path, columns, model)
    # generate(csv_path, columns, deck_title, model)
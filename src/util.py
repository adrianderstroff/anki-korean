import hashlib
from pathlib import Path

from anki import generate_deck
from src.data import grab_data
from src.preview import show_card_preview


def extract_data(data_path, columns, model):
    data = grab_data(data_path, columns, delimiter='\t')
    if 'post_process' in model:
        model['post_process'](data)
    return data


def generate(data, data_path, title, model):
    # generate output path
    file_name = Path(data_path).stem
    out_path = f'../data/apkg/{file_name}.apkg'

    generate_deck(
        output_file_name=out_path,
        data=data,
        deck_title=title,
        deck_id=create_id(title),
        model=model
    )


def preview(data, model, card_idx=-1):
    # display the card preview
    show_card_preview(data, model['name'], model['fields'], model['template'], model['css'], card_idx)


def sdbm_hash_string(str):
    h = 0
    m = (1 << 32)
    for i in str:
        t = h
        h = (t << 6) % m + (t << 16) % m - t + ord(i)
        h %= m
    return h


def create_id(name):
    result = hashlib.md5(str.encode(name))
    numbers = result.hexdigest()
    numbers = sdbm_hash_string(numbers)
    return numbers

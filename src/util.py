import hashlib
from pathlib import Path
from typing import List

from anki import generate_deck
from src.data import grab_data, Data
from src.preview import show_card_preview
from src.type import Model, Template


def extract_data(data_path: str, columns: List[int], model: Model) -> Data:
    print(' ├── Grab Data')
    data = grab_data(data_path, columns, delimiter='\t')
    if 'post_process' in model:
        print(' ├── Perform Post Processing')
        model['post_process'](data)
    return data


def generate(data: Data, data_path: str, title: str, model: Model):
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
    # print(f'Generated "{title}" at {out_path}')


def preview(data: Data, model: Model, card_idx: int = -1):
    # display the card preview
    show_card_preview(data, model['name'], model['fields'], model['template'], model['css'], card_idx)


def sdbm_hash_string(name: str) -> int:
    h = 0
    m = (1 << 32)
    for i in name:
        t = h
        h = (t << 6) % m + (t << 16) % m - t + ord(i)
        h %= m
    return h


def create_id(name: str) -> int:
    result = hashlib.md5(str.encode(name))
    numbers = result.hexdigest()
    numbers = sdbm_hash_string(numbers)
    return numbers


def wrap_template(name: str, question: str, answer: str) -> Template:
    return {
        'name': name,
        'qfmt': question,
        'afmt': answer
    }

import random
import re
import csv
import codecs
import genanki

from src.data import Data
from src.type import Model


def row_iterator(csv_file, delimiter: str = ';', skip: bool = True, num: int = -1):
    file_reader = csv.reader(csv_file, delimiter=delimiter)
    i = 0
    for row in file_reader:
        if not skip or i > 0:
            yield row
        i += 1
        if 0 <= num < i:
            break


def generate_deck(output_file_name: str, data: Data, deck_title: str, deck_id: int, model: Model):
    # extract variables
    model_name = model['name']
    model_id = model['id']
    gui_field = model['gui_field']
    fields = model['fields']
    css = model['css']
    templates = model['template'] if isinstance(model['template'], list) else [model['template']]
    media_files = model['media'] if 'media' in model else None

    # generate card model
    card_model = genanki.Model(
        model_id,
        model_name,
        fields=fields,
        templates=templates,
        css=css
    )

    # create deck
    new_deck = genanki.Deck(deck_id, deck_title)

    # create media package
    package = genanki.Package(new_deck)
    if media_files:
        media_file_paths = [p for media_file in media_files for p in media_file['paths']]
        media_templates = {media_file['field']: media_file['template'] for media_file in media_files if 'field' in media_file}
        package.media_files = media_file_paths

    # only use the first field for the guid
    class MyNote(genanki.Note):
        @property
        def guid(self):
            return genanki.guid_for(self.fields[gui_field])

    # add notes to deck
    for row in data:
        # we assume all medial fields come after the content fields
        if len(row) < len(fields) and media_templates:
            new_row = [el for el in row]
            for field in fields[len(row):]:
                new_row.append(media_templates[field['name']])
            row = new_row

        note = MyNote(
            model=card_model,
            fields=row
        )
        new_deck.add_note(note)

    # finally create package
    package.write_to_file(output_file_name)

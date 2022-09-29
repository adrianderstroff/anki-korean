import random
import re
import csv
import codecs
import genanki


def row_iterator(csv_file, delimiter=';', skip=True, num=-1):
    file_reader = csv.reader(csv_file, delimiter=delimiter)
    i = 0
    for row in file_reader:
        if not skip or i > 0:
            yield row
        i += 1
        if 0 <= num < i:
            break


def generate_deck(output_file_name, data, deck_title, deck_id,  model_name, model_id, fields, css, templates):
    # generate card model
    card_model = genanki.Model(
        model_id,
        model_name,
        fields=fields,
        templates=templates,
        css=css
    )

    # create deck and add notes
    new_deck = genanki.Deck(deck_id, deck_title)
    for row in data:
        note = genanki.Note(
            model=card_model,
            fields=row
        )
        new_deck.add_note(note)

    # finally create package
    genanki.Package(new_deck).write_to_file(output_file_name)

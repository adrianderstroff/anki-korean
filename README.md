# anki-korean
Generate Anki Decks for studying Korean.

## 1 How to make a custom deck

Making a simple custom deck involves three steps. **First** you need to provide a csv or tsv file that contains the content of your fields as rows. **Second** you have to create a model. Create a model in the _src/models_ folder. The model describes the appearance of the cards. It optionally provides the paths to all media files that should be shiped with the deck. For reference please refer to the existing models (_grammar.py_ and _korean.py_). **Lastly** add a convenience function in _main.py_ similar to ```def vocab_model()``` or ```def grammar_model()```.

### 1.1 Create the Data
Simply generate a csv or tsv file and put it into the folder _data/tsv_. The file should be formated in a way that each row contains all necessary fields for one card of the deck. The file can contain more fields than you'll actually use in the deck, also the order of the fields in the file doesn't need to be in any certain order. You will specify which fields to use and in which order to use them in **1.3**.

### 1.2 Defining the Model
The model should is a dictionary containing the following fields

| key          | description                                                                                                                  | mandatory |
|--------------|------------------------------------------------------------------------------------------------------------------------------|-----------|
| name         | Name of the note type                                                                                                        | Yes       |
| id           | Unique note ID, this is used by Anki to identify which notes should be updated.                                              | Yes       |
| gui_field    | Index of which card field should be used to identify a card. Should be unique among all cards                                | Yes       |
| fields       | A list of the field names used in the card template.                                                                         | Yes       |
| css          | CSS styling that should be applied to the html elements specified in the card template                                       | Yes       |
| template     | A list of card templates. Its a list because one might want cards for both directions (English->Korean and Korean->English). | Yes       | 
| post process | A function that can be applied to the data once it's loaded. It can be need to apply custom styling to the card data.        | No        |
| media        | Contains a list to all media files like sounds, fonts, images that should be bundeled with the deck                          | No        |

An example can be seen here as taken from _korean.py_
```python
{
    'name': 'korean',
    'id': create_id('korean'),
    'gui_field': 1,
    'fields': create_fields(),
    'css': create_css(),
    'template': [create_english_template(), create_korean_template()],
    'post_process': post_process
}
```
For more information refer to the model files in _src/models_.

### 1.3 Helper Function to Generate the Model Description

Lastly we need to specify which file to load, which fields to grab from the data from step **1.1** and in which order the fields should be extracted. The number and order of the fields have to match with the order of the fields in the model in **1.2** (e.g ```model['fields']```). This should be done by adding a new function in _main.py_. An example for the Korean model can be seen here

```python
def vocab_model() -> ModelDescription:
    csv_path = "../data/tsv/korean2a.csv"
    deck_title = "Korean Vocab 2A"
    columns = [1, 2, 3]
    model = korean.create_model()
    return csv_path, deck_title, columns, model
```

First we specify the path to the csv file that we want to use for our cards. Next we specify the title of the deck. This name will be shown in Anki's deck overview. Next we specify the column that should be extracted for the cards. Here we have a card model with three fields namely _English, Korean, Sentences_, therefore we need to make sure that we extract these fields from the file in the right order. We then import the model that we created in step **1.2**. All of these variables are then returned in the order we defined them. Make sure to return them in exactly this order else the next step won't work.

```python
if __name__ == '__main__':
    generate_and_preview(vocab_model)
```

Lastly pass your newly defined function as a parameter to the function ```generate_and_preview(...)```. You are now done. You can execute the script and an Anki package should now be created in the directory _data/apkg_. This package file can then be imported in Anki.


## 2 About the Data

The vocabulary and grammar are mostly taken from vocabulary of my Korean class. Currently I'm studying with the **서울대 한국어 2A** student and work books. The example sentences used in the vocabulary and grammar decks are mostly taken from the [Naver Korean-English Dictionary](korean.dict.naver.com/). The dictionary offers example sentence submitted by people which is quite neat.

You can use my decks without any restrictions, however take note that the fonts that I used might have a different licensing model.
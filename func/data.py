import json

def read_text(datei_name):
    with open (datei_name) as open_file:
        file_content = open_file.read()
    return file_content

with open('daten/saved_drinks.json', 'r') as f:
    drinks = json.load(f)
    print(drinks)




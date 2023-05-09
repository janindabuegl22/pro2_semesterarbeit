import json


def read_text(datei_name):
    with open (datei_name) as open_file:
        file_content = open_file.read()
    return file_content

def read_text_lines():
    with open ("test.txt") as open_file:
        file_content = open_file.readlines()
    return file_content

def write_txt(datei_name):
    with open(datei_name, "w") as open_file:
        open_file.write("banana")

def danger(datei_name):
    with open(datei_name, "w") as open_file:
        print("irgendwas")

with open('daten/saved_drinks.json', 'r') as f:
    drinks = json.load(f)
    print(drinks)




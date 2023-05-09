from json import dumps, loads

def read(file_name):
    with open (file_name, encoding="UTF8") as open_file:
        content = open_file.read()
        json_content = loads(content)
    return json_content

def write(file_name, key, inhalt):
    json_inhalt = read(file_name)
    json_inhalt[key] = inhalt
    with open(file_name, "w", encoding="UTF8") as open_file:
        json_str = dumps(json_inhalt, indent=4)
        open_file.write(json_str)


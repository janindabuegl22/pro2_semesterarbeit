from json import dumps, loads

with open('daten/datensatz.json', encoding="utf8") as open_file:
    content = open_file.read()
    datensatz = loads(content)

datensatz['vorname'] = "Jan"
datensatz['ort'] = "Chur"

with open("daten/datensatz.json", "w", encoding="utf8") as open_file:
    json_str = dumps(datensatz, indent=4)
    open_file.write(json_str)

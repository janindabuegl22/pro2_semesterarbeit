from datetime import datetime
from operator import itemgetter
from flask import Flask, render_template, request, url_for, redirect
import random
import plotly.express as px
from plotly.offline import plot
import json
from func.datenbank import read, write
app = Flask(__name__)

latest_drink_record = {}

@app.route("/home", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        selected_drink = request.form.get("drink")
        drink_count = get_drink_count(selected_drink)
        return render_template("index.html", drink=selected_drink, count=drink_count)
    else:
        drinkoftheday = random.choice(["Bier", "Gin Tonic", "Braulio", "Rotwein", "Weisswein", "Wasser"])
        beer_count = get_drink_count("Bier")
        return render_template("index.html", drinkoftheday=drinkoftheday, bier_counter=beer_count)

def get_drink_count(drink):
    with open('daten/saved_drinks.json', 'r') as file:
        drinks_data = json.load(file)
    drink_count = sum(int(d['anzahl']) for data in drinks_data.values() for d in data['getraenke'] if d['art'] == drink)
    return drink_count

@app.route("/neue_eingabe", methods=["GET", "POST"])
def eingabe():
    global latest_drink_record

    if request.method == "POST":
        groesse = request.form.get('groesse')  # Wert des Formularfelds 'groesse' abrufen
        gewicht = request.form.get('gewicht')  # Wert des Formularfelds 'gewicht' abrufen
        alter = request.form.get('alter')  # Wert des Formularfelds 'alter' abrufen
        start = request.form.get('start')  # Wert des Formularfelds 'start' abrufen
        end = request.form.get('end')  # Wert des Formularfelds 'end' abrufen
        anzahl = request.form.getlist('anzahl[]')  # Liste der Werte des Formularfelds 'anzahl[]' abrufen
        art = request.form.getlist('art[]')  # Liste der Werte des Formularfelds 'art[]' abrufen

        if groesse and gewicht and alter and start and end and all(anzahl) and all(art): # Überprüfung, ob alle Felder ausgefüllt sind
            getraenke_list = [] # Erstellen einer neuen Liste, um diese mit den Getränken zu füllen und diese zusammen an daten zu senden (unten)
            for i in range(4):
                if anzahl[i] and art[i]:
                    getraenke_list.append({ # Hier wird die Liste gefüllt
                        "anzahl": anzahl[i],
                        "art": art[i]
                    })
            daten = {
                "groesse": groesse,
                "gewicht": gewicht,
                "alter": alter,
                "start": start,
                "end": end,
                "getraenke": getraenke_list # Hier wird die Liste übergeben
            }
            timestamp = datetime.now() # Zeitstempel erstellen
            # Zeitstempel und Daten an json Datei übergeben. Wird seperat übergeben, damit dict getraenke in dict timestamp ist.
            write('daten/saved_drinks.json', str(timestamp), daten)
            latest_drink_record = daten
            # Durch globale Variable kann der aktualisierte Wert von latest_drink_record an andere Teile des Codes weitergegeben werden
            return redirect(url_for('einzelne'))  # Umleitung zur Route 'einzelne', damit man gleich das Ergebnis der Eingabe sieht
        else:
            return "Bitte alle Felder ausfüllen." # Sollten nicht alle Felder ausgefüllt sein
    return render_template("formular.html", name="Jan", eingabe_url=url_for('eingabe'))
@app.route("/statistik")
def read_saved_drinks():
    drinks = read('daten/saved_drinks.json')    # Lesen der Daten in saved_drinks
    if not drinks:                              # Wenn keine Drinks vorhanden sind, dann wird das returned
        return "No drinks found."
    drinks_stats = get_drinks_stats(drinks)     # Wenn Variabel nicht leer ist, wird get_drink_stats aufgerufen. Das Ergebnis wird an drink_stats gesendet.
    x = [drink_summary['timestamp'] for drink_summary in drinks_stats]  # Variabeln für Graph werden festgelegt. Aus dem dict drink_summary wird eine Variabel genommen. Wird in Zeile 107 hinzugefügt
    y = [drink_summary['total_drinks'] for drink_summary in drinks_stats]  # Variabeln für Graph werden festgelegt. Aus dem dict drink_summary wird eine Variabel genommen. Wird in Zeile 107 hinzugefügt
    fig = px.line(x=x, y=y, labels={"x": "Datum", "y": "Gesamthafte Getränke"})     # Festlegen der Variabeln (verbal)
    div = plot(fig, output_type="div")
    return render_template('statistik.html', drinks_stats=drinks_stats, die_grafik=div)


def get_promille(gewicht, drink):                                       # Wird in Zeile 101 und 122 aufgerufen
    vol = {"Bier": 0.05, "Wein": 0.12, "Sekt": 0.11, "Schnaps": 0.40}   # Die eigentliche Berechnung der Promille
    art = drink['art']                                                  # Gibt den Typen des Getränks an
    anzahl = float(drink['anzahl'])                                     # Gibt die Anzahl der Getränke an
    promille = anzahl * vol[art] * 0.8 / (gewicht * 0.6)                # Berechnet die Promille
    return promille


def get_drinks_stats(drinks):
    drinks_stats = []
    for timestamp, daten in drinks.items():
        total_drinks = 0
        total_promille = 0
        drink_summary = {}
        gewicht = float(daten['gewicht'])
        getraenke = daten['getraenke']
        for drink in getraenke:
            total_drinks += float(drink['anzahl'])
            total_promille += get_promille(gewicht, drink)
        drink_summary['timestamp'] = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f').strftime('%d/%m/%Y')
        drink_summary['start'] = daten['start']
        drink_summary['end'] = daten['end']
        drink_summary['total_drinks'] = total_drinks
        drink_summary['total_promille'] = round(total_promille, 3)
        drinks_stats.append(drink_summary)
    drinks_stats = sorted(drinks_stats, key=itemgetter('timestamp'), reverse=True)
    return drinks_stats


@app.route("/einzelne")
def einzelne():
    global latest_drink_record # Globale Variable wird aufgerufen

    daten = latest_drink_record # Der globalen Variable wird die Bezeichnung Daten zugewiesen. Einfacher zu schreiben unten
    rows = []                   # Es wird eine Liste definiert, die in einzelne.html dann aufgerufen wird
    if daten:                   # Wenn Variable daten einen Wert hat (hat sie, aus latest_drink_record)
        gewicht = float(daten['gewicht'])   # Extrahieren der Daten Gewicht
        uhrzeit = daten['start']            # Extrahieren der Daten Start
        getraenke = daten['getraenke']      # Extrahieren der Daten Getränke
        for drink in getraenke:             # Weil es mehrere Getränke gibt und auch Anzahl verschieden
            promille = get_promille(gewicht, drink)     # Funktion von oben wird hier eingesetzt
            row = [drink['art'], drink['anzahl'], uhrzeit, promille]    # row wird vorbereitet
            rows.append(row)                                            # rows erhält einzelne row
    return render_template('einzelne.html', rows=rows)                  # rows werden übergeben


if __name__ == "__main__":
    app.run(debug=True, port=5001)
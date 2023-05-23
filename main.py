from datetime import datetime
from operator import itemgetter

from flask import Flask, render_template, request, url_for, redirect
import random
import plotly.express as px
from plotly.offline import plot
import plotly.graph_objects as go
import plotly.io as pio
import json


from func.datenbank import read, write

app = Flask(__name__)

latest_drink_record = {}


@app.route("/home")
def index():
    drinkoftheday = ["Bier", "Gin Tonic", "Braulio", "Rotwein", "Weisswein", "Wasser"]
    return render_template("index.html", name="Jan", eingabe_url=url_for('eingabe'), drinkoftheday=random.choice(drinkoftheday))


@app.route("/neue_eingabe", methods=["GET", "POST"])
def eingabe():
    global latest_drink_record

    if request.method == "POST":
        groesse = request.form.get('groesse')
        gewicht = request.form.get('gewicht')
        alter = request.form.get('alter')
        geschlecht = request.form.get('geschlecht')
        start = request.form.get('start')
        end = request.form.get('end')
        anzahl = request.form.getlist('anzahl[]')
        art = request.form.getlist('art[]')

        if groesse and gewicht and alter and geschlecht and start and end and all(anzahl) and all(art):
            getraenke_list = []
            for i in range(4):
                if anzahl[i] and art[i]:
                    getraenke_list.append({
                        "anzahl": anzahl[i],
                        "art": art[i]
                    })
            daten = {
                "groesse": groesse,
                "gewicht": gewicht,
                "alter": alter,
                "geschlecht": geschlecht,
                "start": start,
                "end": end,
                "getraenke": getraenke_list
            }
            timestamp = datetime.now()

            write('daten/saved_drinks.json', str(timestamp), daten)
            latest_drink_record = daten
            return redirect(url_for('einzelne'))  # redirect
        else:
            return "Bitte alle Felder ausfüllen."
    return render_template("formular.html", name="Jan", eingabe_url=url_for('eingabe'))


@app.route("/statistik")
def read_saved_drinks():
    drinks = read('daten/saved_drinks.json')
    if not drinks:
        return "No drinks found."
    drinks_stats = get_drinks_stats(drinks)

    x = [drink_summary['timestamp'] for drink_summary in drinks_stats]
    y = [drink_summary['total_drinks'] for drink_summary in drinks_stats]

    fig = px.line(x=x, y=y, labels={"x": "timestamp", "y": "total_drinks"})
    div = plot(fig, output_type="div")

    return render_template('statistik.html', drinks_stats=drinks_stats, die_grafik=div)


def get_promille(gewicht, drink):
    vol = {"Bier": 0.05, "Wein": 0.12, "Sekt": 0.11, "Schnaps": 0.40}
    art = drink['art']
    anzahl = float(drink['anzahl'])
    promille = anzahl * vol[art] * 0.8 / (gewicht * 0.6)
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
        drink_summary['total_promille'] = total_promille
        drinks_stats.append(drink_summary)
    drinks_stats = sorted(drinks_stats, key=itemgetter('timestamp'), reverse=True)
    return drinks_stats


# def get_drink_list(drinks):
#     drink_list = []
#     for timestamp, daten in drinks.items():
#         gewicht = float(daten['gewicht'])
#         getraenke = daten["getraenke"]
#         for drink in getraenke:
#             anzahl = float(drink['anzahl'])
#             art = drink["art"]
#             promille = get_promille(gewicht, drink)
#             drink_list.append({
#                 "art": art,
#                 "anzahl": anzahl,
#                 "promille": '%.2f' % promille
#             })
#     return drink_list

# def get_avg_promille(drinks):
#     total_promille_dict = {"alles": {"total_promille": 0, "anzahl": 0}}
#     for timestamp, daten in drinks.items():
#         gewicht = float(daten['gewicht'])
#         getraenke = daten["getraenke"]
#         for drink in getraenke:
#             anzahl = float(drink['anzahl'])
#             art = drink["art"]
#             if art not in total_promille_dict:
#                 total_promille_dict[art] = {"total_promille": 0, "anzahl": 0}
#
#             promille = get_promille(gewicht, drink)
#             total_promille_dict[art]["total_promille"] += promille
#             total_promille_dict[art]["anzahl"] += 1
#             total_promille_dict["alles"]["total_promille"] += promille
#             total_promille_dict["alles"]["anzahl"] += 1
#
#     return total_promille_dict

@app.route("/einzelne")
def einzelne():
    global latest_drink_record

    daten = latest_drink_record
    rows = []
    if daten:
        gewicht = float(daten['gewicht'])
        uhrzeit = daten['start']
        getraenke = daten['getraenke']
        for drink in getraenke:
            promille = get_promille(gewicht, drink)
            row = [drink['art'], drink['anzahl'], uhrzeit, promille]
            rows.append(row)
    return render_template('einzelne.html', rows=rows)


@app.route("/graph", methods=['GET'])
def graph():
    with open('daten/saved_drinks.json', 'r') as file: #nicht möglich weil die daten sind nicht in saved_drinks
        data = json.load(file)
    x = []
    y = []
    for key, value in data.items():
        x.append(value['timestamp'])
        y.append(value['total_promille'])
    x = sorted(x)
    fig = px.line(x=x, y=y, labels={"x": "Timestamp", "y": "total_promille"})
    div = plot(fig, output_type="div")
    return render_template(
        'graph.html',
        die_grafik=div)

if __name__ == "__main__":
    app.run(debug=True, port=5001)

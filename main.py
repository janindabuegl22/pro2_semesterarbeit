from datetime import datetime

from flask import Flask, render_template, request, url_for, redirect
import random
import plotly.express as px
from plotly.offline import plot

from func.datenbank import read, write

app = Flask(__name__)


@app.route("/home")
def index():
    tipps = ["Tipp 1", "Tipp 2", "Tipp 3"]
    return render_template("index.html", name="Jan", eingabe_url=url_for('eingabe'), tipp=random.choice(tipps))


@app.route("/neue_eingabe", methods=["GET", "POST"])
def eingabe():
    if request.method == "POST":
        groesse = request.form.get('groesse')
        gewicht = request.form.get('gewicht')
        alter = request.form.get('alter')
        geschlecht = request.form.get('geschlecht')
        mageninhalt = request.form.get('f[stomach]')
        start = request.form.get('start')
        end = request.form.get('end')
        anzahl = request.form.getlist('anzahl[]')
        art = request.form.getlist('art[]')

        if groesse and gewicht and alter and geschlecht and mageninhalt and start and end and all(anzahl) and all(art):
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
                "mageninhalt": mageninhalt,
                "start": start,
                "end": end,
                "getraenke": getraenke_list
            }
            timestamp = datetime.now()

            write('daten/saved_drinks.json', str(timestamp), daten)
            return redirect(url_for('read_saved_drinks'))  # redirect
        else:
            return "Bitte alle Felder ausfüllen."
    return render_template("formular.html", name="Jan", eingabe_url=url_for('eingabe'))


@app.route("/statistik")
def read_saved_drinks():
    drinks = read('daten/saved_drinks.json')
    if not ('daten' in drinks and 'getraenke' in drinks['daten']):
        return "No drinks found."
    gewicht = float(drinks['daten']['gewicht'])
    vol = {"Bier": 0.05, "Wein": 0.12, "Sekt": 0.11, "Schnaps": 0.12}
    drinks_list = get_drink_list(drinks, gewicht, vol)
    avg_promille = get_avg_promille(drinks, gewicht, vol)

    return render_template('statistik.html', drinks=drinks_list, avg_promille=avg_promille, ds_promille=avg_promille["alles"]["total_promille"])

def get_drink_list(drinks, gewicht, vol):
    drink_list = []
    for timestamp, daten in drinks.items():
        getraenke = daten["getraenke"]
        for drink in getraenke:
            anzahl = float(drink['anzahl'])
            art = drink["art"]
            promille = anzahl * vol[art] * 0.8 / (gewicht * 0.6)
            drink_list.append({
                "art": art,
                "anzahl": anzahl,
                "promille": '%.2f' % promille
            })
    return drink_list

def get_avg_promille(drinks, gewicht, vol):
    total_promille_dict = {"alles": {"total_promille": 0, "anzahl": 0}}
    for timestamp, daten in drinks.items():
        getraenke = daten["getraenke"]
        for drink in getraenke:
            anzahl = float(drink['anzahl'])
            art = drink["art"]
            if art not in total_promille_dict:
                total_promille_dict[art] = {"total_promille": 0, "anzahl": 0}

            promille = anzahl * vol[art] * 0.8 / (gewicht * 0.6)
            total_promille_dict[art]["total_promille"] += promille
            total_promille_dict[art]["anzahl"] += 1
            total_promille_dict["alles"]["total_promille"] += promille
            total_promille_dict["alles"]["anzahl"] += 1

    return total_promille_dict

@app.route("/einzelne")
def einzelne():
    drinks = read('daten/saved_drinks.json')
    rows = []
    for timestamp, daten in drinks.items():
        uhrzeit = daten['start']
        getraenke = daten['getraenke']
        for drink in getraenke:
            row = [drink['art'], drink['anzahl'], uhrzeit]
            rows.append(row)
    return render_template('einzelne.html', rows=rows)


@app.route("/graph")
def graph():
    fig = px.line(x=[0, 1, 2, 3, 4], y=[0, 1, 4, 9, 16])
    div = plot(fig, output_type="div")
    return render_template('graph.html', die_grafik=div)


if __name__ == "__main__":
    app.run(debug=True, port=5001)

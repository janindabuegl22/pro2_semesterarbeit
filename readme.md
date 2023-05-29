#  Promillebrille - *Deine Promilledokumentation*


## Warum dieses Projekt
Meine Projektidee umfasst ein Tool, um zu testen, wie viel Alkohol man nach einer gewissen Anzahl Getränke im Blut hat.
Der Grund für dieses Projekt war, eine Plattform zu haben, welche mir anzeigt, wie oft ich Alkohol trinke und wie 
hoch mein Promillewert jeweils ist. 

## Welches Problem löst das Projekt
Das Projekt löst das Problem des Unwissens des Promillewerts, wenn man Alkohol trinkt. Zudem löst es das Problem
fehlender Dokumentation des Alkoholkonsums. 

## Was macht das Projekt
Das Projekt bietet die Möglichkeit, die konsumierten alkoholischen Getränke zu erfassen und zu dokumentieren. Dabei
wird sofort berechnet, wie hoch der aktuelle Promillegehalt im Blut ist. Das Projekt nimmt die Getränke entgegen, 
berechnet den Promillegehalt pro Getränkeart, speichert den Gesamtpromillegehalt und dokumentiert diesen zusammen mit dem 
aktuellen Tagesdatum in einer Tabelle und in einem Graph. 

## Betrieb
Um das Projekt auszuführen, muss die Datei "main.py" ausgeführt werden. Promillebrille verwendet Plotly. Dies muss vor Benutzung 
installiert werden. Sonst wird die Grafik nicht angezeigt. Das Projekt läuft über den Port 5001. 
Wenn auf diesem Port andere Dinge ausgeführt werden, sollte das geändert werden, um Komplikationen zu vermeiden.

## Wie wird das Projekt benutzt

## Welche Optionen oder auch Spezialitäten existieren
zuerst habe ich in main flask importiert: from flask import flask


danach habe ich eine App erstellt und dieses nach meinem Projekt benannt. 
Ein Decorator ist etwas, bei dem ein App davor steht, dann irgend ein Code kommt und darunter die Funktion steht. 
App Decorator sagt "ich mache etwas spezielles mit der Funktion"
Die Funktion im Decorator zeigt, was mit dieser App passiert. So wird in meinem Beispiel Index ausgeführt. 
Ich gebe return und "Hallo Flask" ein, damit dies dann im Browser angezeigt wird. 
@app zeigt mir, wohin das soll
der Link unten zeigt uns, was dort passieren soll. 
Danach habe ich zwei weitere Apps erstellt, die die Seite für eine neue Eingabe und die Seite für die Statistik darstellen. 
Danach habe ich eine Indexdatei mit Html Code erstellt. 
Render Template ist eine Funktion von Flask, die ich importiert habe. 
render_template ist eine Funktion in Flask, die verwendet wird, um eine HTML-Vorlage (Template) mit dynamischen Daten zu rendern und als HTTP-Antwort zurückzugeben.

**jinja codes sind doppelt geschweifte Klammern ({})**
eine Variable namens "Name definitert man im Jinja so: {{ name }}!
Wenn ich Hallo und {{ name }}! im Html Code Index eingebe, wird ein Hallo mit PLatzhalter ausgegeben. 
Ich muss also in der App ein render template mit der Verbindung zum Namen machen (name=Jan).

Danach habe ich eine neue html datei erstellt. Diese soll für das Fenster "Neue Eingabe" dienen. 
In diesem Fenster kann man seinen neusten Alkoholkonsum erfassen. Und es gibt einen sich jeweils ändernden Spruch. 
Danach habe ich ein css dokument erstellt, um den Titel meines Textex grün zu machen. Mit den Daten der Unterrichtsfolien 
habe ich dann copy paste gemacht und den filenamen angepasst. 
Um eine CSS Datei in unser HTML zu laden, müssen wir den Pfad zur CSS-Datei mit dem Befehl url_for erstellen. 
Die url_for-Funktion erstellt eine URL, die auf die Funktion oder den Endpunkt innerhalb der Anwendung verweist, anstatt eine URL manuell zu erstellen oder hartcodiert in den HTML-Code einzufügen. 

Flask verwendet sogenannte Routen, um URLs mit Funktionen in Ihrem Code zu verknüpfen. 
Wenn Sie eine Route definieren, gibt Flask an, welche Funktion aufgerufen werden soll, wenn der Benutzer auf eine bestimmte URL zugreift. In Ihrem Code haben Sie beispielsweise die Route "/neue_eingabe" definiert:

**hallo**
Input gibt uns immer einen String zurück (text)

```mermaid
graph TD;
    A-->B;
    B-->C;
    C-->D;

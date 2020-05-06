# Backend Team

Name | Nickname | Rolle
------------ | ------------ | ------------
Mathis | Block | Teamleitung
Timo | Kohlmeier | Entwickler
Lukas | Hitzemann | Entwickler
Anestis Lalidis | Mateo | Entwickler
Sebastian | Steinmeyer | Entwickler
Julian | Wasilewski | Entwickler

# Einrichtung der Entwicklungsumgebung in VSCode:
- Projekt clonen
- Projektordner in der Konsole öffnen
- Falls nicht vorhanden virtualenv installieren
- Linux: 
```sh
$ python3 -m venv venv
```
- Windows:
```sh
$ python -m venv venv
```
- Projektordner in VSCode öffnen
- Python extension
- Strg+Shift+P "Python: Select Interpreter" auswählen
- Den Interpreter mit der Angabe "venv" auswählen
- Rechtsklick auf den Ordner venv und "Open in Terminal" auswählen
- Linux: 
```sh
$ pip3 install flask
```
- Windows:
```sh
$ pip install flask
```

# Starten der Anwendung:
- In der Konsole ins Hauptverzeichnis des Projekts wechseln
- Setzen von 2 enviroment Variablen
- Linux: 
```sh
$ export FLASK_APP=backend
$ export FLASK_ENV=development
```
- Windows:
```sh
$ set FLASK_APP=backend
$ set FLASK_ENV=development
```
- Nun kann die Anwendung wie folgt genutzt werden
```sh
$ flask <Befehl>
```

# Mögliche Befehle
Befehl | Beschreibung
--- | ---
run | startet das Backend

# Startparameter für run
Parameter | Beschreibung
--- | ---
-h host-ip :text | Angabe der Socket-IP. Mögliche externe IP's können mit ifconfig eingesehen werden.
-p port :integer | Angabe des Socket-Port.

# Backend Team

Name | Nickname | GitHub Nick | Rolle
------------ | ------------ | ------------ | ------------
Mathis | Block | vMysterion | Teamleitung
Timo | Kohlmeier | Wambo04 | Entwickler
Lukas | Hitzemann | Batschko | Entwickler
Anestis Lalidis | Mateo | Nesti024 | Entwickler
Sebastian | Steinmeyer | CrappyAlgorithm | Entwickler
Julian | Wasilewski | JulianWasilewski | Entwickler

# Einrichtung der Entwicklungsumgebung:
- MariaDB 10.x installieren
-- zur besseren Kompatibilität bitte Nutzer="root" und Passwort="softwareprojekt2020" verwenden
-- bei abweichenden Daten muss dies unter backend/util/db.py angepasst werden (bitte nicht commiten!)
- Projekt clonen
- Projektordner in der Konsole öffnen
- Falls nicht vorhanden virtualenv installieren (wird ergänzt falls nötig)
- Virtual Environment anlegen
- Linux: 
```sh
$ python3 -m venv venv
```
- Windows:
```sh
$ python -m venv venv
```
- Virtual Enviroment starten
- Linux:
```sh
$ folgt noch
```
- Windows:
```sh
$ .\venv\Scripts\activate.bat
```
- Nun sollte vor dem Komandozeilenpromt (venv) erscheinen
- Installieren der notwendigen Pakete
- Linux: 
```sh
$ pip3 install flask
$ pip3 install mysql-connector
```
- Windows:
```sh
$ pip install flask
$ pip install mysql-connector
```

# Starten der Anwendung:
- In der Konsole ins Hauptverzeichnis des Projekts wechseln
- Virtual Enviroment starten
- Linux:
```sh
$ folgt noch
```
- Windows:
```sh
$ .\venv\Scripts\activate.bat
```
- Setzen von 2 Enviroment Variablen
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
init-db | initialisiert bzw bereinigt die Datenbank

# Startparameter für run
Parameter | Beschreibung
--- | ---
-h host-ip :text | Angabe der Socket-IP. Mögliche externe IP's können mit ifconfig eingesehen werden.
-p port :integer | Angabe des Socket-Port.

# Backend Team

Name | Nickname | GitHub Nick | Rolle
------------ | ------------ | ------------ | ------------
Mathis | Block | vMysterion | Teamleitung
Timo | Kohlmeier | Wambo04 | Entwickler
Lukas | Hitzemann | Batschko | Entwickler
Anestis Lalidis | Mateo | Nesti024 | Entwickler
Sebastian | Steinmeyer | CrappyAlgorithm | Entwickler
Julian | Wasilewski | JulianWasilewski | Entwickler

# Abhängigkeiten installieren:
- Über pip die requirements.txt als Quelle nutzen, um die Abhängigkeiten zu installieren
```
$ pip install -r requirements.txt
```

# Einrichtung der Entwicklungsumgebung:
- MariaDB 10.x installieren
-- zur besseren Kompatibilität bitte Nutzer="backend" und Passwort="softwareprojekt2020" erstellen
-- bei abweichenden Daten muss dies in der _backend_config.ini_ angepasst werden (bitte nicht commiten!)
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
    $ source venv/bin/activate
    ```
    - Windows:
    ```sh
    $ .\venv\Scripts\activate.bat
    ```
- Nun sollte vor dem Komandozeilenpromt (venv) erscheinen
- Installieren der notwendigen Pakete
    - Linux: 
    ```sh
    $ pip3 install -r requirements.txt
    ```
    - Windows:
    ```sh
    $ pip install -r requirements.txt
    ```

# Starten der Anwendung:
- In der Konsole ins Hauptverzeichnis des Projekts wechseln
- Virtual Enviroment starten
    - Linux:
    ```sh
    $ $ source venv/bin/activate
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

# Raspberry Testumgebung
Bei Fragen bitte an CrappyAlgorithm (Sebastian Steinmeyer) wenden.
## ssh Zugriff 
- falls nicht vorhanden ssh Client installieren (z.B. Putty)

Verbindungsdaten:
```
IP: 84.118.2.15
Port: 222
```

## Backend starten
- Virtual Enviroment wie oben erklärt starten
- fall nötig mit folgendem Befehl die Datenbank bereinigen
```sh
$ flask init-db
```
- Flask starten:
```sh
$ flask run -h 192.168.178.50 
```
- Das Backend ist nun unter folgenden Verbindungsdaten erreichbar:
```
IP: 84.118.2.15
Port: 80
```


# Code linting und Statische Analyse
- Zum testen vor einem PR bitte mit:
    - Linux:
    ```sh
    $ ./CI.sh
    ```
    - Windows:
    ```sh
    $ CI.bat
    ```
    prüfen ob keine Fehler mehr da sind.

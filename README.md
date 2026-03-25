
# Setup

```sh
curl -sSL https://raw.githubusercontent.com/Operators-Diaries/posaune/main/start.sh | bash
```

**Voraussetzungen**

- Python >= 3.12
- Pakete:
    ```sh
    python3 -m pip install -r requirements.txt
    ```
- Startup-Skript (siehe Abschnitt *Starten*)

**Zu beachten**
- Die Option *"Cache deaktivieren"* ist in den Netzwerk-Einstellungen der Entwickler-Tools des Browsers zu **abzuwählen bzw. abgewählt zu lassen**, um Flackern beim Neuladen zu vermeiden
- Es kann sinnvoll sein, browserseitig die Zoomstufe zu erhöhen. Normalerweise speichert der Browser das für eine Domain, sodass es nur einmal eingestellt werden muss. 

# Konfiguration
Nach dem ersten Starten wird eine Datei `config.yaml` mit Standardwerten angelegt. 

Die Konfigurationsparameter werden nur beim Start des Servers ausgelesen.

# Starten
Der Webserver wird einfach durch
```sh
python main.py
```
gestartet.

Es wird eine Website bereitgestellt, die unter
```
http://127.0.0.1:5000/
```
erreichbar ist.
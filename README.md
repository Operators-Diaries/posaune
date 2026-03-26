
<h1 align="center">Posaune</h1>
<h6 align="center">Vertretungsplan-Anzeige für das St. Benno Gymnasium</h6>

<p align="center"><a href="https://operators-diaries.github.io/posaune/">Live-Demo</a></p>

## Setup
**Voraussetzungen**

- Unix-Shell
- Benutzer mit Administratorrechten
- `apt`, `dnf` oder `pacman` Paket-Manager
- `curl`

### Installation
Die Posaune kann per curl heruntergeladen und installiert werden:
```sh
curl -sSL https://raw.githubusercontent.com/Operators-Diaries/posaune/main/start.sh | bash
```
Dafür ist beim ersten Ausführen wahrscheinlich die Eingabe des Systempassworts nötig. (Das Verzeichnis, **in dem dieser Befehl ausgeführt wurde** sei als `~` bezeichnet) Der curl-Befehl erzeugt das Verzeichnis `~/posaune`.

**Zu beachten**
- Die Option *"Cache deaktivieren"* ist in den Netzwerk-Einstellungen der Entwickler-Tools des Browsers **abzuwählen bzw. abgewählt zu lassen**, um Flackern beim Neuladen zu vermeiden
- Es kann sinnvoll sein, browserseitig die Zoomstufe zu erhöhen. Normalerweise speichert der Browser das für eine Domain, sodass es nur einmal eingestellt werden muss. 

## Konfiguration
Nach dem ersten Starten wird eine Datei `~/posaune/config.yaml` mit Standardwerten angelegt. 

Die Konfigurationsparameter werden nur beim Start des Servers ausgelesen.

## Starten
Ein fertiges Start-Skript liegt in `~/posaune/start.sh`. Seine Ausführung muss lediglich als Schedule im System hinterlegt werden - beispielsweise mit `crontab`.
Zu beachten ist, dass das Skript mit `bash` und nicht mit `sh` ausgeführt werden muss.

---

#### Temporäre Alternative für Windows
```
iwr "https://raw.githubusercontent.com/Operators-Diaries/posaune/main/start.ps1" -UseBasicParsing | iex
```
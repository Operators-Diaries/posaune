
<h1 align="center">Posaune</h1>
<h6 align="center">Vertretungsplan-Anzeige für das St. Benno Gymnasium</h6>

<p align="center">
    <a href="https://operators-diaries.github.io/posaune/">Live-Demo</a> - 
    <a href="https://github.com/operators-diaries/posaune?tab=contributing-ov-file">Erläuterung</a>
    <br><br>
    <a href="#"><img alt="Static Badge" src="https://img.shields.io/badge/Flask-x?style=for-the-badge&logo=python&logoColor=ffffff&labelColor=4c75a9&color=161926"></a>
    <!-- <a href="#"><img alt="Static Badge" src="https://img.shields.io/badge/Python-x?style=for-the-badge&logo=python&logoColor=ffffff&color=4c75a9"></a> -->
    <a href="#"><img alt="Static Badge" src="https://img.shields.io/badge/Jinja-x?style=for-the-badge&logo=jinja&logoColor=ffffff&labelColor=a52a22&color=161926"></a>
    <a href="#"><img alt="Static Badge" src="https://img.shields.io/badge/HTMX-x?style=for-the-badge&logo=htmx&logoColor=ffffff&labelColor=E34F26&color=161926"></a>
    <a href="#"><img alt="Static Badge" src="https://img.shields.io/badge/Browser%20JS-x?style=for-the-badge&logo=javascript&logoColor=000000&labelColor=f1df40&color=161926"></a>
</p>


## Setup
**Voraussetzungen**

- Unix-Shell
- Benutzer mit Administratorrechten
- `apt`, `dnf` oder `pacman` Paket-Manager
- `curl`

### Installation
Die Posaune kann per curl heruntergeladen und installiert werden:
```sh
curl -sSL https://raw.githubusercontent.com/Operators-Diaries/posaune/main/scripts/install.sh | bash
```
Dafür ist beim ersten Ausführen wahrscheinlich die Eingabe des Systempassworts nötig. (Das Verzeichnis, **in dem dieser Befehl ausgeführt wurde** sei als `~` bezeichnet) Die Installation erzeugt das Verzeichnis `~/posaune`.

**Zu beachten**
- Die Option *"Cache deaktivieren"* ist in den Netzwerk-Einstellungen der Entwickler-Tools des Browsers **abzuwählen bzw. abgewählt zu lassen**, um Flackern beim Neuladen zu vermeiden
- Es kann sinnvoll sein, browserseitig die Zoomstufe zu erhöhen. Normalerweise speichert der Browser das für eine Domain, sodass es nur einmal eingestellt werden muss. 

## Konfiguration
Nach dem ersten Starten wird eine Datei `~/posaune/config.yaml` mit Standardwerten angelegt. 

Die Konfigurationsparameter werden nur beim Start des Servers ausgelesen.

## Starten
Ein fertiges Start-Skript liegt in `~/posaune/scripts/start.sh`. Seine Ausführung muss lediglich als Schedule im System hinterlegt werden - beispielsweise mit `crontab`.
Zu beachten ist, dass das Skript mit `bash` und nicht mit `sh` ausgeführt werden muss.
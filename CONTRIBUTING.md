# Technische Erläuterung

Ich versuche hier kurz und bündig einige technische Entscheidungen darzulegen, um die
Entwicklung und Debugging zu erleichtern.

Posaune ist eine leichtgewichtige Software zum Betreiben von Vertretungsplan-Monitoren. 
Sie wurde für das St. Benno Gymnasium in Dresden entwickelt und ist dementsprächend auf
die Ansprüche dort eingestellt.

## Architektur

Posaune ist eine [SSR-Website](https://developer.mozilla.org/en-US/docs/Glossary/SSR) mit [Ajax](https://de.wikipedia.org/wiki/Ajax_(Programmierung)).
Die Seite selbst ist in Jinja-HTML, CSS und etwas Browser-JavaScript geschrieben und 
wird in einer Python-Umgebung gerendert und über einen Flask-Webserver
als WSGI-Application bereitgestellt.
Das Laden und die Aktualisierung der angezeigten Daten erfolgt über [htmx](https://en.wikipedia.org/wiki/Htmx) und mehreren separaten HTML-Endpoints, an die die entsprechenden Datenanfragen geknüpft sind.

### Datenstrom

#### 📯 Konfiguration

- `config.toml` enthält die Konfigurationsparameter mit der höchsten Priorität
  - Kein Key *muss* vorhanden sein
  - Unbekannte Keys werden mitgetragen, aber an sich ignoriert 
  - Der Parameter `vermächtnis` kann einen Bezeichner für eine andere Konfiguration enthalten, deren Werte übernommen werden, wenn sie nicht in der aktuellen Konfiguration definiert sind
- `configurations.toml` enthält benannte Konfigurationen
  - Ist eine Map aus Keys (die in `config.yml` als `vermächtnis` referenziert werden können) auf die Struktur, die auch `config.yml` enthalten könnte
  - Auch `vermächtnis`-Parameter sind hier möglich, die Werte werden rekursiv übernommen

#### 📯 Aktualisierung

*veraltet*

#### 📯 Fehlerbehandlung

*veraltet*
# Technische Erläuterung

Ich versuche hier kurz und bündig einige technische Entscheidungen darzulegen, um die
Entwicklung und Debugging zu erleichtern.

Posaune ist eine leichtgewichtige Software zum Betreiben von Vertretungsplan-Monitoren. 
Sie wurde für das St. Benno Gymnasium in Dresden entwickelt und ist dementsprächend auf
die Ansprüche dort eingestellt.

## Architektur

Posaune ist eine [SSR-Website](https://developer.mozilla.org/en-US/docs/Glossary/SSR).
Die Seite selbst ist in Jinja-HTML, CSS und etwas Browser-JavaScript geschrieben und 
wird bei jeder Anfrage in einer Python-Umgebung gerendert und über einen Flask-Webserver
als WSGI-Application bereitgestellt.

### Datenstrom

#### 📯 Konfiguration

- `config.yml` enthält die Konfigurationsparameter mit der höchsten Priorität
  - Kein Key *muss* vorhanden sein
  - Unbekannte Keys werden ignoriert
  - Der Parameter `vermächtnis` kann einen Bezeichner für eine andere Konfiguration enthalten, deren Werte übernommen werden, wenn sie nicht in der aktuellen Konfiguration definiert sind
- `configurations.yaml` enthält benannte Konfigurationen
  - Ist eine Map aus Keys (die in `config.yml` als `vermächtnis` referenziert werden können) auf die Struktur, die auch `config.yml` enthalten könnte
  - Auch `vermächtnis`-Parameter sind hier möglich, die Werte werden rekursiv übernommen

#### 📯 Aktualisierung

Die Daten können momentan auschließlich durch eine neue Anfrage aktualisiert werden,
deswegen lädt die Seite in regelmäßigen Abständen automatisch neu.

#### 📯 Fehlerbehandlung

Wenn ein serverseitiger Fehler auftritt, wird eine Platzhalter-Seite gerendert aus
ausgeliefert, die lediglich den Typ des Fehlers und dessen Nachricht anzeigt.
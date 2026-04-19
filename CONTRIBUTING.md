# Technische Erläuterung

Posaune ist eine leichtgewichtige Software zum Betreiben von Vertretungsplan-Monitoren. 
Sie wurde für das St. Benno Gymnasium in Dresden entwickelt und ist dementsprächend auf
die Ansprüche dort eingestellt.

## Architektur

Posaune ist eine [SSR-Website](https://developer.mozilla.org/en-US/docs/Glossary/SSR).
Die Seite selbst ist in Jinja-HTML, CSS und etwas Browser-JavaScript geschrieben und 
wird bei jeder Anfrage in einer Python-Umgebung gerendert und über einen Flask-Webserver
als WSGI-Application bereitgestellt.

#### 📯 Konfiguration

Bei jedem Start des Webservers wird eine lokale Konfigurationsdatei eingelesen, in der
Aspekte des Inhalts und des Aufbaus so wie die Zugangsdaten zum Vertretungsplan
konfiguriert werden können.

#### 📯 Aktualisierung

Die Daten können momentan auschließlich durch eine neue Anfrage aktualisiert werden,
deswegen lädt die Seite in regelmäßigen Abständen automatisch neu.

#### 📯 Fehlerbehandlung

Wenn ein serverseitiger Fehler auftritt, wird eine Platzhalter-Seite gerendert aus
ausgeliefert, die lediglich den Typ des Fehlers und dessen Nachricht anzeigt.
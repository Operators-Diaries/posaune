from flask import Flask, render_template
from vpmobil import Vertretungsplan, Stundenplan24Pfade, KlassenVertretungsTag
from pathlib import Path
import yaml, json, datetime, typing

from lib.config import Config, load_yaml, resolve_inheritance, update_config_recursively
from lib.solar import fetch_solar
from lib.dvb import get_next_departures_by_line_and_direction
from lib.sorter import csort


#======// Configuration //=======================================================================//

CONFIG_PATH = Path("config.yaml")
CONFIGURATIONS_PATH = Path("configurations.yml")

# lokale Konfiguration laden
config_data = load_yaml(CONFIG_PATH)
if not config_data:
    cfg = Config()
    with CONFIG_PATH.open("w", encoding="utf-8") as f:
        yaml.safe_dump(cfg.model_dump(), f)
else:
    cfg = Config(**config_data)

# alle benannten Konfigurationen laden
configs: dict[str, Config] = {}
configurations_data = load_yaml(CONFIGURATIONS_PATH) or {}
for key, c in configurations_data.items():
    configs[key] = Config(**c)

# zuerst die Vererbungskette der lokalen config auflösen
if cfg.vermächtnis is not None:
    inherited = resolve_inheritance(cfg.vermächtnis, configs)
    update_config_recursively(inherited, cfg.model_dump())
    cfg = inherited

# lokale Datei nochmals als höchste Priorität anwenden
config_dict = load_yaml(CONFIG_PATH) or {}
update_config_recursively(cfg, config_dict)

#======// App //=================================================================================//

app = Flask(__name__)
app.jinja_env.globals |= dict(
    type = type,
    json = json,
    fach_sorting_key = lambda s: (s.fach is None, s.fach),  # None kommt ans Ende
    abfahrt_sorting_key = lambda s: (s[1]),
    csort = csort
)

vpzugang = Vertretungsplan(
    cfg.vertretungsplan.schulnummer,
    cfg.vertretungsplan.benutzer,
    cfg.vertretungsplan.passwort
)

vp_fallback: KlassenVertretungsTag | None = None

def get_payload() -> dict[str, typing.Any]:
    # In dieser Funktion wird das abrufen der Daten gesteuert und die entsprechenden Fehlermeldungen
    # konfiguriert. Exceptions sollen geraised werden. Sie werden in der App abgefangen.
    global vp_fallback

    try:
        solardaten = fetch_solar()
    except Exception as e:
        raise

    try:
        abfahrtsdaten = get_next_departures_by_line_and_direction()
    except Exception as e:
        raise e

    try:
        vpdaten = vpzugang.fetch()
        vp_fallback = vpdaten
    except:
        if vp_fallback and vp_fallback.datum == datetime.date.today():
            vpdaten = vp_fallback
        else:
            vp_fallback = None # es gibt kein sinnvolles Fallback
            vpdaten = vpzugang.fetch(datei=Stundenplan24Pfade.Klassen)

    return dict(
        vp = vpdaten,
        cfg = cfg,
        sol = solardaten,
        dvb = abfahrtsdaten
    )

@app.route('/')
def index():

    try:
        payload = get_payload()

        return render_template(
            'main.jinja',
            **payload
        )
    
    except Exception as e:
        return render_template(
            '404.jinja',
            cfg=cfg,
            e=e
        )

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template
from vpmobil import Vertretungsplan, Stundenplan24Pfade, KlassenVertretungsTag
from pathlib import Path
import yaml, json, datetime

from lib.config import PosauneConfig, load_yaml, resolve_inheritance, update_config_recursively
from lib.sorter import csort
from lib import solar
from lib import dvb


#======// Configuration //=======================================================================//

CONFIG_PATH = Path("config.yaml")
CONFIGURATIONS_PATH = Path("configurations.yml")

# lokale Konfiguration laden
_config_data = load_yaml(CONFIG_PATH)
if not _config_data:
    cfg = PosauneConfig()
    with CONFIG_PATH.open("w", encoding="utf-8") as f:
        yaml.safe_dump(cfg.model_dump(), f)
else:
    cfg = PosauneConfig(**_config_data)

# alle benannten Konfigurationen laden
configs: dict[str, PosauneConfig] = {}
_configurations_data = load_yaml(CONFIGURATIONS_PATH) or {}
for key, c in _configurations_data.items():
    configs[key] = PosauneConfig(**c)

# zuerst die Vererbungskette der lokalen config auflösen
if cfg.vermächtnis is not None:
    inherited = resolve_inheritance(cfg.vermächtnis, configs)
    update_config_recursively(inherited, cfg.model_dump())
    cfg = inherited

# lokale Datei nochmals als höchste Priorität anwenden
update_config_recursively(cfg, _config_data)

#======// App //=================================================================================//

app = Flask(__name__)
app.jinja_env.globals |= dict(
    type = type,
    json = json,
    csort = csort,
    sorting_key_fächer = lambda s: (s.fach is None, s.fach),  # None kommt ans Ende
    sorting_key_abfahrten = lambda s: (s[1]),
)

vpzugang = Vertretungsplan(
    cfg.vertretungsplan.schulnummer,
    cfg.vertretungsplan.benutzer,
    cfg.vertretungsplan.passwort
)

vp_fallback: KlassenVertretungsTag | None = None
timestamp: datetime.datetime | None = None

def get_payload() -> dict[str]:
    # In dieser Funktion wird das abrufen der Daten gesteuert und die entsprechenden Fehlermeldungen
    # konfiguriert. Exceptions sollen geraised werden. Sie werden in der App abgefangen.
    
    global vp_fallback

    try:
        vpdaten = vpzugang.fetch()
        timestamp = datetime.datetime.now()
        vp_fallback = vpdaten
    except:
        if vp_fallback and vp_fallback.datum == datetime.date.today():
            vpdaten = vp_fallback
        else:
            vp_fallback = None # es gibt kein sinnvolles Fallback
            vpdaten = vpzugang.fetch(datei=Stundenplan24Pfade.Klassen)
            
    try:
        solardaten = solar.fetch_solar()
    except Exception as e:
        solardaten = solar.Solardaten()

    try:
        abfahrtsdaten = dvb.get_abfahrten()
    except Exception as e:
        abfahrtsdaten = {}

    return dict(
        vp = vpdaten,
        cfg = cfg,
        sol = solardaten,
        dvb = abfahrtsdaten,
        timestamp = timestamp
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
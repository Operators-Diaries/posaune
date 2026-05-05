from flask import Flask, render_template
from vpmobil import Vertretungsplan, Stundenplan24Pfade, KlassenVertretungsTag
from pathlib import Path
import yaml, json, datetime

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
app.jinja_env.globals['type'] = type
app.jinja_env.globals['json'] = json
app.jinja_env.globals['fach_sorting_key'] = lambda s: (s.fach is None, s.fach)  # None kommt ans Ende
app.jinja_env.globals['abfahrt_sorting_key'] = lambda s: (s[1])
app.jinja_env.globals['csort'] = csort

vp = Vertretungsplan(
    cfg.vertretungsplan.schulnummer,
    cfg.vertretungsplan.benutzer,
    cfg.vertretungsplan.passwort
)

fallback: KlassenVertretungsTag | None = None

@app.route('/')
def index():
    global fallback

    try:
        solardaten = fetch_solar()
        dvb = get_next_departures_by_line_and_direction()

        try:
            data = vp.fetch()
            fallback = data
        except:
            if fallback and fallback.datum == datetime.date.today():
                data = fallback
            else:
                fallback = None # es gibt kein sinnvolles Fallback
                data = vp.fetch(datei=Stundenplan24Pfade.Klassen)

        return render_template(
            'main.jinja',
            vp=data,
            cfg=cfg,
            sol=solardaten,
            dvb=dvb
        )
    
    except Exception as e:
        return render_template(
            '404.jinja',
            cfg=cfg,
            e=e
        )

if __name__ == "__main__":
    app.run(debug=True)
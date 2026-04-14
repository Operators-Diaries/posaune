from flask import Flask, render_template
from vpmobil import Vertretungsplan, Stundenplan24Pfade
from pathlib import Path
import yaml, json

from lib.config import Config
from lib.solar import fetch_solar
from lib.dvb import get_next_departures_by_line_and_direction
from lib.sorter import csort

CONFIG_PATH = Path("config.yaml")

#======// Configuration //=======================================================================//

if not CONFIG_PATH.exists():
    cfg = Config()
    with CONFIG_PATH.open("w", encoding="utf-8") as f:
        yaml.safe_dump(cfg.model_dump(), f)
else:
    with CONFIG_PATH.open(encoding="utf-8") as f:
        cfg = Config(**yaml.safe_load(f))
    

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

@app.route('/')
def index():

    solardaten = fetch_solar()

    try:
        try:
            data = vp.fetch()
        except:
            data = vp.fetch(datei=Stundenplan24Pfade.Klassen)

        return render_template(
            'main.jinja',
            vp=data,
            cfg=cfg,
            sol=solardaten,
            dvb=get_next_departures_by_line_and_direction()
        )
    
    except Exception as e:
        return render_template(
            '404.jinja',
            cfg=cfg,
            e=e
        )

if __name__ == "__main__":
    app.run(debug=True)
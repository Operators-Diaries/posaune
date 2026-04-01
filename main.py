from flask import Flask, render_template
from vpmobil import Vertretungsplan, Standardpfade
from pathlib import Path
import yaml

from lib.config import Config
from lib.solar import fetch_solar

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
app.jinja_env.globals['sort_stunden_by_fach'] = lambda x: sorted(x, key=lambda s: (s.fach is None, s.fach))  # None kommt ans Ende

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
            data = vp.fetch(datei=Standardpfade.Klassen)

        return render_template(
            'main.jinja',
            vp=data,
            cfg=cfg,
            sol=solardaten
        )
    
    except Exception as e:
        return render_template(
            '404.jinja',
            cfg=cfg,
            e=e
        )

if __name__ == "__main__":
    app.run(debug=True)
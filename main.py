from flask import Flask, render_template
from vpmobil import Vertretungsplan
from pathlib import Path
import yaml

from config import Config

CONFIG_PATH = Path("config.yaml")


#======// Configuration //=======================================================================//

if not CONFIG_PATH.exists():
    cfg = Config()
    with CONFIG_PATH.open("w") as f:
        yaml.safe_dump(cfg.model_dump(), f)
else:
    with CONFIG_PATH.open() as f:
        data = yaml.safe_load(f)
    cfg = Config(**data)


#======// App //=================================================================================//

app = Flask(__name__)
app.jinja_env.globals['type'] = type
app.jinja_env.globals['sort_stunden_by_fach'] = lambda x: sorted(x, key=lambda s: (s.fach is None, s.fach)  # None kommt ans Ende
)

vp = Vertretungsplan(
    cfg.vertretungsplan.schulnummer,
    cfg.vertretungsplan.benutzer,
    cfg.vertretungsplan.passwort
)

@app.route('/')
def index():

    try:
        data = vp.fetch()

        return render_template(
            'main.html',
            vp=data,
            cfg=cfg
        )
    
    except Exception as e:
        return render_template(
            '404.html',
            cfg=cfg,
            e=e
        )

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template
from threading import Thread
from time import sleep
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
vp = Vertretungsplan(
    cfg.vertretungsplan.schulnummer,
    cfg.vertretungsplan.benutzer,
    cfg.vertretungsplan.passwort
)

# data_cache = None

# def update_data():
#     global data_cache
#     while True:
#         data_cache = vp.fetch()
#         sleep(5 * 60)

# thread = Thread(target=update_data, daemon=True)
# thread.start()

@app.route('/')
def index():

    data = vp.fetch()

    return render_template(
        'main.html',
        vp=data,
        cfg=cfg
    )

app.run(debug=True)
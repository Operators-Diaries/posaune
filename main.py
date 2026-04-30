from flask import Flask, render_template
from vpmobil import Vertretungsplan, Stundenplan24Pfade
from pathlib import Path
import yaml, json

from lib.config import Config
from lib.solar import fetch_solar
from lib.dvb import get_next_departures_by_line_and_direction
from lib.sorter import csort


#======// Configuration //=======================================================================//

CONFIG_PATH = Path("config.yaml")
CONFIGURATIONS_PATH = Path("configurations.yml")

def update_config_recursively(target, source_dict):
    """Recursively update config, handling nested BaseModels."""
    for param, value in source_dict.items():
        if hasattr(target, param):
            target_attr = getattr(target, param)
            if hasattr(target_attr, "model_dump") and isinstance(value, dict):
                update_config_recursively(target_attr, value)
            else:
                setattr(target, param, value)
        else:
            setattr(target, param, value)

def load_yaml(path: Path):
    if not path.exists():
        return None
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

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

def resolve_inheritance(name: str) -> Config:
    chain = []
    seen = set()
    current = name

    while current is not None:
        if current in seen:
            raise Exception(f"Zirkuläre Vererbung erkannt bei '{current}'.")

        seen.add(current)

        if current not in configs:
            raise Exception(f"Vermächtnis '{current}' nicht gefunden.")

        cfg_part = configs[current]
        chain.append((current, cfg_part))
        current = cfg_part.vermächtnis

    resolved = Config()

    for name, part in reversed(chain):
        print(f"Konfiguration wird von '{name}' geerbt.")
        update_config_recursively(resolved, part.model_dump(exclude_unset=True))

    return resolved

# zuerst die Vererbungskette der lokalen config auflösen
if cfg.vermächtnis is not None:
    inherited = resolve_inheritance(cfg.vermächtnis)
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
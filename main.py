from flask import Flask, render_template
from vpmobil import VertretungsplanZugang, Standardpfade, Vertretungsplan
from pathlib import Path
import yaml, json, datetime, locale

from src.lib.config import PosauneConfig, load_yaml, resolve_inheritance, update_config_recursively
from src.lib.sorter import csort
from src.lib import solar
from src.lib import dvb

locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")

#======// Configuration //=======================================================================//

CONFIG_PATH = Path("config.yaml")
CONFIGURATIONS_PATH = Path("configurations.yml")

# lokale Konfiguration laden
_config_dict = load_yaml(CONFIG_PATH)
if not _config_dict:
    cfg = PosauneConfig()
    with CONFIG_PATH.open("w", encoding="utf-8") as f:
        yaml.safe_dump(cfg.model_dump(), f, allow_unicode=True)
else:
    cfg = PosauneConfig(**_config_dict)

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
update_config_recursively(cfg, _config_dict or {})

#======// App //=================================================================================//

app = Flask(
    __name__,
    static_folder="src",
    template_folder="src"
)
app.jinja_env.globals |= dict(
    type = type,
    json = json,
    csort = csort,
    sorting_key_fächer = lambda s: (s.fach is None, s.fach),  # None kommt ans Ende
    sorting_key_abfahrten = lambda s: (s[1]),
)

vpzugang = VertretungsplanZugang(
    cfg.vertretungsplan.schulnummer,
    cfg.vertretungsplan.benutzer,
    cfg.vertretungsplan.passwort
)



#======// Hauptroute //==================================//

@app.route('/')
def index():

    try:
        return render_template(
            'main.jinja',
            cfg=cfg.frontend,
        )
    except Exception as e:
        raise e


#======// Komponenten //=================================//

vp_fallback: Vertretungsplan | None = None
timestamp: datetime.datetime | None = None
error = lambda e: render_template('components/error.jinja', cfg=cfg.frontend, e=e)

@app.route('/plan')
def get_plan():
    global vp_fallback
    global timestamp

    try:
        try:
            vpdaten = vpzugang.get()
            timestamp = datetime.datetime.now()
            vp_fallback = vpdaten
        except:
            if vp_fallback and vp_fallback.datum == datetime.date.today():
                vpdaten = vp_fallback
            else:
                vp_fallback = None # es gibt kein sinnvolles Fallback
                vpdaten = vpzugang.get(datei=Standardpfade.Klassen)
                
        # vpdaten = vpzugang.get(datetime.date(2026, 5, 14)) # DEBUG
        return render_template(
            'components/plan.jinja',
            timestamp=timestamp,
            cfg=cfg.frontend,
            vp=vpdaten
        )
            
    except Exception as e:
        return render_template('components/error.jinja', cfg=cfg.frontend, e=e)

@app.route('/dvb')
def get_dvb():
    
    try:
        
        try:
            abfahrtsdaten = dvb.get_abfahrten()
        except Exception as e:
            abfahrtsdaten = {}
            
        return render_template(
            'components/dvb.jinja',
            dvb=abfahrtsdaten
        )
            
    except Exception as e:
        return error(e)
        
@app.route('/solar')
def get_solar():
    
    try:
        
        try:
            solardaten = solar.fetch_solar()
        except Exception as e:
            solardaten = solar.Solardaten()
            
        return render_template(
            'components/sol.jinja',
            sol=solardaten
        )
            
    except Exception as e:
        return error(e)

if __name__ == "__main__":
    app.run(debug=True)
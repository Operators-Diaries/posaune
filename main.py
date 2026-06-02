from flask import Flask, render_template
from vpmobil import VertretungsplanZugang, Standardpfade, Vertretungsplan, Parser as VpParser
# from vpmobil.extensions import pp
from pathlib import Path
import yaml, json, datetime, locale

from src.lib.config import PosauneConfig, load_yaml, resolve_inheritance, update_config_recursively
from src.lib.sorting import csort
from src.lib import solar
from src.lib import öpnv

locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")

#======// Configuration //=======================================================================//

CONFIG_PATH = Path("config.yaml")
CONFIGURATIONS_PATH = Path("configurations.yml")

# lokale Konfiguration laden
_config_dict = load_yaml(CONFIG_PATH)
if not _config_dict:
    config = PosauneConfig()
    with CONFIG_PATH.open("w", encoding="utf-8") as f:
        yaml.safe_dump(config.model_dump(), f, allow_unicode=True)
else:
    config = PosauneConfig(**_config_dict)

# alle benannten Konfigurationen laden
configs: dict[str, PosauneConfig] = {}
_configurations_data = load_yaml(CONFIGURATIONS_PATH) or {}
for key, c in _configurations_data.items():
    configs[key] = PosauneConfig(**c)

# zuerst die Vererbungskette der lokalen config auflösen
if config.vermächtnis is not None:
    inherited = resolve_inheritance(config.vermächtnis, configs)
    update_config_recursively(inherited, config.model_dump())
    config = inherited

# lokale Datei nochmals als höchste Priorität anwenden
update_config_recursively(config, _config_dict or {})

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
    config.vertretungsplan.schulnummer,
    config.vertretungsplan.benutzer,
    config.vertretungsplan.passwort
)



#======// Hauptroute //==================================//

@app.route('/')
def index():

    try:
        return render_template(
            'main.html.j2',
            cfg=config.frontend,
        )
    except Exception as e:
        raise e


#======// Komponenten //=================================//

vp_fallback: Vertretungsplan | None = None
timestamp: datetime.datetime | None = None
error = lambda e: render_template('components/error.html.j2', cfg=config.frontend, e=e)

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
                vpdaten = vpzugang.get(datei=Standardpfade.Klassen)#, parser=pp.StBennoGymnasium)
                
        # vpdaten = Vertretungsplan.fromfile("src/assets/debug_plan.xml", parser=VpParser())#, parser=pp.StBennoGymnasium) # DEBUG
        return render_template(
            'components/plan.html.j2',
            timestamp=timestamp,
            cfg=config.frontend,
            vp=vpdaten
        )
            
    except Exception as e:
        return render_template('components/error.html.j2', cfg=config.frontend, e=e)

@app.route('/öpnv')
def get_öpnv():
    
    try:
        
        try:
            abfahrtsdaten = öpnv.get_abfahrten()
        except Exception as e:
            abfahrtsdaten = {}
            
        return render_template(
            'components/öpnv.html.j2',
            öpnv=abfahrtsdaten
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
            'components/sol.html.j2',
            sol=solardaten
        )
            
    except Exception as e:
        return error(e)


if __name__ == "__main__":
    app.run(debug=True)
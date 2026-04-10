from pathlib import Path
from flask import render_template
from main import app, vp, cfg, Stundenplan24Pfade, fetch_solar, get_next_departures_by_line_and_direction

with app.app_context():
    try:
        data = vp.fetch()
    except:
        data = vp.fetch(datei=Stundenplan24Pfade.Klassen)

    solardaten = fetch_solar()

    # DEBUG
    print(data.datum)
    print(data._data)

    with app.test_request_context():
        html = render_template("main.jinja", vp=data, cfg=cfg, sol=solardaten, dvb=get_next_departures_by_line_and_direction())

    # GitHub Pages: absolute /static/... in relative static/... umwandeln
    html = html.replace('href="/static/', 'href="static/')
    html = html.replace('src="/static/', 'src="static/')
    html = html.replace("url('/static/", "url('static/")
    html = html.replace('url("/static/', 'url("static/')

    out = Path("build")
    out.mkdir(exist_ok=True)
    (out / "index.html").write_text(html, encoding="utf-8")
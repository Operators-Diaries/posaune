from pathlib import Path
from flask import render_template
from main import app, vp, cfg, Standardpfade, fetch_solar

with app.app_context():
    try:
        data = vp.fetch()
    except:
        data = vp.fetch(datei=Standardpfade.Klassen)

    solardaten = fetch_solar()

    with app.test_request_context():
        html = render_template("main.jinja", vp=data, cfg=cfg, sol=solardaten)

    # GitHub Pages: absolute /static/... in relative static/... umwandeln
    html = html.replace('href="/static/', 'href="static/')
    html = html.replace('src="/static/', 'src="static/')
    html = html.replace("url('/static/", "url('static/")
    html = html.replace('url("/static/', 'url("static/')

    out = Path("build")
    out.mkdir(exist_ok=True)
    (out / "index.html").write_text(html, encoding="utf-8")
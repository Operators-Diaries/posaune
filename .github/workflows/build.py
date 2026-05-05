from pathlib import Path
from flask import render_template
from main import app, cfg, get_payload

with app.app_context():
    try:
        payload = get_payload()

        with app.test_request_context():
            html = render_template("main.jinja", **payload)
    
    except Exception as e:
        with app.test_request_context():
            html = render_template('404.jinja', cfg=cfg, e=e)

    # GitHub Pages: absolute /static/... in relative static/... umwandeln
    html = html.replace('href="/static/', 'href="static/')
    html = html.replace('src="/static/', 'src="static/')
    html = html.replace("url('/static/", "url('static/")
    html = html.replace('url("/static/', 'url("static/')

    out = Path("build")
    out.mkdir(exist_ok=True)
    (out / "index.html").write_text(html, encoding="utf-8")
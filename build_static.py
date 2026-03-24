from flask import render_template
from main import app, vp, cfg

with app.app_context():
    data = vp.fetch()
    with app.test_request_context():
        html = render_template("main.html", vp=data, cfg=cfg)

    with open("build/index.html", "w", encoding="utf-8") as f:
        f.write(html)
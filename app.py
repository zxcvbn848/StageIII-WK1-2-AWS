from flask import Flask, render_template
from datetime import timedelta
import os

from api.upload import api_upload

app = Flask(__name__)
app.config.from_object("config")

app.register_blueprint(api_upload, url_prefix = "/api")

app.config["JSON_SORT_KEYS"] = False
app.config["JSON_AS_ASCII"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True

app.config["SECRET_KEY"] = os.urandom(24)
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days = 1)

@app.route("/")
def index():
	return render_template("index.html")

if __name__ == "__main__":
	app.run(host = "0.0.0.0", port = 5000, debug = True)

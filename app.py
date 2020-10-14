""" 
Start the flask server by running:
$ python app.py

And then head to http://127.0.0.1:5000/ in your browser to see the map displayed
"""

import json
import os
from typing import Dict

from dotenv import load_dotenv
from flask import Flask
from flask_compress import Compress

import fover.api.main as api_main


def setup_app_conf(app: Flask, prefix: str) -> None:
    envs = {k: v for k, v in os.environ.items() if k.startswith(prefix) and v}

    for k, v in envs.items():
        key = k[len(prefix) :]  # Strip the prefix

        try:
            app.config[key] = json.loads(v)
        except ValueError as e:
            # Value is a raw string
            app.config[key] = v


load_dotenv()

# static_url_path – can be used to specify a different path for the static files on the web.
#                   Defaults to the name of the static_folder folder.
# static_folder – the folder with static files that should be served at static_url_path.
#                 Defaults to the 'static' folder in the root path of the application.
FLASK_APP_ENV_PREFIX = "FLASK_APP_"
app = Flask(__name__)

setup_app_conf(app, FLASK_APP_ENV_PREFIX)
Compress(app)

app.register_blueprint(api_main.bp)

if __name__ == "__main__":
    app.run(debug=True)

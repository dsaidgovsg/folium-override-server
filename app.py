""" 
Start the flask server by running:
$ python app.py

And then head to http://127.0.0.1:5000/ in your browser to see the map displayed
"""

import os

from flask import Flask

import fover.api.main as api_main

# static_url_path – can be used to specify a different path for the static files on the web.
#                   Defaults to the name of the static_folder folder.
# static_folder – the folder with static files that should be served at static_url_path.
#                 Defaults to the 'static' folder in the root path of the application.
app = Flask(__name__)

app.register_blueprint(api_main.bp)

if __name__ == "__main__":
    app.run(debug=True)

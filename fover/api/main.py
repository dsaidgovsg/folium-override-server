import json
import logging
import os
from typing import Dict

from flask import (
    Blueprint,
    Response,
    make_response,
    render_template,
    request,
    send_file,
)

from fover.utils.env import Env
from fover.utils.parse import convert_folium_html

bp = Blueprint("main", __name__, static_folder="../../static")


def read_json_conf(conf_path: str, folium_server_url: str) -> Dict[str, str]:
    with open(os.path.join(conf_path)) as json_file:
        folium_conf = json.load(json_file)
        for res_name in folium_conf:
            folium_conf[res_name] = os.path.join(
                folium_server_url, folium_conf[res_name]
            )
    return folium_conf


@bp.route("/generate", methods=["POST"])
def generate() -> Response:
    folium_host = request.form.get("folium_host")
    tileserver_gl_host = request.form.get("tileserver_gl_host")
    tileserver_gl_tile = request.form.get("tileserver_gl_tile")

    f = request.files["file"]
    html_content = f.read()

    filename, _ = os.path.splitext(f.filename)
    override_filename = f"${filename}_override.html"

    # Read and modify the JS and CSS configurations
    folium_js_conf = read_json_conf(
        os.path.join(bp.static_folder, "external/folium-js.json"), folium_host,
    )
    folium_css_conf = read_json_conf(
        os.path.join(bp.static_folder, "external/folium-css.json"), folium_host,
    )

    mod_html = convert_folium_html(
        html_content,
        folium_js_conf,
        folium_css_conf,
        tileserver_gl_host,
        tileserver_gl_tile,
    )

    rsp = make_response(mod_html)
    rsp.headers["Content-Type"] = "text/html"
    rsp.headers["Content-Disposition"] = f"attachment;filename={filename}_override.html"
    return rsp


@bp.route("/")
def root() -> Response:
    return render_template(
        "root.html",
        folium_host=Env.APP_DEFAULT_FOLIUM_SERVER_URL,
        tileserver_gl_host=Env.APP_DEFAULT_TILESERVER_GL_URL,
        tileserver_gl_tiles=Env.APP_TILESERVER_GL_TILES,
    )

import logging
from os import path

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

bp = Blueprint("main", __name__)


@bp.route("/generate", methods=["POST"])
def generate() -> Response:
    folium_host = request.form.get("folium_host")
    tileserver_gl_host = request.form.get("tileserver_gl_host")
    tileserver_gl_tile = request.form.get("tileserver_gl_tile")

    f = request.files["file"]
    html_content = f.read()

    filename, _ = path.splitext(f.filename)
    override_filename = f"${filename}_override.html"

    mod_html = convert_folium_html(
        html_content, folium_host, tileserver_gl_host, tileserver_gl_tile,
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

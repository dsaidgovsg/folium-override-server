import logging
from os import path

import folium
from flask import Blueprint, render_template, request, send_file
from RestrictedPython import compile_restricted, safe_globals

from fover.utils.env import Env

bp = Blueprint("main", __name__)


def parse_script(content: str) -> folium.Map:
    loc = {}
    byte_code = compile_restricted(content, "<inline>", "exec")
    exec(byte_code, safe_globals, loc)
    loc["generate_map"]()


@bp.route("/generate", methods=["POST"])
def generate():
    f = request.files["file"]

    filename, _ = path.splitext(f.filename)
    override_filename = f"${filename}_override.py"
    f.save(override_filename)

    return send_file(override_filename, as_attachment=True, mimetype="text/plain")

    # return content
    # override_js = (
    #     {
    #         "leaflet": path.join(Env.APP_FOLIUM_SERVER_URL, "leaflet@1.5.1/leaflet.js"),
    #         "jquery": path.join(Env.APP_FOLIUM_SERVER_URL, "jquery-1.12.4.min.js"),
    #         "bootstrap": path.join(
    #             Env.APP_FOLIUM_SERVER_URL, "bootstrap@3.2.0/bootstrap.min.js"
    #         ),
    #         "awesome_markers": path.join(
    #             Env.APP_FOLIUM_SERVER_URL,
    #             "leaflet.awesome-markers@2.0.2/leaflet.awesome-markers.js",
    #         ),
    #     }
    #     if Env.APP_FOLIUM_SERVER_URL
    #     else {}
    # )

    # override_css = (
    #     {
    #         "leaflet_css": path.join(
    #             Env.APP_FOLIUM_SERVER_URL, "leaflet@1.5.1/leaflet.css"
    #         ),
    #         "bootstrap_css": path.join(
    #             Env.APP_FOLIUM_SERVER_URL, "bootstrap@3.2.0/bootstrap.min.css"
    #         ),
    #         "bootstrap_theme_css": path.join(
    #             Env.APP_FOLIUM_SERVER_URL, "bootstrap@3.2.0/bootstrap-theme.min.css"
    #         ),
    #         "awesome_markers_font_css": path.join(
    #             Env.APP_FOLIUM_SERVER_URL, "font-awesome@4.6.3/font-awesome.min.css"
    #         ),
    #         "awesome_markers_css": path.join(
    #             Env.APP_FOLIUM_SERVER_URL,
    #             "leaflet.awesome-markers@2.0.2/leaflet.awesome-markers.css",
    #         ),
    #         "awesome_rotate_css": path.join(
    #             Env.APP_FOLIUM_SERVER_URL, "leaflet.awesome.rotate.css"
    #         ),
    #     }
    #     if Env.APP_FOLIUM_SERVER_URL
    #     else {}
    # )

    # folium_map = folium.Map(
    #     location=SG_LATLNG,
    #     zoom_start=FOLIUM_DEFAULT_ZOOM,
    #     tiles=f"{Env.APP_TILESERVER_URL}/styles/{Env.APP_TILESERVER_STYLE}/{{z}}/{{x}}/{{y}}.png",
    #     attr=Env.APP_FOLIUM_ATTRIBUTION,
    # )

    # folium_map.set_override_js(override_js)
    # folium_map.set_override_css(override_css)

    # return folium_map._repr_html_()


@bp.route("/")
def root():
    return render_template("root.html")

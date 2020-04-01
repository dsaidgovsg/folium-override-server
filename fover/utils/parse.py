import base64
import binascii
import os
import re

from bs4 import BeautifulSoup


def convert_folium_html(
    html: str,
    folium_override_base_path: str,
    tileserver_override_base_path: str,
    tile_identifier: str,
) -> str:
    HTML_PARSER = "html.parser"

    # See: https://github.com/dsaidgovsg/folium-resource-server
    js_mappings = {
        "leaflet.js": os.path.join(
            folium_override_base_path, "leaflet@1.5.1/leaflet.js"
        ),
        "jquery-1.12.4.min.js": os.path.join(
            folium_override_base_path, "jquery-1.12.4.min.js"
        ),
        "bootstrap.min.js": os.path.join(
            folium_override_base_path, "bootstrap@3.2.0/bootstrap.min.js"
        ),
        "leaflet.awesome-markers.js": os.path.join(
            folium_override_base_path,
            "leaflet.awesome-markers@2.0.2/leaflet.awesome-markers.js",
        ),
    }

    css_mappings = {
        "leaflet.css": os.path.join(
            folium_override_base_path, "leaflet@1.5.1/leaflet.css"
        ),
        "bootstrap.min.css": os.path.join(
            folium_override_base_path, "bootstrap@3.2.0/bootstrap.min.css"
        ),
        "bootstrap-theme.min.css": os.path.join(
            folium_override_base_path, "bootstrap@3.2.0/bootstrap-theme.min.css"
        ),
        "font-awesome.min.css": os.path.join(
            folium_override_base_path, "font-awesome@4.6.3/font-awesome.min.css"
        ),
        "leaflet.awesome-markers.css": os.path.join(
            folium_override_base_path,
            "leaflet.awesome-markers@2.0.2/leaflet.awesome-markers.css",
        ),
        "leaflet.awesome.rotate.css": os.path.join(
            folium_override_base_path, "leaflet.awesome.rotate.css"
        ),
    }

    soup = BeautifulSoup(html, HTML_PARSER)
    iframe = soup.find("iframe")

    SRC_BASE64_PREFIX = "data:text/html;charset=utf-8;base64,"
    iframe_src_encoded = iframe["src"].replace(SRC_BASE64_PREFIX, "")
    iframe_src_decoded = base64.b64decode(iframe_src_encoded)
    soup_iframe = BeautifulSoup(iframe_src_decoded, HTML_PARSER)

    # Modify all JS URLs
    js_scripts = [s for s in soup_iframe.find_all("script") if s.get("src")]
    for s in js_scripts:
        filename = s["src"].split("/")[-1]
        mod_url = js_mappings.get(filename)
        if mod_url:
            s["src"] = mod_url

    # Modify all CSS URLs
    js_scripts = [s for s in soup_iframe.find_all("link") if s.get("href")]
    for s in js_scripts:
        filename = s["href"].split("/")[-1]
        mod_url = css_mappings.get(filename)
        if mod_url:
            s["href"] = mod_url

    # Modify tileserver
    # There should be only one of such script amongst the rest of the script tags
    tileserver_pattern = re.compile(r"L\.tileLayer\((\s+)\".+?\",", re.MULTILINE)

    tileserver_scripts = [
        s for s in soup_iframe.find_all("script") if s.get("src") is None
    ]
    for s in tileserver_scripts:
        # We manually escape replacement string e.g. \1 -> \\1 since there isn't
        # a built-in method
        escaped_tileserver_override_path = (
            os.path.join(
                tileserver_override_base_path,
                f"styles/{tile_identifier}/{{z}}/{{x}}/{{y}}.png",
            )
            .strip("/")
            .replace("\\", "\\\\")
        )
        mod_text = tileserver_pattern.sub(
            r'L.tileLayer(\1"' + escaped_tileserver_override_path + r'",', s.getText()
        )
        s.string = mod_text

    mod_iframe_encoded = str(
        base64.b64encode(soup_iframe.prettify().encode("ascii")), "utf-8"
    )
    iframe["src"] = f"{SRC_BASE64_PREFIX}{mod_iframe_encoded}"

    return soup.prettify()

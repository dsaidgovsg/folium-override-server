import base64
import binascii
import os
import re
from typing import Dict

from bs4 import BeautifulSoup, Tag

HTML_PARSER = "html.parser"


def convert_folium_html_impl(
    soup_inner: BeautifulSoup,
    folium_override_js_mappings: Dict[str, str],
    folium_override_css_mappings: Dict[str, str],
    tileserver_override_base_path: str,
    tile_identifier: str,
) -> None:
    """This implementation in-place changes soup_inner content for `save` mode."""

    # Modify all JS URLs
    js_scripts = [s for s in soup_inner.find_all("script") if s.get("src")]
    for s in js_scripts:
        filename = s["src"].split("/")[-1]
        mod_url = folium_override_js_mappings.get(filename)
        if mod_url:
            s["src"] = mod_url

    # Modify all CSS URLs
    js_scripts = [s for s in soup_inner.find_all("link") if s.get("href")]
    for s in js_scripts:
        filename = s["href"].split("/")[-1]
        mod_url = folium_override_css_mappings.get(filename)
        if mod_url:
            s["href"] = mod_url

    # Modify tileserver
    # There should be only one of such script amongst the rest of the script tags
    tileserver_pattern = re.compile(r"L\.tileLayer\((\s+)\".+?\",", re.MULTILINE)

    tileserver_scripts = [
        s for s in soup_inner.find_all("script") if s.get("src") is None
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


def convert_folium_html_iframe_impl(
    iframe: Tag,
    folium_override_js_mappings: Dict[str, str],
    folium_override_css_mappings: Dict[str, str],
    tileserver_override_base_path: str,
    tile_identifier: str,
) -> None:
    """This implementation in-place changes iframe content for `_repr_html_` mode."""

    SRC_BASE64_PREFIX = "data:text/html;charset=utf-8;base64,"
    iframe_src_encoded = iframe["src"].replace(SRC_BASE64_PREFIX, "")
    iframe_src_decoded = base64.b64decode(iframe_src_encoded)
    soup_inner = BeautifulSoup(iframe_src_decoded, HTML_PARSER)

    # The rest of the impl is the same as `.save` mode
    convert_folium_html_impl(
        soup_inner,
        folium_override_js_mappings,
        folium_override_css_mappings,
        tileserver_override_base_path,
        tile_identifier,
    )

    mod_iframe_encoded = str(
        base64.b64encode(soup_inner.prettify().encode("ascii")), "utf-8"
    )
    iframe["src"] = f"{SRC_BASE64_PREFIX}{mod_iframe_encoded}"


def convert_folium_html(
    html: str,
    folium_override_js_mappings: Dict[str, str],
    folium_override_css_mappings: Dict[str, str],
    tileserver_override_base_path: str,
    tile_identifier: str,
) -> str:
    soup = BeautifulSoup(html, HTML_PARSER)
    iframe = soup.find("iframe")

    if iframe:
        # If iframe is found, this is saved via `_repr_html_`, so need to decode the iframe
        convert_folium_html_iframe_impl(
            iframe,
            folium_override_js_mappings,
            folium_override_css_mappings,
            tileserver_override_base_path,
            tile_identifier,
        )
    else:
        # Else, it is done normally via `.save(filename)`, i.e. soup -> soup_inner
        convert_folium_html_impl(
            soup,
            folium_override_js_mappings,
            folium_override_css_mappings,
            tileserver_override_base_path,
            tile_identifier,
        )

    return soup.prettify()

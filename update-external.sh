#!/usr/bin/env bash
FOLIUM_VERSION="v0.10.1"
curl -sLo static/external/folium-css.json https://raw.githubusercontent.com/dsaidgovsg/folium-resource-server/v0.1.0_folium-${FOLIUM_VERSION}/external/folium-css.json
curl -sLo static/external/folium-js.json https://raw.githubusercontent.com/dsaidgovsg/folium-resource-server/v0.1.0_folium-${FOLIUM_VERSION}/external/folium-js.json

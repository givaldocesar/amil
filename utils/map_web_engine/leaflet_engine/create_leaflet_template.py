from .create_leaflet_core_script import *
from .create_leaflet_basemaps_script import *
from .create_leaflet_layers_script import *

def create_leaflet_template(configs):
    html = f"""<!DOCTYPE html>
    <html>
    <head>
        <title>Amil WebGIS - Leaflet</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <style>
            html, body, #map {{ width: 100%; height: 100%; margin: 0; padding: 0; }}
        </style>
    </head>
    <body>
        <div id="map"></div>
        { create_leaflet_core_script(configs) }
        { create_leaflet_basemaps_script(configs) }
        { create_leaflet_layers_script(configs) }
    </body>
    </html>"""

    return html
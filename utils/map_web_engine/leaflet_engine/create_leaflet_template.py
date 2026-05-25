from ..create_page_title import *
from .create_leaflet_core_script import *
from .create_leaflet_basemaps_script import *
from .create_leaflet_layers_script import *

def create_leaflet_template(configs):
    head_tags, title = create_page_title(configs["title"])
    
    html = f"""<!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        { head_tags }
    </head>
    <body>
        { title }
        <div id="map"></div>
        { create_leaflet_core_script(configs) }
        { create_leaflet_basemaps_script(configs) }
        { create_leaflet_layers_script(configs) }
    </body>
    </html>"""

    return html
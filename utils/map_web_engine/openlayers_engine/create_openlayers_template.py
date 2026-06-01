from ..create_page_title import create_page_title
from .create_openlayers_core_script import create_openlayers_core_script
from .create_openlayers_basemaps_script import create_openlayers_basemaps_script


def create_openlayers_template(configs):    
    head_tags, title = create_page_title(configs["title"])
    
    html = f"""<!DOCTYPE html>
    <html>
    <head>
        <title>{configs['title']}</title>
        <meta charset="utf-8" />
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/ol@v8.2.0/ol.css" />
        <script src="https://cdn.jsdelivr.net/npm/ol@v8.2.0/dist/ol.js"></script>
        { head_tags }
    </head>
    <body>
        { title }
        <div id="map"></div>
        { create_openlayers_core_script(configs) }
        { create_openlayers_basemaps_script(configs) }
    </body>
    </html>"""

    return html
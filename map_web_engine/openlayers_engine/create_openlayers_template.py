from ..create_page_title import create_page_title
from ..copy_engine import copy_engine
from .create_openlayers_core_script import create_openlayers_core_script
from .create_openlayers_basemaps_script import create_openlayers_basemaps_script

def create_openlayers_template(configs):    
    link_href = "https://cdn.jsdelivr.net/npm/ol@v8.2.0/ol.css"
    script_src = "https://cdn.jsdelivr.net/npm/ol@v8.2.0/dist/ol.js"

    if(configs["mode"] == "offline"):
        link_href = "openlayers/ol.css"
        script_src = "openlayers/ol.js"
        copy_engine(configs["output_dir"], 'openlayers')
    
    head_tags, title = create_page_title(configs["title"])
    
    html = f"""<!DOCTYPE html>
    <html>
    <head>
        <title>{configs['title']}</title>
        <meta charset="utf-8" />
        <link rel="stylesheet" href="{link_href}"/>
        <script src="{script_src}"></script>
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
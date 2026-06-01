import os, shutil
from ..create_page_title import *
from .create_leaflet_core_script import *
from .create_leaflet_basemaps_script import *
from .create_leaflet_layers_script import *

def create_leaflet_template(configs):
    link_href = "https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
    script_src = "https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"
    
    if(configs["mode"] == "offline"):
        link_href = "leaflet/leaflet.css"
        script_src = "leaflet/leaflet.js"

        output_dir = configs["output_dir"]

        current_dir = os.path.dirname(__file__)
        plugin_root = os.path.abspath(os.path.join(current_dir, '..', '..', '..'))
        src_leaflet = os.path.join(plugin_root, 'assets', 'leaflet')
        dst_leaflet = os.path.join(output_dir, 'leaflet')
        
        if not os.path.exists(dst_leaflet):
            shutil.copytree(src_leaflet, dst_leaflet)

    head_tags, title = create_page_title(configs["title"])
    
    html = f"""<!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="{link_href}" />
        <script src="{script_src}"></script>
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
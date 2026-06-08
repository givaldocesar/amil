import os
from ..get_layers_extension import get_layers_extension
from ..save_script import save_script

def create_leaflet_core_script(configs):
    output_dir = configs.get("output_dir")
    lat, long = configs.get("center")

    scripts_dir = os.path.join(output_dir, "scripts")
    os.makedirs(scripts_dir, exist_ok=True)

    js = []

    bounds = get_layers_extension(configs.get("layers"))
    if configs.get("auto_extent") and bounds:
        js.append(f"const map = L.map('map').fitBounds([{bounds}], 4);\n")
    else:
        js.append(f"const map = L.map('map').setView([{lat}, {long}], 4);\n")
    
    js.append("map.getPane('popupPane').style.zIndex = 2000;")

    js.append("const layerControl = L.control.layers(null, {}, {",)
    js.append("\tcollapsed: true",)
    js.append("}).addTo(map);")

    save_script(scripts_dir, "core.js", js)

    return '<script src="scripts/core.js"></script>'
import os
from ...tr import tr
from ..basemaps_providers import BASEMAP_PROVIDERS

def create_leaflet_basemaps_script(configs):
    output_dir = configs.get("output_dir")
    basemaps =  configs.get("basemaps")

    scripts_dir = os.path.join(output_dir, "scripts")
    os.makedirs(scripts_dir, exist_ok=True)
    
    js = [tr("//--- Definições de Mapas Base---")]
    obj_basemaps = []
    first_map = True

    for basemap in basemaps:
        if  basemap  in BASEMAP_PROVIDERS:
            provider = BASEMAP_PROVIDERS[ basemap ]
            name = provider["name"]
            url = provider["url"]
            attribution = provider["attribution"]

            js.append(f"const {basemap} = L.tileLayer('{url}', {{ attribution: '{attribution}' }});")
            js.append(f"layerControl.addBaseLayer({basemap}, '{name}');")
            obj_basemaps.append(f"\t'{name}': {basemap}")

            if first_map:
                first_map = basemap
    
    js.append("")

    if(first_map): js.append(f"{first_map}.addTo(map);")

    js_path = os.path.join(scripts_dir, "basemaps.js")
    with open(js_path, "w", encoding="utf-8") as f:
        f.write("\n".join(js))

    return '<script src="scripts/basemaps.js"></script>'
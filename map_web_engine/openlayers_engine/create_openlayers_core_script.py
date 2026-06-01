import os
from ...utils.tr import tr
from ..save_script import save_script
from ..get_layers_extension import get_layers_extension

def create_openlayers_core_script(configs):
    output_dir = configs.get("output_dir")
    lat, long = configs.get("center")

    scripts_dir = os.path.join(output_dir, "scripts")
    os.makedirs(scripts_dir, exist_ok=True)
    
    #Group de Camadas Vetoriais
    js = ["const vector_layers = new ol.layer.Group({"]
    js.append(f"\ttitle: '{tr('Camadas')}',")
    js.append("\tlayers: [],")
    js.append("});\n")

    #Group de Basemaps
    js.append("const basemaps = new ol.layer.Group({")
    js.append(f"\ttitle: '{tr('Mapas Base')}',")
    js.append("\tlayers: [],")
    js.append("});\n")
    
    # Mapa
    js.append("const map = new ol.Map({")
    js.append("\ttarget: 'map',")
    js.append("\tlayers: [basemaps, vector_layers],")
    js.append("\tview: new ol.View({")
    js.append(f"\t\tcenter: ol.proj.fromLonLat([{long}, {lat}]),")
    js.append("\t\tzoom: 10")
    js.append("\t})")
    js.append("});\n")

    bounds = get_layers_extension(configs.get("layers"))
    if configs.get("auto_extent") and bounds:
        minY, minX = bounds[0]
        maxY, maxX = bounds[1]
        extent = f"[{minX}, {minY}, {maxX}, {maxY}]"

        js.append(f"map.getView().fit(ol.proj.transformExtent({extent}, 'EPSG:4326', 'EPSG:3857'),{{")
        js.append("\tpadding: [50, 50, 50, 50],")
        js.append("\tmaxZoom: 10")
        js.append("});")
    
    # Salva o script
    save_script(scripts_dir, "core.js", js)

    return '<script src="scripts/core.js"></script>'
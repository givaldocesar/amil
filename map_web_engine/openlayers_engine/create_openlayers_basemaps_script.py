import os
from ...utils.tr import tr
from ..basemaps_providers import BASEMAP_PROVIDERS
from ..save_script import save_script

def create_openlayers_basemaps_script(configs):
    if configs["mode"] == 'offline': return ''

    output_dir = configs.get("output_dir")
    basemaps =  configs.get("basemaps")

    scripts_dir = os.path.join(output_dir, "scripts")
    os.makedirs(scripts_dir, exist_ok=True)
    
    layers = []
    js = [tr("//--- Definições de Mapas Base---")]
    
    for basemap in basemaps:
        if  basemap in BASEMAP_PROVIDERS:
            provider = BASEMAP_PROVIDERS[ basemap ]
            name = provider["name"]
            url = provider["url"]
            attribution = provider["attribution"]

            layer_js = []
            layer_js.append("\tnew ol.layer.Tile({")
            
            if basemap == 'osm':
                layer_js.append("\t\tsource: new ol.source.OSM(),")
            else:
                layer_js.append("\t\tsource: new ol.source.XYZ({")
                layer_js.append(f"\t\t\turl: '{url}'")
                layer_js.append("\t\t}),")
            
            layer_js.append("\t\tvisible: false,")
            layer_js.append(f"\t\tattributions: '{attribution}',")
            layer_js.append(f"\t\ttitle: '{name}',")
            layer_js.append("\t\ttype: 'base'")
            layer_js.append("\t})")

            layers.append("\n".join(layer_js))
    
    js.append("const basemaps_layers = [")
    js.append(",\n".join(layers))
    js.append("];\n")
    js.append("if(basemaps_layers[0]) basemaps_layers[0].setVisible(true);\n")
    js.append("basemaps.getLayers().extend(basemaps_layers);\n")
    
    save_script(scripts_dir, "basemaps.js", js)

    return '<script src="scripts/basemaps.js"></script>'
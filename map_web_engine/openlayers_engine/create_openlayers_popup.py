import os
from ...utils import tr
from ..save_script import save_script

def create_openlayers_popup(configs):
    output_dir = configs.get("output_dir")
    
    scripts_dir = os.path.join(output_dir, "scripts")
    os.makedirs(scripts_dir, exist_ok=True)

    js = []

    #popup container
    js.append("const container = document.getElementById('popup');")
    js.append("const content = document.getElementById('popup-content');")
    js.append("const closer = document.getElementById('popup-closer');\n")

    #ol overlay
    js.append("const overlay = new ol.Overlay({")
    js.append("\telement: container,")
    js.append("\tautoPan: { animation: { duration: 250 } }")
    js.append("});\n")

    js.append("map.addOverlay(overlay);\n")

    #closer logic
    js.append("closer.onclick = function() {")
    js.append("\toverlay.setPosition(undefined);")
    js.append("\tcloser.blur();")
    js.append("\treturn false;")
    js.append("};\n")

    # map click event
    js.append("map.on('singleclick', function(evt) {")
    js.append("\tconst data = map.forEachFeatureAtPixel(evt.pixel, function(feature, layer) { return [feature, layer] });\n")
    
    js.append("\tif (data) {")
    js.append("\t\tconst [feature, layer] = data;")
    js.append("\t\tconst props = feature.getProperties();")
    js.append("\t\tconst attributesConfig = layer ? layer.get('attributesConfig') : {};")
    js.append("\t\tlet html = '<table class=\"popup-table\">';\n")
    
    js.append("\t\tfor (const key in props) {")
    js.append("\t\t\tif (key !== 'geometry' && props[key] !== null && props[key] !== undefined && props[key] !== '') {")
    js.append("\t\t\t\tlet value = props[key];\n")

    js.append("\t\t\t\tif (typeof value === 'number' && attributesConfig && attributesConfig[key] !== undefined) {")
    js.append("\t\t\t\t\tconst decimals = attributesConfig[key];")
    js.append(f"\t\t\t\t\tvalue = value.toFixed(decimals).toLocaleString('{tr('pt-BR')}');")
    js.append("\t\t\t\t}\n")

    js.append("\t\t\t\thtml += '<tr><th>' + key + '</th><td>' + value + '</td></tr>';")
    js.append("\t\t\t}")
    js.append("\t\t}\n")
    
    js.append("\t\thtml += '</table>';")
    js.append("\t\tcontent.innerHTML = html;")
    js.append("\t\toverlay.setPosition(evt.coordinate);")
    js.append("\t} else {")
    js.append("\t\toverlay.setPosition(undefined);")
    js.append("\t}")
    js.append("});\n")

    js.append("map.on('pointermove', function(e) {")
    js.append("\tconst hit = map.hasFeatureAtPixel(e.pixel);")
    js.append("\tmap.getTargetElement().style.cursor = hit ? 'pointer' : '';")
    js.append("});\n")

    save_script(scripts_dir, "popup.js", js)

    return '<script src="scripts/popup.js"></script>'
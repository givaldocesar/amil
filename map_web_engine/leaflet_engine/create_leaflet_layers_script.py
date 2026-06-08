import os
from ...utils.tr import tr
from ..save_script import save_script

def create_leaflet_layers_script(configs):
    output_dir = configs.get("output_dir")
    
    scripts_dir = os.path.join(output_dir, "scripts")
    os.makedirs(scripts_dir, exist_ok=True)

    layers_dir = os.path.join(scripts_dir, "layers")
    os.makedirs(layers_dir, exist_ok=True)

    tags_html_data = []

    for layer in configs.get("layers"):
        js = []

        #layer info
        layer_id = layer.layer_id
        name = layer.layer_name
        
        # estilo
        style = layer.style
        stroke_color = style.stroke_color
        stroke_width = style.stroke_width
        fill_color = style.fill_color
        radius = style.radius

        # popup rules
        popup_rules = []
        for attribute_name, attribute_config in layer.attributes.items():
            if attribute_config.export:
                rule = f"\n\t{{name: '{attribute_name}', "
                rule += f"is_float: {str(attribute_config.is_float).lower()}, "
                rule += f"decimals: {attribute_config.decimals} }}"
                popup_rules.append(rule)
        

        # Montando o JS
        js.append(tr("\n// Camada: {}").format(name))
        js.append(f"map.createPane('pane_{layer_id}');")
        js.append(f"map.getPane('pane_{layer_id}').style.zIndex = {layer.z_index};")
        js.append(f"map.getPane('pane_{layer_id}').style.pointerEvents = 'none';\n")

        # Regras POPUP
        if(len(popup_rules) > 0):
            js_popup_rules = "[" + ",".join(popup_rules) + "\n]"
            js.append(f"const popupRules_{layer_id} = {js_popup_rules};\n")

        # camada
        js.append(f"const layer_{layer_id} = L.geoJSON(data_{layer_id}, {{")
        js.append(f"\tpane: 'pane_{layer_id}',")
        js.append("\tinteractive: true,")
        js.append("\tstyle: function (feature) {")
        js.append("\t\treturn{")
        js.append(f"\t\t\tcolor: '{stroke_color}',")
        js.append(f"\t\t\tfillColor: '{fill_color}',")
        js.append(f"\t\t\tweight: {stroke_width},")
        js.append("\t\t\topacity: 1,")
        js.append("\t\t\tfillOpacity: 0.6")
        js.append("\t\t};")
        js.append("\t},")

        # configurações se é ponto
        if layer.is_point:
            js.append("\tpointToLayer: function(feature, latlng) {")
            js.append("\t\treturn L.circleMarker(latlng, {")
            js.append(f"\t\t\tradius: {radius},")
            js.append(f"\t\t\tcolor: '{stroke_color}',")
            js.append(f"\t\t\tfillColor: '{fill_color}',")
            js.append(f"\t\t\tweight: {stroke_width},")
            js.append("\t\t\topacity: 1,")
            js.append("\t\t\tfillOpacity: 0.6")
            js.append("\t\t});")
            js.append("\t},")

        if(len(popup_rules) > 0):
            #construido o popup dinâmico
            js.append("\tonEachFeature: function (feature, layer) {")
            js.append(f'''\t\tlet popupContent = '<div class="amil-popup"><b>{name}</b><hr><table style="width:100%; text-align:left;">';\n''')
            js.append(f"\t\tpopupRules_{layer_id}.forEach(function(rule) {{")
            js.append("\t\t\tlet value = feature.properties[rule.name];\n")
            js.append("\t\t\tif (value !== null && value !== undefined) {")
            js.append("\t\t\t\tif (rule.is_float && typeof value === 'number') {")
            js.append("\t\t\t\t\tvalue = value.toFixed(rule.decimals);")
            js.append("\t\t\t\t};\n")
            js.append("\t\t\t\tpopupContent += '<tr><th>' + rule.name + ':</th><td>' + value + '</td></tr>';")
            js.append("\t\t\t}")
            js.append("\t\t});\n")
            js.append("\t\tpopupContent += '</table></div>';")
            js.append("\t\tlayer.bindPopup(popupContent);")
            js.append("\t}")
        
        js.append("});\n")
        
        js.append("if (typeof layerControl !== 'undefined') {")
        js.append(f"\tlayerControl.addOverlay(layer_{layer_id}, '{name}');")
        js.append("}\n")

        js.append(f"map.addLayer(layer_{layer_id});")

        save_script(layers_dir, f"{layer_id}.js", js)
        tags_html_data.append(f'<script src="data/{layer_id}.js"></script>')
        tags_html_data.append(f'<script src="scripts/layers/{layer_id}.js"></script>')

    all_tags = "\n".join(tags_html_data)
    
    return all_tags
import os

def create_leaflet_layers_script(configs):
    output_dir = configs.get("output_dir")
    
    scripts_dir = os.path.join(output_dir, "scripts")
    os.makedirs(scripts_dir, exist_ok=True)

    js = ["// --- LAYERS ---"]
    tags_html_data = []

    for layer in configs.get("layers"):
        layer_id = layer.get("layer_id")
        name = layer.get("layer_name")
        
        style = layer.get("style", {})
        stroke_color = style.get("stroke_color", "#3388ff")
        stroke_width = style.get("stroke_width", 1.0)
        fill_color = style.get("fill_color", "#3388ff")
        is_polygon = style.get("is_polygon", False)

        js.append(f"\n// Camada: {name}")
        js.append(f"const style_{layer_id} = {{")
        js.append(f"\tcolor: '{stroke_color}',")
        js.append(f"\tweight: {stroke_width},")
        js.append(f"\topacity: 1.0,")
        
        if is_polygon:
            js.append(f"\tfillColor: '{fill_color}',")
            js.append(f"\tfillOpacity: 0.6")
        else:
            js.append(f"\tfill: false")
            
        js.append("};\n")

        js.append(f"const layer_{layer_id} = L.geoJSON(data_{layer_id}, {{")
        js.append(f"    style: style_{layer_id}")
        js.append(f"}}).addTo(map);\n")

        js.append(f"if (typeof layerControl !== 'undefined') {{")
        js.append(f"\tlayerControl.addOverlay(layer_{layer_id}, '{name}');")
        js.append(f"}}")
        
        tags_html_data.append(f'<script src="data/{layer_id}.js"></script>')

    js_path = os.path.join(scripts_dir, "layers.js")
    with open(js_path, "w", encoding="utf-8") as f:
        f.write("\n".join(js))

    all_tags = "\n".join(tags_html_data)
    all_tags += '\n<script src="scripts/layers.js"></script>'
    
    return all_tags
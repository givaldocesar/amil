import os, json
from ..save_script import save_script

def create_openlayers_layers_script(configs):
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

        if layer.is_point:
            geom_type = 'Point'
        elif layer.is_line: 
            geom_type = 'Line'
        else:
            geom_type = 'Polygon'
        
        # estilo
        style = layer.style
        stroke_color = style.stroke_color
        stroke_width = style.stroke_width
        fill_color = style.fill_color
        radius = style.radius

        #decimals rules
        decimals_rules = {}
        for name_attr, config_attr in layer.attributes.items():
            if config_attr.export and config_attr.is_float:
                decimals_rules[name_attr] = config_attr.decimals
                
        decimals_rules_js = json.dumps(decimals_rules)

        # ESTILO DA CAMADA
        if layer.is_point:
            js.append(f"const style_{layer_id} = new ol.style.Style({{")
            js.append("\timage: new ol.style.Circle({")
            js.append(f"\t\tradius: {radius},")
            js.append("\t\tstroke: new ol.style.Stroke({")
            js.append(f"\t\t\tcolor: '{stroke_color}',")
            js.append(f"\t\t\twidth: {stroke_width}")
            js.append("\t\t}),")
            js.append("\t\tfill: new ol.style.Fill({")
            js.append(f"\t\t\tcolor: '{fill_color}99'")
            js.append("\t\t})")
            js.append("\t})")
            js.append("});\n")
        else:
            js.append(f"const style_{layer_id} = new ol.style.Style({{")
            js.append("\tstroke: new ol.style.Stroke({")
            js.append(f"\t\tcolor: '{stroke_color}',")
            js.append(f"\t\twidth: {stroke_width}")
            js.append("\t}),")
            js.append("\tfill: new ol.style.Fill({")
            js.append(f"\t\tcolor: '{fill_color}99'")
            js.append("\t})")
            js.append("});\n")
        
        #CONFIGURAÇÕES DA CAMADA
        js.append(f"const layer_{layer_id} = new ol.layer.Vector({{")
        js.append(f"\ttitle: '{name}',")
        js.append(f"\tzIndex: {layer.z_index},")
        js.append(f"\tstyle: style_{layer_id},")
        js.append(f"\tgeomType: '{geom_type}',")
        js.append(f"\tfillColor: '{fill_color}',")
        js.append(f"\tstrokeColor: '{stroke_color}',")
        js.append(f"\tattributesConfig: {decimals_rules_js},")
        js.append("\tsource: new ol.source.Vector({")
        js.append(f"\t\tfeatures: new ol.format.GeoJSON().readFeatures(data_{layer_id}, {{")
        js.append("\t\t\tdataProjection: 'EPSG:4326',")
        js.append("\t\t\tfeatureProjection: 'EPSG:3857'")
        js.append("\t\t})")
        js.append("\t})")
        js.append("});\n")

        js.append(f"vector_layers.getLayers().push(layer_{layer_id});")
    
        save_script(layers_dir, f"{layer_id}.js", js)
        tags_html_data.append(f'<script src="data/{layer_id}.js"></script>')
        tags_html_data.append(f'<script src="scripts/layers/{layer_id}.js"></script>')
    
    all_tags = "\n".join(tags_html_data)
    return all_tags
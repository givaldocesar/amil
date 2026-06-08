import os
from ..save_script import save_script

def create_openlayers_css(configs):
    output_dir = configs.get("output_dir")
    
    scripts_dir = os.path.join(output_dir, "scripts")
    os.makedirs(scripts_dir, exist_ok=True)

    css = []

    #legend style
    css.append(".legend {")
    css.append("\ttop: 10px;")
    css.append("\tright: 10px;")
    css.append("\tbackground: rgba(255,255,255,0.95);")
    css.append("\tpadding: 5px;")
    css.append("\tborder-radius: 4px;")
    css.append("\tbox-shadow: 0 1px 4px rgba(0,0,0,0.2);")
    css.append("\tfont-family: sans-serif;")
    css.append("\tmin-width: 180px;")
    css.append("}\n")

    #collapse button
    css.append(".legend .collapse-button {")
    css.append("\twidth: 100%;")
    css.append("\ttext-align: left;")
    css.append("\tbackground: none;")
    css.append("\tborder: none;")
    css.append("\tfont-weight: bold;")
    css.append("\tcursor: pointer;")
    css.append("\tpadding: 5px;")
    css.append("\tfont-size: 14px;")
    css.append("\toutline: none;")
    css.append("}\n")

    css.append(".legend .collapse-button:hover {")
    css.append("\tbackground: none;")
    css.append("\tcolor: #000;")
    css.append("}\n")

    #layers content
    css.append(".layers-content {")
    css.append("\tpadding: 5px;")
    css.append("\tmax-height: 60vh;")
    css.append("\toverflow-y: auto;")
    css.append("}\n")

    save_script(scripts_dir, 'style.css', css)

    return '<link rel="stylesheet" href="scripts/style.css"/>'
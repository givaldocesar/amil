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

    # popup
    css.append(".ol-popup {")
    css.append("\tposition: absolute;")
    css.append("\tbackground-color: white;")
    css.append("\tbox-shadow: 0 1px 4px rgba(0,0,0,0.2);")
    css.append("\tpadding: 15px;")
    css.append("\tborder-radius: 10px;")
    css.append("\tborder: 1px solid #cccccc;")
    css.append("\tbottom: 12px;")
    css.append("\tleft: -50px;")
    css.append("\tmin-width: 280px;")
    css.append("}\n")

    css.append(".ol-popup:after, .ol-popup:before {")
    css.append("\tcontent: ' ';")
    css.append("\tpointer-events: none;")
    css.append("\tborder: solid transparent;")
    css.append("\tposition: absolute;")
    css.append("\ttop: 100%;")
    css.append("\theight: 0;")
    css.append("\twidth: 0;")
    css.append("}\n")

    css.append(".ol-popup:after {")
    css.append("\tmargin-left: -10px;")
    css.append("\tleft: 48px;")
    css.append("\tborder-top-color: white;")
    css.append("\tborder-width: 10px;")
    css.append("}\n")

    css.append(".ol-popup:before {")
    css.append("\tmargin-left: -11px;")
    css.append("\tleft: 48px;")
    css.append("\tborder-top-color: #cccccc;")
    css.append("\tborder-width: 11px;")
    css.append("}\n")
    
    # close popup button
    css.append(".ol-popup-closer {")
    css.append("\ttext-decoration: none;")
    css.append("\tposition: absolute;")
    css.append("\ttop: 2px;")
    css.append("\tright: 8px;")
    css.append("\tcolor: #333;")
    css.append("\tfont-weight: bold;")
    css.append("}\n")

    css.append(".ol-popup-closer:after { content: '✖'; }\n")
    
    # attributes table
    css.append(".popup-table {")
    css.append("\tmargin-top: 10px;")
    css.append("\twidth: 100%;")
    css.append("\tborder-collapse: collapse;")
    css.append("\tfont-size: 13px;")
    css.append("\tfont-family: sans-serif;")
    css.append("}\n")

    css.append(".popup-table th, .popup-table td {")
    css.append("\tpadding: 4px;")
    css.append("\tborder-bottom: 1px solid #eee;")
    css.append("\ttext-align: left;")
    css.append("}\n")

    css.append(".popup-table th {")
    css.append("\twidth: 40%;")
    css.append("\tfont-weight: bold;")
    css.append("\tcolor: #555;")
    css.append("}\n")

    save_script(scripts_dir, 'style.css', css)

    return '<link rel="stylesheet" href="scripts/style.css"/>'
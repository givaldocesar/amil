import os
from ...utils import tr
from ..save_script import save_script

def create_openlayers_legend_script(configs):
    output_dir = configs.get("output_dir")
    
    scripts_dir = os.path.join(output_dir, "scripts")
    os.makedirs(scripts_dir, exist_ok=True)

    js = []

    #cria a caixa principal
    js.append("const legendElement = document.createElement('div');")
    js.append("legendElement.className = 'ol-control ol-unselectable legend';\n")

    #botao para colapsar
    js.append("const toggleBtn = document.createElement('button');")
    js.append(f"toggleBtn.innerHTML = '− {tr('Legenda')}';")
    js.append("toggleBtn.className = 'collapse-button';\n")

    #layers content
    js.append("const contentDiv = document.createElement('div');")
    js.append("contentDiv.className = 'layers-content';\n")

    #expanded logic
    js.append("let isExpanded = true;")
    js.append("toggleBtn.onclick = function(e) {")
    js.append("\te.preventDefault();")
    js.append("\tisExpanded = !isExpanded;")
    js.append("\tcontentDiv.style.display = isExpanded ? 'block' : 'none';")
    js.append(f"\ttoggleBtn.innerHTML = isExpanded ? '− {tr('Legenda')}' : '+ {tr('Legenda')}';")
    js.append("}\n")
   
    js.append("legendElement.appendChild(toggleBtn);")
    js.append("legendElement.appendChild(contentDiv);\n")

    #basemaps
    js.append("if (basemaps.getLayers().getLength() > 0) {")
    js.append("\tconst baseTitle = document.createElement('div');")
    js.append(f'''\tbaseTitle.innerHTML = '<small style="color: #666; font-weight: bold;">{tr('MAPAS BASE')}</small>';''')
    js.append("\tbaseTitle.style.marginBottom = '5px';")
    js.append("\tcontentDiv.appendChild(baseTitle);\n")
    
    js.append("\tbasemaps.getLayers().forEach(function(layer, index) {")
    js.append("\t\tconst title = layer.get('title');")
    js.append("\t\tif (title) {")
    js.append("\t\t\tconst row = document.createElement('div');")
    js.append("\t\t\trow.style.margin = '4px 0';\n")
    
    js.append("\t\t\tconst rb = document.createElement('input');")
    js.append("\t\t\trb.type = 'radio';")
    js.append("\t\t\trb.name = 'basemap_group';")
    js.append("\t\t\trb.id = 'base_' + index;")
    js.append("\t\t\trb.checked = layer.getVisible(); ")
    js.append("\t\t\trb.onchange = function() {")
    js.append("\t\t\t\tbasemaps.getLayers().forEach(l => l.setVisible(false));")
    js.append("\t\t\t\tlayer.setVisible(true);")
    js.append("\t\t\t};\n")
    
    js.append("\t\t\tconst lbl = document.createElement('label');")
    js.append("\t\t\tlbl.htmlFor = 'base_' + index;")
    js.append("\t\t\tlbl.innerHTML = ' ' + title;")
    js.append("\t\t\tlbl.style.cursor = 'pointer';")
    js.append("\t\t\tlbl.style.fontSize = '13px';\n")

    js.append("\t\t\trow.appendChild(rb);")
    js.append("\t\t\trow.appendChild(lbl);")
    js.append("\t\t\tcontentDiv.appendChild(row);")
    js.append("\t\t}")
    js.append("\t});\n")

    js.append("\tconst hr = document.createElement('hr');")
    js.append("\thr.style.cssText = 'border: 0; border-top: 1px solid #ccc; margin: 10px 0;';")
    js.append("\tcontentDiv.appendChild(hr);")
    js.append("}\n")

    #set legen control
    js.append("const legendControl = new ol.control.Control({ element: legendElement });")
    js.append("map.addControl(legendControl);")
        
    save_script(scripts_dir, "legend.js", js)

    return f'<script src="scripts/legend.js"></script>'
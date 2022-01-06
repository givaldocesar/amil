from .objects import POINT, LINE, POLYGON, SINGLE
from qgis.PyQt.QtWidgets import *

GOOGLE_STREET = 'Google Street'
GOOGLE_SATELLITE = 'Google Satellite'
GOOGLE_HYBRID = 'Google Hybrid'


class Head:
    def __init__(self, title):
        self.code = '\t\t<meta charset="utf-8"/>\n'
        self.code += '\t\t<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        self.code += f'\t\t<title>{title}</title>\n\n'
        self.code += '\t\t<link rel="stylesheet" type="text/css" href="javascript/style.css" />\n'
        self.code += '\t\t<link rel="stylesheet" type="text/css" href="leaflet/leaflet.css"/>\n\n'      
        self.code += '\t\t<script type="text/javascript" src="leaflet/leaflet.js"></script>\n'
        self.code += '\t\t<script type="text/javascript" src="javascript/tab.js"></script>\n'
    
    def addLayerDataPath(self, layerName):
        self.code += f'\t\t<script type="text/javascript" src="data/{layerName}.js"></script>\n'
    
    def completeCode(self):
        return self.code


class Body:
    def __init__(self, title):
        self.code = '\t\t<div class="title">\n'
        self.code += f'\t\t\t<h1>{title}</h1>\n'
        self.code += '\t\t</div>\n'
        self.code += '\t\t<div class="maintab">\n'
        self.code += '\t\t\t<button id="mapBtn" class="mainTablinks" onclick="openMainTab(event, \'mapArea\')">Mapa</button>\n'
        self.code += '\t\t\t<button class="mainTablinks" onclick="openMainTab(event, \'attributesArea\')">Tabelas de Atributos</button>\n'
        self.code += '\t\t</div>\n'
        self.code += '\t\t<div id="mapArea" class="mainTabContent">\n'
        self.code += '\t\t\t<div id="map"></div>\n'
        self.code += '\t\t</div>\n'
        
        self.layersButton = ''
        self.layersTable = ''
    
    def addLayerTableButton(self, layerName, label):
        self.layersButton  += f'\t\t\t\t<button id="{layerName}_btn" class="tablinks" onclick="openTab(event, \'{layerName}_tab\')">{label}</button>\n'
    
    def addLayerTableArea(self, layerName):
        self.layersTable += f'\t\t\t<div id="{layerName}_tab" class="tabcontent"></div>\n'
    
    def completeCode(self):
        code = self.code
        code += '\n\t\t<div id="attributesArea" class="mainTabContent">\n'
        code +=	'\t\t\t<div class="tab">\n'
        code += self.layersButton
        code += '\t\t\t</div>\n'
        code += self.layersTable
        code += '\t\t</div>\n'
        
        return code
 
 
class Map:
    def __init__(self):
        self.mapPanes = '// PAINEIS\n'
        self.baseLayers = '// CAMADAS BASE\n'
        self.layers = '// CAMADAS VETORIAIS\n'
        self.layersControl = '// CONTROLE DE CAMADAS\n'
        self.legend = '// LEGENDA\n'
        self.legendBody = ''
    
    @staticmethod
    def writeSymbology(layer, expression):
        symbology = ''
        for key, symbol in layer.symbology[expression].items():
            if key != 'label':
                if key == 'color' or key == 'fillColor':
                    symbology += f'\t\t\t\t\t\t{key}: \'rgba({symbol})\',\n'
                else:
                    symbology += f'\t\t\t\t\t\t{key}: {symbol},\n'
    
        symbology = symbology[:-2]
        
        return symbology
    
    @staticmethod
    def translateExpression(expression):
        translated = ''
        splitted = expression.split(' ')
        while splitted:
            word = splitted[0]

            if word:
                # Verifica se é um atributo
                if word[0] == '"':
                    translated += f' feature.properties[{word}'
                    splitted.remove(word)
                    
                    # Verifica se o atributo tem mais de uma palavra 
                    if word[-1] != '"':
                        # Verifica se é a ultima palavra do atributo
                        while splitted[0][-1] != '"':
                            word = splitted[0]
                            translated += ' ' + word
                            splitted.remove(word)
                    
                        word = splitted[0]
                        translated += ' ' + word + ']'
                    else:
                        translated += ']'
                        continue
                
                # Verifica se é uma igualdade
                elif word == '=':
                    translated += ' =='
                
                # Verifica o termo IS
                elif word == 'is':
                    splitted.remove(word)
                    
                    word = splitted[0]
                    if word == 'not':
                        translated += ' !='
                    else:
                        translated += ' =='
                        continue

                # Verifica o termo NULL
                elif word.lower() == 'null':
                    translated += ' ""'
                    
                # adiciona outras palavras
                elif word.lower() == 'and':
                    translated += ' &&'
                elif word.lower() == 'or':
                    translated += ' ||'
                # Verifica se é um valor
                elif word[0] == "'":
                    translated += f' {word}'
                    splitted.remove(word)
                    
                    # Verifica se o valor tem mais de uma palavra 
                    if word[-1] != "'":
                        # Verifica se é a ultima palavra do atributo
                        while splitted[0][-1] != "'":
                            word = splitted[0]
                            translated += ' ' + word
                            splitted.remove(word)
                    
                        word = splitted[0]
                        translated += ' ' + word
                else:
                    translated += ' ' + word

            if word in splitted:
                splitted.remove(word)
                     
        return translated
    
    @staticmethod
    def createPopUpLayer(layer):
        popUp = f"'<h4>CAMADA: {layer.label}</h4><br/>'  +\n"
    
        for attribute in layer.popUpAttributes:
            if attribute.enabled:
                popUp += f"\t\t\t\t\t\t\t'<b>{attribute.label.upper()}:</b>&ensp;' + feature.properties['{attribute.name}'] + '<br/>' +\n"
    
        return popUp[:-2]
     
    @staticmethod 
    def createLegendForFeature(geometry, symbol):
        if not symbol["label"]:
            symbol["label"] = '-------'
        
        if geometry == POINT:
            return f'<svg class="legendIcon"><circle cx="9" cy="9" r="5" stroke="rgba({symbol["color"]})" stroke-width="2" fill="rgba({symbol["fillColor"]})"></svg>{symbol["label"]}'
        elif geometry == LINE:
            return f'<svg class="legendIcon"><line x1="0" y1="9" x2="18" y2="9" stroke="rgba({symbol["color"]})" stroke-width="3"></svg>{symbol["label"]}'
        elif geometry == POLYGON:
            return f'<svg class="legendIcon"><rect width="18" height="18" stroke="rgba({symbol["color"]})" stroke-width="3" fill="rgba({symbol["fillColor"]})"></svg>{symbol["label"]}'
        else:
            return symbol['label']
    
    @staticmethod
    def translatePosition(position):
        if position == 'Inferior Direita':
            position = 'bottomright'
        elif position == 'Inferior Esquerda':
            position = 'bottomleft'
        elif position == 'Superior Direita':
            position = 'topright'
        elif position == 'Superior Esquerda':
            position = 'topleft'
        
        return position
        
    @staticmethod
    def createScale():
        code =  '//ESCALA\n'
        code += 'L.control.scale({\n'
        code += '\tmaxWidth: 250,\n'
        code += '\timperial: false\n'
        code += '}).addTo(map);\n\n'
        return code
    
    @staticmethod
    def createShowHideFunctions():
        code = 'function layerON (event){\n'
        code +=	'\tvar className = event.name + \'_lgd\';\n'
        code +=	'\tvar legendItems = document.getElementsByClassName(className);\n'
        code +=	'\tfor (var i = 0; i < legendItems.length; i++) {\n'
        code +=	'\t\tlegendItems[i].style.display = \'block\';\n'
        code +=	'\t}\n'	
        code += '}\n\n'

        code += 'function layerOFF (event){\n'
        code +=	'\tvar className = event.name + \'_lgd\';\n'
        code +=	'\tvar legendItems = document.getElementsByClassName(className);\n'
        code +=	'\tfor (var i = 0; i < legendItems.length; i++) {\n'
        code +=	'\t\tlegendItems[i].style.display = \'none\';\n'
        code +=	'\t}\n'
        code += '}\n\n'
        
        code +=  'map.on(\'overlayadd\', layerON);\n'
        code += 'map.on(\'overlayremove\', layerOFF);\n\n'
        
        return code
    
    def addBaseLayers(self, layers, standard):
        if layers[GOOGLE_STREET]:
            self.baseLayers += 'var googleStreet = L.tileLayer(\'http://{s}.google.com/vt/lyrs=m,h&x={x}&y={y}&z={z}\',{\n'
            self.baseLayers += '\tmaxZoom: 20,\n'
            self.baseLayers += '\tsubdomains:[\'mt0\',\'mt1\',\'mt2\',\'mt3\'],\n'
            self.baseLayers += '\tattribution: \'<a href="https://www.google.at/permissions/geoguidelines/attr-guide.html">Map data ©2021 Google</a>\'\n'
            self.baseLayers += '});\n'
            if standard == GOOGLE_STREET:
                self.baseLayers += 'googleStreet.addTo(map);\n'
            self.baseLayers += 'baseMaps["Google Street"] = googleStreet;\n\n'
            
    
        if layers[GOOGLE_SATELLITE]:
            self.baseLayers += 'var googleSatellite = L.tileLayer(\'http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}\',{\n'
            self.baseLayers += '\tmaxZoom: 20,\n'
            self.baseLayers += '\tsubdomains:[\'mt0\',\'mt1\',\'mt2\',\'mt3\'],\n'
            self.baseLayers += '\tattribution: \'<a href="https://www.google.at/permissions/geoguidelines/attr-guide.html">Map data ©2021 Google</a>\'\n'
            self.baseLayers += '});\n'
            if standard == GOOGLE_SATELLITE:
                self.baseLayers += 'googleSatellite.addTo(map);\n'
            self.baseLayers += 'baseMaps[\'Google Satellite\'] = googleSatellite;\n\n'
            
    
        if layers[GOOGLE_HYBRID]:
            self.baseLayers += 'var googleHybrid = L.tileLayer(\'http://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}\',{\n'
            self.baseLayers += '\tmaxZoom: 20,\n'
            self.baseLayers += '\tsubdomains:[\'mt0\',\'mt1\',\'mt2\',\'mt3\'],\n'
            self.baseLayers += '\tattribution: \'<a href="https://www.google.at/permissions/geoguidelines/attr-guide.html">Map data ©2021 Google</a>\'\n'
            self.baseLayers += '});\n'
            if standard == GOOGLE_HYBRID:
                self.baseLayers += 'googleHybrid.addTo(map);\n'
            self.baseLayers += 'baseMaps["Google Hybrid"] = googleHybrid;\n\n'
                
    def addLayerMap(self, layerName, layer):
        self.layers += f'var {layerName} = L.geoJSON({layerName}_data, {{\n'
        self.mapPanes += f'map.createPane(\'pane_{layer.order}\').style.zIndex = {499 - layer.order};\n'
        
        if layer.geometry == POINT:
            self.layers += f'\t\t\tpointToLayer: function(geoJsonPoint, latlng) {{return L.circleMarker(latlng, {{pane: \'pane_{layer.order}\'}})}},\n'
        else:
            self.layers += f'\t\t\tpane: \'pane_{layer.order}\',\n'
        
        if layer.type == SINGLE:
            self.layers += '\t\t\tstyle: {\n'
            self.layers += self.writeSymbology(layer, 'symbol')
            
            self.legendBody += f'\tdiv.innerHTML += \t\'<dt class="{layerName}_lgd">{self.createLegendForFeature(layer.geometry, layer.symbology["symbol"])}</dt>\';\n'
        else:
            self.layers += '\t\t\tstyle: function (feature) {\n'
            self.legendBody += f'\tdiv.innerHTML += \t\'<dt class="{layerName}_lgd">{layer.label}</dt>\';\n'
            
            first = True
            for expression in layer.symbology:
                self.legendBody += f'\tdiv.innerHTML += \t\t\'<dd class="{layerName}_lgd">{self.createLegendForFeature(layer.geometry, layer.symbology[expression])}</dd>\';\n'
                
                if expression != 'ELSE':
                    if first:
                        self.layers += f'\t\t\t\tif ({self.translateExpression(expression)}) {{\n'   
                    else:
                        self.layers += f'else if ({self.translateExpression(expression)}) {{\n'
                    
                    self.layers += '\t\t\t\t\treturn {\n'
                    self.layers += self.writeSymbology(layer, expression)
                    self.layers += '\n\t\t\t\t\t}\n'
                    self.layers += '\t\t\t\t} '
                
                first = False
                
            if 'ELSE' in layer.symbology:
                self.layers += 'else {\n'
                self.layers += '\t\t\t\t\treturn {\n'
                self.layers += self.writeSymbology(layer, 'ELSE')
                self.layers += '\n\t\t\t\t\t}\n'
                self.layers += '\t\t\t\t}'
        
        self.layers += '\n\t\t\t}'
        
        if layer.enablePopUp:
            self.layers += ',\n\t\t\tonEachFeature: function (feature, layer){\n'
            self.layers += '\t\t\t\tlayer.on({click: clickedFeature});\n'
            self.layers += '\t\t\t\tlayer.bindPopup(function (layer) {\n'
            self.layers += f'\t\t\t\t\treturn {self.createPopUpLayer(layer)}\n'
            self.layers += '\t\t\t\t});\n'
            self.layers += '\t\t\t}' 
            
        self.layers += '\n}).addTo(map);\n'
        self.layers += f'overlayMaps[\'{layerName[1:]}\'] = {layerName};\n\n'
        
    def createLegendMap(self, legendPosition):
        legendPosition = self.translatePosition(legendPosition)
        
        self.legend += f'var legend = L.control({{position: \'{legendPosition}\'}});\n'
        self.legend +=  'legend.onAdd = function (map) {\n'
        self.legend +=  '\tvar div = L.DomUtil.create(\'div\', \'info legend\');\n'
        self.legend +=  '\tdiv.innerHTML = \'<dl>\';\n'
        self.legend +=  self.legendBody 
        self.legend +=  '\tdiv.innerHTML += \'</dl>\';\n'
        self.legend +=  '\treturn div\n'
        self.legend +=  '}\n'
        self.legend +=  'legend.addTo(map);\n\n'
    
    def createLayersControl(self, controlPosition):
        controlPosition = self.translatePosition(controlPosition)
        
        self.layersControl +=  'L.control.layers(baseMaps, overlayMaps, {\n'
        self.layersControl += f'\tposition: \'{controlPosition}\',\n'
        self.layersControl +=  '\tcollapsed: false,\n'
        self.layersControl +=  '\tsortLayers: true\n'
        self.layersControl +=  '}).addTo(map);\n\n'
    
    def code(self, showHideEnabled):
        _code = 'var map = L.map(\'map\', {});\n\n'
        _code += self.mapPanes + '\n'
        _code += 'var baseMaps = {};\n'
        _code += 'var overlayMaps = {};\n\n'
        _code += self.baseLayers
        _code += self.layers
        
        _code += '//Função que dá zoom sobre a feição clicada\n'
        _code += 'function clickedFeature(e) {\n'
        _code += '\tvar feature = e.target;\n'
        _code += '\tif (feature.feature.geometry.type == \'Point\' ) {\n'
        _code += '\t\tmap.setView(feature.getLatLng(), 16);\n' 
        _code += '\t} else {\n'
        _code += '\t\tmap.fitBounds(feature.getBounds());\n'
        _code += '\t}\n'
        _code += '}\n\n'
      
        _code += self.legend
        _code += self.createScale()
        _code += self.layersControl
        _code += self.createShowHideFunctions()
        
        _code += '// CALCULA A AREA QUE COBRE TODAS AS CAMADAS\n'
        _code += 'var bounds = {xmin: 180, ymin: 90, xmax: -180, ymax: -90};\n'
        _code += 'for (var layer in overlayMaps) {\n'
        _code += '\tvar layerBounds = overlayMaps[layer].getBounds();\n'
        _code += '\tif (bounds.xmin > layerBounds.getSouthWest().lng) {bounds.xmin = layerBounds.getSouthWest().lng};\n'
        _code += '\tif (bounds.ymin > layerBounds.getSouthWest().lat) {bounds.ymin = layerBounds.getSouthWest().lat};\n'
        _code += '\tif (bounds.xmax < layerBounds.getNorthEast().lng) {bounds.xmax = layerBounds.getNorthEast().lng};\n'
        _code += '\tif (bounds.ymax < layerBounds.getNorthEast().lat) {bounds.ymax = layerBounds.getNorthEast().lat};\n'
        _code += '}\n'
        _code += 'map.fitBounds([\n'
        _code += '\t[bounds.ymin, bounds.xmin],\n'
        _code += '\t[bounds.ymax, bounds.xmax]\n'
        _code += ']);\n'
        
        return _code


class AttributesTable:
    def __init__(self):
        self.tables =  'function filter(evt, column) {\n'
        self.tables += '\t// Declare variables\n'
        self.tables += '\tvar input, filter, table, tr, td, i, txtValue;\n'
        self.tables += '\tinput = evt.target;\n'
        self.tables += '\tfilter = input.value.toUpperCase();\n'
        self.tables += '\ttable = evt.path[4];\n'
        self.tables += '\ttr = table.getElementsByTagName("tr");\n\n'
        self.tables += '\t// Loop through all table rows, and hide those who don\'t match the search query\n'
        self.tables += '\tfor (i = 2; i < tr.length; i++) {\n'
        self.tables += '\t\ttd = tr[i].getElementsByTagName("td")[column];\n'
        self.tables += '\t\tif (td) {\n'
        self.tables += '\t\t\ttxtValue = td.textContent || td.innerText;\n'
        self.tables += '\t\t\tif (txtValue.toUpperCase().indexOf(filter) > -1) {\n'
        self.tables += '\t\t\t\ttr[i].style.display = "";\n'
        self.tables += '\t\t\t} else {\n'
        self.tables += '\t\t\t\ttr[i].style.display = "none";\n'
        self.tables += '\t\t\t}\n'
        self.tables += '\t\t}\n'
        self.tables += '\t}\n'
        self.tables += '}\n\n'
        
        self.tables += 'function goToMap(layer, featureID){\n'
        self.tables += '\tvar feature = layer._layers[featureID];\n'
        self.tables += '\tif (feature.feature.geometry.type == \'Point\' ) {\n'
        self.tables += '\t\tmap.setView(feature.getLatLng(), 16);\n'
        self.tables += '\t} else {\n'
        self.tables += '\t\tmap.fitBounds(feature.getBounds());\n'
        self.tables += '\t}\n\n'
        self.tables += '\tdocument.getElementById(\'mapBtn\').click();\n'
        self.tables += '\tfeature.openPopup();\n\n'
        self.tables += '\tif (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {\n'
        self.tables += '\t\tlayer.bringToFront();\n'
        self.tables += '\t};\n'
        self.tables += '}\n\n'
        
    
    def addAttributesTable(self, layerName, layer):
        table = f'tableHTML_{layerName} = \'<table id="{layerName}_table">\';\n'
        
        headers = f'tableHTML_{layerName} += \t\'<tr>\';\n'        
        headers += f'tableHTML_{layerName} += \t\t\'<th>Mapa</th>\';\n'
        
        filters = f'tableHTML_{layerName} += \t\'<tr>\';\n'
        filters += f'tableHTML_{layerName} += \t\t\'<td></td>\';\n'    
        
        row = ''
        
        count = 1
        for attribute in layer.attributesTable:
            if attribute.enabled:
                headers += f'tableHTML_{layerName} += \t\t\'<th>{attribute.label}</th>\';\n'
                row += f'\ttableHTML_{layerName} += \t\'<td>\' + feature.properties[\'{attribute.name}\'] + \'</td>\';\n'
                
                if attribute.filter:
                    filters += f'tableHTML_{layerName} += \t\t\'<td><input type="text" onkeyup="filter(event, {count})" placeholder="Procurar {attribute.label}"></td>\';\n'
                else:
                    filters += f'tableHTML_{layerName} += \t\t\'<td></td>\';\n' 
                count += 1
        
        headers += f'tableHTML_{layerName} += \t\'</tr>\';\n'
        filters += f'tableHTML_{layerName} += \t\'</tr>\';\n\n'        
        
        table += headers
        table += filters
        
        table += f'var {layerName}_IDs = Object.keys({layerName}._layers);\n'
        table += f'for (var i=0; i < {layerName}_IDs.length; i++){{\n'
        table += f'\tvar feature = {layerName}._layers[{layerName}_IDs[i]].feature;\n'
        table += f'\ttableHTML_{layerName} += \'<tr>\';\n' 
        table += f'\ttableHTML_{layerName} += \t\'<td onclick="goToMap({layerName}, \' + {layerName}_IDs[i] + \')"><img src="javascript/icon.png" width="32px" height="32px"/></td>\';\n'            
        table += row
        table += f'\ttableHTML_{layerName} += \'</tr>\';\n' 
        table +=  '}\n\n'
        
        table += f'tableHTML_{layerName} += \'</table>\';\n'
        table += f'document.getElementById(\'{layerName}_tab\').innerHTML = tableHTML_{layerName};\n'
        
        self.tables += table + '\n'
    
    def code(self):
        return self.tables
        

class WebPage:
    def __init__(self, title):
        self.head = Head(title)
        self.body = Body(title)
    
    def html(self):
        html = '<!DOCTYPE html>\n'
        html += '<html lang="pt-br">\n'
        html += '\t<head>\n'
        html += self.head.completeCode()
        html += '\t</head>\n'
        html += '\t<body>\n'
        html += self.body.completeCode()
        html += '\t\t<script type="text/javascript" src="javascript/map.js"></script>\n'
        html += '\t\t<script type="text/javascript" src="javascript/attributes.js"></script>\n'
        html += '\t\t<script>document.getElementById(\'mapBtn\').click();</script>'
        html += '\t</body>\n'
        html += '</html>'
        return html
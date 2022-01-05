from qgis.PyQt.QtWidgets import *
from qgis.PyQt.QtCore import pyqtSignal, QObject

def printf(obj):
    QMessageBox.information(None, 'PRINT', str(obj))



POINT = 'Ponto'
LINE = 'Linha'
POLYGON = 'Polígono'

SINGLE = 'Símbolo Simples'
CATEGORIZED = 'Categorizado'
GRADUATED = 'Graduado'
RULED = 'Baseado em Regra'


def convertColor(color):
    channels = color.split(',')
    return f'{channels[0]}, {channels[1]}, {channels[2]}, {int(channels[3])/255:.2f}'


def convertWeight(weight):
    return 5 * float(weight)


class Attribute:
    def __init__(self, name, label):
        self.name = name
        self.label = label
        self.filter = True
        self.enabled = True
    
    def __str__(self):
        return f'NAME: {self.name}\nLABEL: {self.label}\nFILTER:{self.filter}\nENABLE:{self.enabled}'

 
class Layer(QObject):
    rendererChanged = pyqtSignal(QObject)
    
    def __init__(self, VectorLayer, order):
        super().__init__()
        self.order = order
        self.id = VectorLayer.id()
        self.layerName = VectorLayer.name()
        self.label = self.layerName
        
        self.enabled = True
        self.enablePopUp = True
        self.enableTable = True
        
        VectorLayer.rendererChanged.connect(lambda: self.rendererChanged.emit(self))
        
        self.__setAttributes(VectorLayer.attributeAliases())
        
    def __str__(self):
        return f'ID: {self.id}\nOrder: {self.order}'
    
    def __setAttributes(self, attributes):
        self.popUpAttributes = []
        self.attributesTable = []

        for attribute in attributes:
            if attributes[attribute]:
                self.popUpAttributes.append(Attribute(attribute, attributes[attribute]))
                self.tableAttributes.append(Attribute(attribute, attributes[attribute]))
            else:
                self.popUpAttributes.append(Attribute(attribute, attribute))
                self.attributesTable.append(Attribute(attribute, attribute))
    
    def getAttribute(self, name):
        for attribute in self.attributesTable:
            if attribute.name == name:
                return attribute
    
    def getPopUpAttribute(self, name):
        for attribute in self.popUpAttributes:
            if attribute.name == name:
                return attribute
    
    def setEnablePopUp(self, enable: bool):
         self.enablePopUp = enable
    
    def setEnableTable(self, enable: bool):
         self.enableTable = enable
    
    def setSymbology(self, layer):
        renderer = layer.renderer()
        
        if renderer.type() == 'singleSymbol':
            self.type = SINGLE
            symbol = renderer.symbol().symbolLayer(0).properties()
            self.symbology = {'symbol': self.style(layer, symbol)}
            self.symbology['symbol']['label'] = layer.name()
        
        elif renderer.type() == 'categorizedSymbol':
            self.type = CATEGORIZED
            
            attribute = renderer.classAttribute()
            categories = renderer.categories()
    
            self.symbology = {}
            for category in categories:
                symbol = category.symbol().symbolLayer(0).properties()
                if category.value():
                    self.symbology[f'"{attribute}" = \'{category.value()}\''] = self.style(layer, symbol)
                    self.symbology[f'"{attribute}" = \'{category.value()}\'']['label'] = category.label()
                else:
                    self.symbology['ELSE'] = self.style(layer, symbol)
                    self.symbology['ELSE']['label'] = category.label()
            
        elif renderer.type() == 'graduatedSymbol':
            self.type = GRADUATED
           
            attribute = renderer.classAttribute()
            ranges = renderer.ranges()
                
            self.symbology = {}
            for _range in ranges:
                symbol = _range.symbol().symbolLayer(0).properties()
                self.symbology[f'"{attribute}" >= {_range.lowerValue()} and "{attribute}" < {_range.upperValue() + 10**-10}'] = self.style(layer, symbol)
                self.symbology[f'"{attribute}" >= {_range.lowerValue()} and "{attribute}" < {_range.upperValue() + 10**-10}']['label'] = _range.label()
        
        elif renderer.type() == 'RuleRenderer':
            self.type = RULED
            
            self.symbology = {}
            for rule in renderer.rootRule().descendants():
                symbol = rule.symbol().symbolLayer(0).properties()
                self.symbology[rule.filterExpression()] = self.style(layer, symbol)
                self.symbology[rule.filterExpression()]['label'] = rule.label()

            
class PointLayer(Layer):
    def __init__(self, VectorLayer, order):
        super().__init__(VectorLayer, order)
        self.geometry = POINT
        self.setSymbology(VectorLayer)
    
    @staticmethod
    def style(layer, symbol):
        return {'opacity': layer.opacity(),
                'fillOpacity': layer.opacity(),
                'radius': float(symbol['size']),
                'weight': convertWeight(symbol['outline_width']),
                'color': convertColor(symbol['outline_color']),
                'fillColor': convertColor(symbol['color'])}
    
    
class LineLayer(Layer):
    def __init__(self, VectorLayer, order):
        super().__init__(VectorLayer, order)
        self.geometry = LINE
        self.setSymbology(VectorLayer)
    
    @staticmethod
    def style(layer, symbol):
        return {'opacity': layer.opacity(),
                'fillOpacity': layer.opacity(),
                'weight': convertWeight(symbol['line_width']),
                'color': convertColor(symbol['line_color'])}  


class PolygonLayer(Layer):
    def __init__(self, VectorLayer, order):
        super().__init__(VectorLayer, order)
        self.geometry = POLYGON
        self.setSymbology(VectorLayer)
    
    @staticmethod
    def style(layer, symbol):
        return {'opacity': layer.opacity(),
                'fillOpacity': layer.opacity(),
                'weight': convertWeight(symbol['outline_width']),
                'color': convertColor(symbol['outline_color']),
                'fillColor': convertColor(symbol['color'])}
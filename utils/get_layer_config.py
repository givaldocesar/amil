from qgis.core import QgsWkbTypes
from qgis.PyQt.QtCore import QVariant
from .layer_config import *

def get_layer_config(layer):
    config = LayerConfig(
        layer_id=layer.id(),
        layer_name=layer.name(),
        is_polygon=(layer.geometryType() == QgsWkbTypes.PolygonGeometry),
        is_line=(layer.geometryType() == QgsWkbTypes.LineGeometry),
        is_point=(layer.geometryType() == QgsWkbTypes.PointGeometry)
    )

    renderer = layer.renderer()
    if renderer and renderer.symbol():
        symbol = renderer.symbol()
        symbol_layer = symbol.symbolLayer(0) if symbol.symbolLayerCount() > 0 else None
    
        # CORES
        if config.is_polygon:
            config.style.fill_color = symbol.color().name()
            if symbol_layer and hasattr(symbol_layer, 'strokeColor'):
                config.style.stroke_color = symbol_layer.strokeColor().name()
        
        elif config.is_line:
            config.style.stroke_color = symbol.color().name()
            config.style.fill_color = symbol.color().name()
        
        elif config.is_point:
            config.style.fill_color = symbol.color().name()
            if symbol_layer and hasattr(symbol_layer, 'strokeColor'):
                config.style.stroke_color = symbol_layer.strokeColor().name()
            if hasattr(symbol, 'size'):
                config.style.radius = symbol.size() * 1.5
        
        # ESPESSURA DA LINHA
        if symbol_layer and hasattr(symbol_layer, 'width'):
            config.style.stroke_width = symbol_layer.width()

        #ATRIBUTOS DA CAMADA
        for field in layer.fields():
            is_float = field.type() == QVariant.Double
            config.attributes[field.name()] = AttributeConfig(
                name=field.name(),
                is_float=is_float
            )
    
    return config
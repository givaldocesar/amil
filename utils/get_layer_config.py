from qgis.core import QgsWkbTypes, QgsRenderContext
from .layer_config import *

def get_layer_config(layer):
    renderer = layer.renderer()
    symbol = None

    if renderer:
        context = QgsRenderContext()
        symbols = renderer.symbols(context)

        if symbols:
            symbol = symbols[0]

    config = LayerConfig(
        layer_id=layer.id(),
        layer_name=layer.name(),
        is_polygon=(layer.geometryType() == QgsWkbTypes.PolygonGeometry),
        is_point=(layer.geometryType() == QgsWkbTypes.PointGeometry)
    )

    if symbol:
        config.style.stroke_color = symbol.color().name()

        if hasattr(symbol, "size"):
            config.style.radius = symbol.size() * 1.5

        if hasattr(symbol, "fillColor"):
            config.style.fill_color = symbol.fillColor().name()

        if hasattr(symbol, 'width'):
            config.style.stroke_width = symbol.width()
    
    return config
from qgis.core import *

def get_layers_extension(layers):
    project = QgsProject.instance()
    rect_total = QgsRectangle()
    crs_wgs84 = QgsCoordinateReferenceSystem("EPSG:4326")
    first = True

    for layer in layers:
        layer_id = layer.layer_id
        layer = project.mapLayer(layer_id)
        
        if not layer:
            continue

        transform = QgsCoordinateTransform(layer.crs(), crs_wgs84, project)
        extension_wgs84 = transform.transformBoundingBox(layer.extent())

        if first:
            rect_total = extension_wgs84
            first = False
        else:
            rect_total.combineExtentWith(extension_wgs84)
    
    if first:           #Não tem camadas
        return None

    return [
        [rect_total.yMinimum(), rect_total.xMinimum()],
        [rect_total.yMaximum(), rect_total.xMaximum()]
    ]
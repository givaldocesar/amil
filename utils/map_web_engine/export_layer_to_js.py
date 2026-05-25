import os
from qgis.core import *
from ..tr import tr

def export_layer_to_js(layer_id, output_dir):
    layer = QgsProject.instance().mapLayer(layer_id)
    
    if not layer:
        print(tr("Aviso: Camada {} não encontrada no projeto.").format(layer_id))
        return False

    data_dir = os.path.join(output_dir, "data")
    os.makedirs(data_dir, exist_ok=True)

    gjson_temp_path = os.path.join(data_dir, f"{layer_id}_temp.geojson")
    js = os.path.join(data_dir, f"{layer_id}.js")

    options = QgsVectorFileWriter.SaveVectorOptions()
    options.driverName = "GeoJSON"
    options.fileEncoding = "UTF-8"

    crs_wgs84 = QgsCoordinateReferenceSystem("EPSG:4326")
    transform = QgsCoordinateTransform(layer.crs(), crs_wgs84, QgsProject.instance())
    options.ct = transform
    
    error, error_string, *_ = QgsVectorFileWriter.writeAsVectorFormatV3(
        layer, 
        gjson_temp_path, 
        QgsProject.instance().transformContext(), 
        options
    )

    if error == QgsVectorFileWriter.NoError:
        with open(gjson_temp_path, "r", encoding="utf-8") as f:
            geojson_data = f.read()

        js_content = f"var data_{layer_id} = {geojson_data};\n"
        
        with open(js, "w", encoding="utf-8") as f:
            f.write(js_content)
            
        os.remove(gjson_temp_path)
        return True
    else:
        print(tr("Erro ao exportar a camada {layer_name}: {error}").format(
            layer_name=layer.name(),
            error=error_string
        ))
        return False

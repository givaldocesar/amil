import os
from .leaflet_engine import *
from .openlayers_engine import *
from .export_layer_to_js import *
from ..tr import tr

def map_web_engine(configs):
    """
    Motor centralizador de exportação do AMIL 2.0.
    Recebe a configuração completa da UI e gera a estrutura do WebGIS.
    """

    output_dir = configs.get("output_dir")
    engine = configs.get("engine", "openlayers")
    mode = configs.get("modo", "online")
    layers = configs.get("layers", [])
    
    # 1. Validação básica da pasta
    if not output_dir:
        print(tr("Erro: Nenhuma pasta de saída foi selecionada."))
        return False

    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    for layer in layers:
        layer_id = layer.get("layer_id")
        name = layer.get("name")
        success = export_layer_to_js(layer_id, output_dir)
        if not success:
            print(tr("Falha ao processar os dados da camada {}.").format(name))

    html = ""
    if engine == "openlayers":
        pass
        #html = create_openlayers_template(basemaps)
    else:
        html = create_leaflet_template(configs)

    index_path = os.path.join(output_dir, "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html)

    return tr("Sucesso! Mapa Web gerado em: {}").format(index_path)
        
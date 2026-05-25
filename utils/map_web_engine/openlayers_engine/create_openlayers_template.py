def create_openlayers_template(basemaps):    
    html = f"""<!DOCTYPE html>
    <html>
    <head>
        <title>Amil WebGIS - OpenLayers</title>
        <meta charset="utf-8" />
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/ol@v8.2.0/ol.css" />
        <script src="https://cdn.jsdelivr.net/npm/ol@v8.2.0/dist/ol.js"></script>
        <style>
            html, body, #map {{ width: 100%; height: 100%; margin: 0; padding: 0; }}
        </style>
    </head>
    <body>
        <div id="map"></div>
        <script>
            // Inicializa o mapa em OpenLayers
            var map = new ol.Map({{
                target: 'map',
                layers: [
                    new ol.layer.Tile({{ source: new ol.source.OSM() }})
                ],
                view: new ol.view.View({{
                    center: ol.proj.fromLonLat([-47.9292, -15.7801]),
                    zoom: 4
                }})
            }});
            console.log("Mapas base selecionados: {basemaps}");
        </script>
    </body>
    </html>"""

    return html
import os

def create_leaflet_core_script(configs):
    output_dir = configs.get("output_dir")
    lat, long = configs.get("center")

    scripts_dir = os.path.join(output_dir, "scripts")
    os.makedirs(scripts_dir, exist_ok=True)

    js = [
        f"const map = L.map('map').setView([{lat}, {long}], 4);\n",
        "const layerControl = L.control.layers(null, null, {",
        "\tcollapsed: false",
        "}).addTo(map);"
    ]

    script_path = os.path.join(scripts_dir, "core.js")
    with open(script_path, "w", encoding="utf-8") as f:
        f.write("\n".join(js))

    return '<script src="scripts/core.js"></script>'
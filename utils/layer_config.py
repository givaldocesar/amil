from dataclasses import dataclass, field

@dataclass
class StyleConfig:
    stroke_color: str = "#3388FF"
    stroke_width: float = 1.0
    fill_color: str = "#3388FF75"
    radius: float = 6.0

@dataclass
class LayerConfig:
    #infos
    layer_id: str
    layer_name: str
    export_geometry: bool = True
    export_attributes: bool = False

    #styles
    style: StyleConfig = field(default_factory=StyleConfig)

    is_polygon: bool = False
    is_point: bool = False
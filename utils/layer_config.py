from dataclasses import dataclass, field

@dataclass
class StyleConfig:
    stroke_color: str = "#3388FF"
    stroke_width: float = 1.0
    fill_color: str = "#3388FF75"
    radius: float = 6.0

@dataclass
class AttributeConfig:
    name: str
    export: bool = True
    is_float: bool = False
    decimals: int = 2
    sortable: bool = False
    filterable: bool = False

@dataclass
class LayerConfig:
    #infos
    layer_id: str
    layer_name: str
    z_index: int = 0
    export_geometry: bool = True
    export_attributes: bool = False
    is_polygon: bool = False
    is_point: bool = False
    is_line: bool = False

    #styles
    style: StyleConfig = field(default_factory=StyleConfig)

    #attributes
    attributes: dict[str, AttributeConfig] = field(default_factory=dict)



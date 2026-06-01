from qgis.PyQt.QtWidgets import QCheckBox, QLabel, QSpinBox
from .tr import tr

def create_attributes_row(layout, row, attribute_config):
    export = QCheckBox(attribute_config.name)
    export.setChecked(attribute_config.export)
    export.toggled.connect(lambda value, config=attribute_config: setattr(config, 'export', value))
    layout.addWidget(export, row, 0)

    sortable = QCheckBox(tr("Ordenável"))
    sortable.setChecked(attribute_config.sortable)
    sortable.toggled.connect(lambda value, config=attribute_config: setattr(config, 'sortable', value))
    layout.addWidget(sortable, row, 1)

    filterable = QCheckBox(tr("Filtrável"))
    filterable.setChecked(attribute_config.filterable)
    filterable.toggled.connect(lambda value, config=attribute_config: setattr(config, 'filterable', value))
    layout.addWidget(filterable, row, 2)

    if attribute_config.is_float:
        lbl_decimals = QLabel(tr("Decimais:"))
        spin_decimals = QSpinBox()
        spin_decimals.setRange(0, 6)
        spin_decimals.setValue(attribute_config.decimals)
        spin_decimals.valueChanged.connect(lambda value, config=attribute_config: setattr(config, 'decimals', value))
        
        layout.addWidget(lbl_decimals, row, 3)
        layout.addWidget(spin_decimals, row, 4)

    layout.setRowStretch(row, 1)
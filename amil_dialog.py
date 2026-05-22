# -*- coding: utf-8 -*-
import os
from qgis.core import QgsProject, Qgis, QgsApplication
from qgis.PyQt import uic
from qgis.PyQt.QtCore import Qt, QSize
from qgis.PyQt.QtWidgets import *


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'amil_dialog_base.ui'))

EXPORT_CHK_NAME = "export_chk"
ATTRIBUTES_CHK_NAME = "attributes_chk"

class AmilDialog(QDialog, FORM_CLASS):    
    def __init__(self, iface, parent=None):
        super().__init__(parent)
        self.setupUi(self)      
        self.iface = iface

        #FICA LIGADO NAS CAMADAS
        QgsProject.instance().layersAdded.connect(self.sync_layers)
        QgsProject.instance().layersRemoved.connect(self.sync_layers)

        #ARROW UP LAYERS
        icon_up = QgsApplication.getThemeIcon("/mActionArrowUp.svg")
        self.up_layer_btn.setIcon(icon_up)
        self.up_layer_btn.setIconSize(QSize(20, 20)) # Ajuste o tamanho se achar necessário
        self.up_layer_btn.setText("")
        self.up_layer_btn.clicked.connect(self.up_layer)

        # ARROW DOWN LAYERS
        icon_down = QgsApplication.getThemeIcon("/mActionArrowDown.svg")
        self.down_layer_btn.setIcon(icon_down)
        self.down_layer_btn.setIconSize(QSize(20, 20))
        self.down_layer_btn.setText("")
        self.down_layer_btn.clicked.connect(self.down_layer)

        self.export_btn.clicked.connect(self.layers_to_export)

    def create_layer_row(self, item, layer_name):
        row = QWidget()
        layout = QHBoxLayout(row)
        layout.setContentsMargins(0, 0, 0, 0)

        export = QCheckBox()
        export.setChecked(True)
        export.setObjectName(EXPORT_CHK_NAME)

        label = QLabel(layer_name)
        font = label.font()
        font.setBold(True)
        label.setFont(font)

        attributes = QCheckBox("Tabela de Atributos")
        attributes.setChecked(True)
        attributes.setObjectName(ATTRIBUTES_CHK_NAME)

        layout.addWidget(export)
        layout.addWidget(label)
        layout.addStretch()
        layout.addWidget(attributes)

        self.layers.setItemWidget(item, row)

    def change_position(self, current_row, value):
        current_item = self.layers.item(current_row)
        if not current_item:
            return
        
        row = self.layers.itemWidget(current_item)
        if not row:
            return
        
        export_checked = row.findChild(QCheckBox, EXPORT_CHK_NAME).isChecked()
        attributes_checked = row.findChild(QCheckBox, ATTRIBUTES_CHK_NAME).isChecked()
        layer_name = row.findChild(QLabel).text()

        self.layers.blockSignals(True)
        item = self.layers.takeItem(current_row)
        self.layers.insertItem(current_row + value, item)

        self.create_layer_row(item, layer_name)

        new_row = self.layers.itemWidget(item)
        if new_row:
            new_row.findChild(QCheckBox, EXPORT_CHK_NAME).setChecked(export_checked)
            new_row.findChild(QCheckBox, ATTRIBUTES_CHK_NAME).setChecked(attributes_checked)
        
        self.layers.setCurrentRow(current_row + value)
        self.layers.blockSignals(False)
    
    def up_layer(self):
        current_row = self.layers.currentRow()
        if current_row > 0:
            self.change_position(current_row, -1)
 
    def down_layer(self):
        current_row = self.layers.currentRow()
        if current_row < self.layers.count() and current_row >= 0:
            self.change_position(current_row, 1)
    

    def sync_layers(self):
        if not self.isVisible():
            return
        
        self.layers.blockSignals(True)

        qgis_layers = {
            layer.id(): layer for layer in QgsProject.instance().mapLayers().values() 
            if layer.type() == Qgis.LayerType.Vector and layer.isSpatial()
        }

        layers_ids = []
        for i in range(self.layers.count() - 1, -1, -1):
            item = self.layers.item(i)

            if item:
                id = item.data(Qt.UserRole)
                if id not in qgis_layers:
                    self.layers.takeItem(i)
                else:
                    layers_ids.append(id)

        for layer_id, layer in qgis_layers.items():
            if layer_id not in layers_ids:
                item = QListWidgetItem()
                item.setData(Qt.UserRole, layer_id)
                self.layers.addItem(item)
                self.create_layer_row(item, layer.name())
        
        self.layers.blockSignals(False)
 
    def layers_to_export(self):
        layers = []
        
        for i in range(self.layers.count()):
            item = self.layers.item(i)
            layer_id = item.data(Qt.UserRole)
            row = self.layers.itemWidget(item)

            if row:
                export_chk = row.findChild(QCheckBox, EXPORT_CHK_NAME)
                attributes_chk = row.findChild(QCheckBox, ATTRIBUTES_CHK_NAME)
            
                if export_chk and export_chk.isChecked():
                    layers.append({
                        "id": layer_id,
                        "export_attributes": attributes_chk.isChecked() if attributes_chk else False
                    })
        
        print(layers)
        return layers
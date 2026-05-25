# -*- coding: utf-8 -*-
import os
from dataclasses import asdict
from qgis.core import QgsProject, Qgis, QgsApplication
from qgis.PyQt import uic
from qgis.PyQt.QtCore import Qt, QSize
from qgis.PyQt.QtWidgets import *
from .utils import *


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'amil_dialog_base.ui'))

class AmilDialog(QDialog, FORM_CLASS):    
    def __init__(self, iface, parent=None):
        super().__init__(parent)
        self.setupUi(self)      
        self.iface = iface

        #FICA LIGADO NAS CAMADAS
        QgsProject.instance().layersAdded.connect(self.sync_layers)
        QgsProject.instance().layersRemoved.connect(self.sync_layers)

        #EVENTOS DA LISTA
        self.layers.itemDoubleClicked.connect(toggle_item_state)
        self.check_all.clicked.connect(lambda _: self.change_checked_state(Qt.Checked))
        self.uncheck_all.clicked.connect(lambda _: self.change_checked_state(Qt.Unchecked))

        #ARROW UP LAYERS
        icon_up = QgsApplication.getThemeIcon("/mActionArrowUp.svg")
        self.up_layer_btn.setIcon(icon_up)
        self.up_layer_btn.setIconSize(QSize(20, 20))
        self.up_layer_btn.setText("")
        self.up_layer_btn.clicked.connect(self.up_layer)

        # ARROW DOWN LAYERS
        icon_down = QgsApplication.getThemeIcon("/mActionArrowDown.svg")
        self.down_layer_btn.setIcon(icon_down)
        self.down_layer_btn.setIconSize(QSize(20, 20))
        self.down_layer_btn.setText("")
        self.down_layer_btn.clicked.connect(self.down_layer)

        #OUTPUT
        self.set_output.clicked.connect(self.select_output_dir)
        self.export_btn.clicked.connect(self.export)

    def change_checked_state(self, state):
        for i in range(self.layers.count()):
            item = self.layers.item(i)
            if item:
                item.setCheckState(state)

    def change_layer_position(self, current_row, value):
        self.layers.blockSignals(True)

        current_item = self.layers.takeItem(current_row)
        if current_item:
            self.layers.insertItem(current_row + value, current_item)
            self.layers.setCurrentRow(current_row + value)
        
        self.layers.blockSignals(False)
    
    def up_layer(self):
        current_row = self.layers.currentRow()
        if current_row > 0:
            self.change_layer_position(current_row, -1)
 
    def down_layer(self):
        current_row = self.layers.currentRow()
        if current_row < self.layers.count() and current_row >= 0:
            self.change_layer_position(current_row, 1)
    
    def sync_layers(self):
        if not self.isVisible():
            return
        
        self.layers.blockSignals(True)

        qgis_layers = [
            layer for layer in QgsProject.instance().mapLayers().values() 
            if layer.type() == Qgis.LayerType.Vector and layer.isSpatial() 
        ]

        layers_ids = []
        for i in range(self.layers.count() - 1, -1, -1):
            item = self.layers.item(i)

            if item:
                id = item.data(Qt.UserRole)
                if id not in qgis_layers:
                    self.layers.takeItem(i)
                else:
                    layers_ids.append(id)

        for layer in qgis_layers:
            if layer.id() not in layers_ids:
                item = create_list_item(layer)
                self.layers.addItem(item)
        
        self.layers.blockSignals(False)
 
    def select_output_dir(self):
        directory = QFileDialog.getExistingDirectory(self, self.tr("Selecionar Diretório de Saída"))
        if directory:
            self.output_dir.setText(directory)

    def get_global_configs(self):
        engine = "openlayers" if self.openlayers.isChecked() else "leaflet"
        mode = "offline" if self.offline.isChecked() else "online"
        output_dir = self.output_dir.text()
        title = self.page_title.text() or QgsProject.instance().baseName() 
        
        basemaps = []
        if self.google_sat.isChecked(): basemaps.append("google_sat")
        if self.google_terrain.isChecked(): basemaps.append("google_terrain")
        if self.google_hybrid.isChecked(): basemaps.append("google_hybrid")
        if self.esri.isChecked(): basemaps.append("esri")
        if self.carto.isChecked(): basemaps.append("cartodb_positron")
        if self.osm.isChecked(): basemaps.append("osm")

        lat = self.latitude.value()
        long = self.longitude.value()

        return {
            "engine": engine,
            "mode": mode,
            "output_dir": output_dir,
            "basemaps": basemaps,
            "center": [lat, long],
            "title": title
        }

    def get_layers_configs(self):
        layers_payload = []
        
        for i in range(self.layers.count()):
            item = self.layers.item(i)
            layer_id = item.data(Qt.UserRole)
            layer = QgsProject.instance().mapLayer(layer_id)
            if layer:
                config = get_layer_config(layer)
                layers_payload.append(asdict(config))
        
        return layers_payload

    def export(self):
        global_configs = self.get_global_configs()
        global_configs["layers"] = self.get_layers_configs()

        if(global_configs["output_dir"] == ""):
            QMessageBox.warning(self, self.tr("Aviso"), self.tr("Por favor, selecione um diretório de saída válido."))
        else:
            message = map_web_engine(global_configs)
            QMessageBox.warning(self, self.tr("Aviso"), message)
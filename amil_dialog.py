# -*- coding: utf-8 -*-
import os, webbrowser
from qgis.core import QgsProject, Qgis, QgsApplication
from qgis.PyQt import uic
from qgis.PyQt.QtCore import Qt, QSize
from qgis.PyQt.QtGui import QColor
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
        project = QgsProject.instance()
        project.layersAdded.connect(self.sync_layers)
        project.layersRemoved.connect(self.sync_layers)

        #EVENTOS DA LISTA
        self.layers.itemDoubleClicked.connect(toggle_item_state)
        self.check_all.clicked.connect(lambda: self.change_layers_checked_state(Qt.Checked))
        self.uncheck_all.clicked.connect(lambda: self.change_layers_checked_state(Qt.Unchecked))

        #EVENTOS DE MODO
        self.online.clicked.connect(lambda: self.enable_basemap(True))
        self.offline.clicked.connect(lambda: self.enable_basemap(False))

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

        #SYNC BUTTON
        icon_sync = QgsApplication.getThemeIcon('/mActionRefresh.svg')
        self.sync_style_button.setIconSize(QSize(20, 20))
        self.sync_style_button.setText("")
        self.sync_style_button.setIcon(icon_sync)
        self.sync_style_button.clicked.connect(self.sync_style)

        #OUTPUT
        self.set_output.clicked.connect(self.select_output_dir)
        self.export_btn.clicked.connect(self.export)

        #EXTENT vs CENTER
        self.extent_to_layers.stateChanged.connect(self.change_extent_to_layers)

        #CACHE DE CONFIGURAÇÃO DAS CAMADAS
        self.layers_configs_cache = {}

        #CONFIGS DAS CAMADAS
        self.current_layer.currentIndexChanged.connect(self.layer_changed)
    
        self.stroke_button.colorChanged.connect(
            lambda value: self.save_layer_style_property('stroke_color', value))
        self.fill_button.colorChanged.connect(
            lambda value: self.save_layer_style_property('fill_color', value))
        self.stroke_width_spin.valueChanged.connect(
            lambda value: self.save_layer_style_property('stroke_width', value))
        self.radius_spin.valueChanged.connect(
            lambda value: self.save_layer_style_property('radius', value))
        
        self.sync_layers()

    def change_extent_to_layers(self, state):
        if(state == Qt.Checked):
            self.latitude.setEnabled(False)
            self.longitude.setEnabled(False)
        else:
            self.latitude.setEnabled(True)
            self.longitude.setEnabled(True)

    def change_layers_checked_state(self, state):
        for i in range(self.layers.count()):
            item = self.layers.item(i)
            if item:
                item.setCheckState(state)
    
    def enable_basemap(self, enable):
        self.google_hybrid.setEnabled(enable)
        self.google_sat.setEnabled(enable)
        self.google_terrain.setEnabled(enable)
        self.osm.setEnabled(enable)
        self.esri.setEnabled(enable)
        self.carto.setEnabled(enable)

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
        self.layers.blockSignals(True)
        self.current_layer.blockSignals(True)

        root = QgsProject.instance().layerTreeRoot()
        qgis_layers = {}

        for node in root.findLayers():
            layer = node.layer()
            if layer and layer.type() == Qgis.LayerType.Vector and layer.isSpatial():
                qgis_layers[layer.id()] = layer

        layers_ids = set()
        for i in range(self.layers.count() - 1, -1, -1):
            item = self.layers.item(i)

            if item:
                id = item.data(Qt.UserRole)
                if id not in qgis_layers:
                    self.layers.takeItem(i)
                    self.current_layer.removeItem(i)
                    self.layers_configs_cache.pop(id, None)
                else:
                    layers_ids.add(id)

        for layer_id, layer in qgis_layers.items():
            if layer_id not in layers_ids:
                item = create_list_item(layer)
                self.layers.addItem(item)
                self.current_layer.addItem(layer.name(), layer.id())

                if layer_id not in self.layers_configs_cache:
                    config = get_layer_config(layer)
                    self.layers_configs_cache[layer_id] = config
        
        self.current_layer.model().sort(0, Qt.AscendingOrder)

        self.layers.blockSignals(False)
        self.current_layer.blockSignals(False)
        self.layer_changed()
 
    def sync_style(self):
        layer_id = self.current_layer.currentData()
        if not layer_id:
            return

        layer = QgsProject.instance().mapLayer(layer_id)
        if not layer:
            return
        
        config_qgis = get_layer_config(layer)
        if layer_id in self.layers_configs_cache:
            self.layers_configs_cache[layer_id].style = config_qgis.style

        self.layer_changed()
    
    def select_output_dir(self):
        directory = QFileDialog.getExistingDirectory(self, self.tr("Selecionar Diretório de Saída"))
        if directory:
            self.output_dir.setText(directory)

    def save_layer_style_property(self, property, value):
        layer_id = self.current_layer.currentData()
        if layer_id and layer_id in self.layers_configs_cache:
            current_style = self.layers_configs_cache[layer_id].style
            setattr(current_style, property, value)

    def layer_changed(self):
        layer_id = self.current_layer.currentData()
        if not layer_id: return

        layer = QgsProject.instance().mapLayer(layer_id)
        if not layer: return

        #CRIA OU PEGA A CONFIG
        config = self.layers_configs_cache[layer_id]
        
        self.stroke_button.blockSignals(True)
        self.fill_button.blockSignals(True)
        self.stroke_width_spin.blockSignals(True)
        self.radius_spin.blockSignals(True)
        
        # BOTOES DE CORES
        self.stroke_button.setColor(QColor(config.style.stroke_color))
        self.fill_button.setColor(QColor(config.style.fill_color))
        
        # ESPESSURA DA LINHA
        self.stroke_width_spin.setValue(config.style.stroke_width)

        # TAMANHO DO PONTO
        self.radius_spin.setValue(config.style.radius)
        
        # DESABILITA O QUE SERVE PRA GEOMETRIA
        self.radius_spin.setEnabled(config.is_point)
        self.fill_button.setEnabled(not config.is_line)

        self.stroke_button.blockSignals(False)
        self.fill_button.blockSignals(False)
        self.stroke_width_spin.blockSignals(False)
        self.radius_spin.blockSignals(False)

        layout = self.attributes_contents.layout()
        while layout.count() > 0:
            child = layout.takeAt(0)
            if child.widget():
               child.widget().deleteLater()
        
        row = 0
        for _, attribute_config in config.attributes.items():
            create_attributes_row(layout, row, attribute_config)
            row += 1

    def get_global_configs(self):
        engine = "openlayers" if self.openlayers.isChecked() else "leaflet"
        mode = "offline" if self.offline.isChecked() else "online"
        output_dir = self.output_dir.text()
        title = self.page_title.text() or QgsProject.instance().baseName() 
        
        basemaps = []

        if mode == "online":
            if self.google_sat.isChecked(): basemaps.append("google_sat")
            if self.google_terrain.isChecked(): basemaps.append("google_terrain")
            if self.google_hybrid.isChecked(): basemaps.append("google_hybrid")
            if self.esri.isChecked(): basemaps.append("esri")
            if self.carto.isChecked(): basemaps.append("cartodb_positron")
            if self.osm.isChecked(): basemaps.append("osm")

        lat = self.latitude.value()
        long = self.longitude.value()

        auto_extent = self.extent_to_layers.isChecked()

        return {
            "engine": engine,
            "mode": mode,
            "output_dir": output_dir,
            "basemaps": basemaps,
            "center": [lat, long],
            "title": title,
            "auto_extent": auto_extent
        }

    def export(self):
        global_configs = self.get_global_configs()
        layers_to_export = []
        current_z_index = 1000 + self.layers.count()

        for i in range(self.layers.count()):
            item = self.layers.item(i)
            if item and item.checkState() == Qt.Checked:
                layer_id = item.data(Qt.UserRole)
                if layer_id in self.layers_configs_cache:
                    config = self.layers_configs_cache[layer_id]
                    config.z_index = current_z_index
                    current_z_index -= 1 
                    layers_to_export.append(config)

        global_configs["layers"] = layers_to_export

        if(global_configs["output_dir"] == ""):
            QMessageBox.warning(self, self.tr("Aviso"), self.tr("Por favor, selecione um diretório de saída válido."))
        else:
            message = map_web_engine(global_configs)
            QMessageBox.information(self, self.tr("Aviso"), message)
            
            if self.open_map.isChecked():
                index_path = os.path.join(global_configs["output_dir"], "index.html")
                if os.path.exists(index_path):
                    webbrowser.open(f"file:///{index_path}")
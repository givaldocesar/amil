from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QListWidgetItem

def toggle_item_state(item):
    if item.checkState() == Qt.Checked:
        item.setCheckState(Qt.Unchecked)
    else:
        item.setCheckState(Qt.Checked)

def create_list_item(layer):
    item = QListWidgetItem(layer.name())
    item.setData(Qt.UserRole, layer.id())
    
    item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
    item.setCheckState(Qt.Checked)
    
    font = item.font()
    font.setBold(True)
    item.setFont(font)

    return item
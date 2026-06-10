# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets
from qgis.core import QgsMapLayerProxyModel

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'hankaku_converter_dialog_base.ui'))


class HankakuConverterDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setFixedSize(self.size())

        self.mMapLayerComboBox.setFilters(QgsMapLayerProxyModel.Filter.VectorLayer)
        self.mMapLayerComboBox.layerChanged.connect(self.mFieldComboBox.setLayer)
        self.mFieldComboBox.setAllowEmptyFieldName(True)
        self.pushButton_options.setStyleSheet('text-align: left; padding-left: 2px;')
        self.pushButton_options.clicked.connect(self._toggle_options)

    def _toggle_options(self):
        visible = not self.widget_options.isVisible()
        self.widget_options.setVisible(visible)
        self.pushButton_options.setText(
            '▼ オプション　Option' if visible else '▶ オプション　Option')

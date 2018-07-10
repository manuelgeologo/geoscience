import os

from PyQt5 import QtCore, uic
from PyQt5 import QtWidgets
#from PyQt5 import QtGui

from qgis.core import *
from qgis.utils import *
from qgis.gui import *

from .QgisDialogBase import QgisDialogBase

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'drilltrace_dialog_base.ui'))


class DrillTraceDialog(QtWidgets.QDialog, QgisDialogBase, FORM_CLASS):
    def __init__(self, manager, parent=None):
        """Constructor."""
        super(DrillTraceDialog, self).__init__(parent)
        
        # Keep a reference to the DrillManager
        self.drillManager = manager
        
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
    
        self.lbDataLayer.setFilters(QgsMapLayerProxyModel.NoGeometry)
        self.initLayer(self.drillManager.dataLayer, self.lbDataLayer, ["lith", "geol"])
        self.lbDataLayer.layerChanged.connect(self.onDataLayerChanged)
        self.teSuffix.setText(self.drillManager.dataSuffix)

        self.onDataLayerChanged()

    def onDataLayerChanged(self):
        layer = self.lbDataLayer.currentLayer()
        if layer is not None and layer.isValid():
            self.fbDataId.setLayer(layer)
            self.initField(self.drillManager.dataId, self.fbDataId, ["holeid", "id", "hole", "name"])
            self.fbDataFrom.setLayer(layer)
            self.initField(self.drillManager.dataFrom, self.fbDataFrom, ["from", "start", "depth"])
            self.fbDataTo.setLayer(layer)
            self.initField(self.drillManager.dataTo, self.fbDataTo, ["to","end"])
            #Load the list widget
            self.listFields.clear()
            for field in layer.fields():
                item = QtWidgets.QListWidgetItem()
                item.setText(field.name())
                item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
                item.setCheckState(QtCore.Qt.Checked)
                self.listFields.addItem(item)
        else:
            self.fbDataId.setCurrentIndex(-1)
            self.fbDataFrom.setCurrentIndex(-1)
            self.fbDataTo.setCurrentIndex(-1)
            self.listFields.clear()
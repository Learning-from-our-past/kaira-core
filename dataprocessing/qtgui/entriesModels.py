from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QAbstractListModel, QVariant, QModelIndex
from PyQt5.QtGui import  QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog
from PyQt5.QtCore import pyqtSlot
import qtgui.utils as utils

"""Holds entries listing and handling related code for mainwindow."""

class EntriesListModel(QStandardItemModel):

    def __init__(self, listview, parent):
        super(EntriesListModel, self).__init__(listview)
        self.parent = parent
        listview.clicked.connect(self.itemSelected)
        #listview.selectionModel().selectionChanged.connect(self.itemSelected)

    def addItems(self, entries):
        for entry in entries:
            self.appendRow(EntriesListItemModel(entry))

    #Maybe these event handlers should be moved to view itself, but for now they can reside here.
    def itemSelected(self, index):
        #TODO: EMIT SIGNAL TO SET RELEVANT DATA TO TEXTFIELDS.
        self.parent.entrySelectedSignal.emit(self.itemFromIndex(index).getDataEntry())



class EntriesListItemModel(QStandardItem):
    #http://pyqt.sourceforge.net/Docs/PyQt4/qabstractlistmodel.html
    dataEntry = None    #xml, results

    def __init__(self, dataEntry):
        super(EntriesListItemModel, self).__init__()
        self.dataEntry = dataEntry
        self.setText(self._constructText())

    def getDataEntry(self):
        return self.dataEntry

    def _constructText(self):
        return utils.makeSubStrForListViews(self.dataEntry["xml"].text) +"..."

from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtCore import QAbstractListModel, QVariant, QModelIndex
from PyQt5.QtGui import  QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog, QListView
from PyQt5.QtCore import pyqtSlot
import qtgui.utils as utils

"""Holds entries listing and handling related code for mainwindow."""

class EntriesListModel(QStandardItemModel):

    def __init__(self, listview, parent):
        super(EntriesListModel, self).__init__(listview)
        self.parent = parent

    def addItems(self, entries):
        for entry in entries:
            self.appendRow(EntriesListItemModel(entry))






class EntriesListView(QListView):

    entrySelectedSignal = pyqtSignal(dict, name="entrySelected")

    def __init__(self, parent):
        super(EntriesListView, self).__init__(parent)
        self.parent = parent

    @pyqtSlot(int)
    def _selectionChanged(self, selection):
        if len(selection.indexes()) > 0:
            self.entrySelectedSignal.emit(self.model().itemFromIndex(selection.indexes()[0]).getDataEntry())

    def setModel(self, model):
        super(EntriesListView, self).setModel(model)
        self.selectionModel().selectionChanged.connect(self._selectionChanged)


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
        if "name" in self.dataEntry["xml"].attrib:
            return utils.makeSubStrForListViews(self.dataEntry["xml"].attrib["name"])
        else:
            return utils.makeSubStrForListViews(self.dataEntry["xml"].text) +"..."

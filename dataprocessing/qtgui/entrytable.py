from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtCore import QAbstractListModel, QVariant, QModelIndex
from PyQt5.QtGui import  QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog, QTableView
from PyQt5.QtCore import pyqtSlot
import qtgui.utils as utils

"""Holds entries listing and handling related code for mainwindow."""

class EntryTableModel(QStandardItemModel):

    def __init__(self, tableview, parent):
        super(EntryTableModel, self).__init__(tableview)
        self.parent = parent

    def addItems(self, entry):
        #generate tableitems from dict's keys and add them to the columns:
        items = self._getDataFromDict(entry["extractionResults"])
        self.appendColumn(items["keyColumn"])
        self.appendColumn(items["valueColumn"])

    def _getDataFromDict(self, d):
        keyColumn = []
        valueColumn = []
        for key, value in d.items():

            if type(value) is list:
                for i in value:
                    elements = self._getDataFromDict(i)
                    keyColumn = keyColumn + elements["keyColumn"]
                    valueColumn = valueColumn + elements["valueColumn"]
            elif type(value) is dict:
                elements = self._getDataFromDict(value)
                keyColumn = keyColumn + elements["keyColumn"]
                valueColumn = valueColumn + elements["valueColumn"]
            else:
                keyColumn.append(EntryTableItemModel(key))
                valueColumn.append(EntryTableItemModel(value))

        return {"keyColumn" : keyColumn, "valueColumn": valueColumn}



class EntryTableView(QTableView):

    entrySelectedSignal = pyqtSignal(dict, name="entrySelected")

    def __init__(self, parent):
        super(EntryTableView, self).__init__(parent)
        self.parent = parent

    @pyqtSlot(int)
    def _selectionChanged(self, selection):
        if len(selection.indexes()) > 0:
            self.entrySelectedSignal.emit(self.model().itemFromIndex(selection.indexes()[0]).getDataEntry())

    def setModel(self, model):
        super(EntryTableView, self).setModel(model)
        self.selectionModel().selectionChanged.connect(self._selectionChanged)


class EntryTableItemModel(QStandardItem):
    #http://pyqt.sourceforge.net/Docs/PyQt4/qabstractlistmodel.html
    dataEntry = None    #xml, results

    def __init__(self, text):
        super(EntryTableItemModel, self).__init__()
        self.setText(str(text))

    def getDataEntry(self):
        return self.dataEntry

    def _constructText(self):
        return utils.makeSubStrForListViews(self.dataEntry["xml"].text) +"..."

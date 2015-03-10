from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import  QStandardItemModel
from qtgui.layouts.ui_mainwindow import Ui_MainWindow
import processData
import threading
import time
import qtgui.utils
from qtgui.entriesModels import *
from qtgui.xmlImport import XmlImport
from qtgui.entriesModels import *
from qtgui.entrytable import *
from qtgui.entrytree import *
from PyQt5.QtGui import  QStandardItem, QStandardItemModel


class Mainwindow(QMainWindow):

    dataEntries = []
    missingDataEntries = {}
    missingDataListing = []
    entriesListModel = None



    def __init__(self, parent=None):
        super(Mainwindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.xmlImporter = XmlImport(self)
        #Connect actions to slots
        self.ui.actionOpen_XML_for_analyze.triggered.connect(self.xmlImporter.openXMLFile)
        self.xmlImporter.finishedSignal.connect(self._entriesImportedFromFile)
        self.ui.entriestListView.entrySelectedSignal.connect(self._updateEntryTextFields)

        #set models.
        self.entriesListModel = EntriesListModel(self.ui.entriestListView, self)
        self.ui.entriestListView.setModel(self.entriesListModel)
        self.ui.entriestListView.show()

        self.entryTableModel = EntryTableModel(self.ui.tableView, self)
        self.ui.tableView.setModel(self.entryTableModel)
        self.ui.tableView.show()


        self.ui.entriesComboBox.clear()
        self.ui.entriesComboBox.setCurrentIndex(0)
        self.ui.entriesComboBox.currentIndexChanged.connect(self._changedEntriesComboBox)


        #http://doc.qt.digia.com/4.6/itemviews-editabletreemodel.html
        """self.treeModel = TreeModel()
        self.treeModel.setColumnCount(2)
        self.ui.treeView.setModel(self.treeModel)
        item = TreeItem("jaska", None)
        self.treeModel.setItem(item)
        self.treeModel.setItem(TreeItem("jaska2", item))"""

    def _updateEntriesList(self, items):
        self.entriesListModel.clear()
        self.entriesListModel.addItems(items)

    def _updateEntriesComboBox(self):
        self.ui.entriesComboBox.clear()
        self.missingDataListing = []
        self.ui.entriesComboBox.addItem("ALL " + str(len(self.dataEntries)))
        for key, value in self.missingDataEntries.items():
            self.ui.entriesComboBox.addItem(str(key) + " " + str(len(value)))
            self.missingDataListing.append(value)

    @pyqtSlot(int)
    def _changedEntriesComboBox(self, index):
        if index > 0:
            self._updateEntriesList(self.missingDataListing[index-1])
        else:
            self._updateEntriesList(self.dataEntries)

    @pyqtSlot(dict)
    def _updateEntryTextFields(self, entry):
        self.ui.rawTextTextEdit.setPlainText(entry["xml"].text)
        self.entryTableModel.clear()
        self.entryTableModel.addItems(entry)
        previous = entry["xml"].getprevious()
        if previous is not None:
            self.ui.previousEntryTextEdit.setPlainText(previous.text)
        else:
            self.ui.previousEntryTextEdit.setPlainText("")

    @pyqtSlot(dict)
    def _entriesImportedFromFile(self, resultsFromFile):

        self.dataEntries = resultsFromFile["entries"]
        self.missingDataEntries = resultsFromFile["errors"]
        self._updateEntriesList(self.dataEntries)
        self._updateEntriesComboBox()


def start():
    import sys
    app = QApplication(sys.argv)
    fixingtool = Mainwindow()
    fixingtool.show()
    sys.exit(app.exec_())

if __name__ == '__main__':

    start()



from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog
from PyQt5.QtCore import pyqtSlot,QSortFilterProxyModel, Qt
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
from qtgui.savefile import *

class Mainwindow(QMainWindow):

    def __init__(self, parent=None):
        self.dataEntries = []
        self.missingDataEntries = {}
        self.missingDataListing = []
        self.entriesListModel = None
        self.xmlDocument = None

        super(Mainwindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.xmlImporter = XmlImport(self)
        self.saveFile = SaveFile(self)
        #Connect actions to slots
        self.ui.actionOpen_XML_for_analyze.triggered.connect(self.xmlImporter.openXMLFile)
        self.xmlImporter.finishedSignal.connect(self._entriesImportedFromFile)
        self.ui.entriestListView.entrySelectedSignal.connect(self._updateEntryTextFields)
        self.ui.actionSave_changes_to_xml.triggered.connect(self.saveFile.choose_place_to_save_xml)

        #set models.
        self.entriesListModel = EntriesListModel(self.ui.entriestListView, self)
        self.ui.entriestListView.setModel(self.entriesListModel)
        self.ui.entriestListView.show()

        self.ui.entriesComboBox.clear()
        self.ui.entriesComboBox.setCurrentIndex(0)
        self.ui.entriesComboBox.currentIndexChanged.connect(self._changedEntriesComboBox)
        self.ui.nextEntryTextEdit.setEnabled(False)
        self.ui.previousEntryTextEdit.setEnabled(False)
        self.ui.rawTextTextEdit.setEnabled(False)

        #http://doc.qt.digia.com/4.6/itemviews-editabletreemodel.html
        self.treeModel = TreeModel([], self)

        """
        jaska = TreeItem(["JASKA", 33])
        jaska.appendChild(TreeItem(["jakke", 32], jaska))
        jaska.appendChild(TreeItem(["jarkko", 66], jaska))
        toinen = TreeItem(["KAIJA", 123])
        self.treeModel.rootItem.appendChild(toinen)
        toinen.appendChild(TreeItem(["Lissu", 23], toinen))
        toinen.child(0).appendChild(TreeItem(["Liina", 47], toinen.child(0)))"""

        #self.treeModel.setColumnCount(2)
        #self.ui.treeView.setModel(self.treeModel)
        proxyModel = QSortFilterProxyModel(self.ui.treeView)
        proxyModel.setSourceModel(self.treeModel)

        self.ui.treeView.setModel(proxyModel)
        proxyModel.sort(0, Qt.AscendingOrder)
        self.ui.treeView.resizeColumnToContents(0)
        self.ui.treeView.resizeColumnToContents(1)
        self.ui.treeView.expandAll()
        #item = TreeItem(["jaska"], None)
        #self.treeModel.setItem(item)
        #self.treeModel.setItem(TreeItem("jaska2", item))

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
        self.ui.rawTextTextEdit.setEnabled(True)
        self.treeModel.clear()
        self.treeModel.createTreeFromDict(entry["extractionResults"], entry["xml"], self.treeModel.rootItem, True)
        proxyModel = QSortFilterProxyModel(self.ui.treeView)
        proxyModel.setSourceModel(self.treeModel)
        self.ui.treeView.setModel(proxyModel)
        proxyModel.sort(0, Qt.AscendingOrder)
        self.ui.treeView.resizeColumnToContents(0)
        self.ui.treeView.resizeColumnToContents(1)
        self.ui.treeView.expandAll()

        previous = entry["xml"].getprevious()
        if previous is not None:
            self.ui.previousEntryTextEdit.setPlainText(previous.text)
            self.ui.previousEntryTextEdit.setEnabled(True)
        else:
            print("disabled previous")
            self.ui.previousEntryTextEdit.setPlainText("")
            self.ui.previousEntryTextEdit.setEnabled(False)

        next = entry["xml"].getnext()
        if next is not None:
            self.ui.nextEntryTextEdit.setPlainText(next.text)
            self.ui.nextEntryTextEdit.setEnabled(True)
        else:
            self.ui.nextEntryTextEdit.setPlainText("")
            self.ui.nextEntryTextEdit.setEnabled(False)

    @pyqtSlot(dict)
    def _entriesImportedFromFile(self, resultsFromFile):
        self.ui.nextEntryTextEdit.setEnabled(False)
        self.ui.previousEntryTextEdit.setEnabled(False)
        self.ui.rawTextTextEdit.setEnabled(False)

        self.xmlDocument = resultsFromFile["xmlDocument"]
        self.dataEntries = resultsFromFile["entries"]
        self.missingDataEntries = resultsFromFile["errors"]
        self._updateEntriesList(self.dataEntries)
        self._updateEntriesComboBox()
        self.treeModel.clear()
        self.ui.previousEntryTextEdit.setPlainText("")
        self.ui.nextEntryTextEdit.setPlainText("")
        self.ui.rawTextTextEdit.setPlainText("")

def start():
    import sys
    app = QApplication(sys.argv)
    fixingtool = Mainwindow()
    fixingtool.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    start()



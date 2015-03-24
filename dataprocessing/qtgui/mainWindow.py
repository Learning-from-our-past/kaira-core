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
from qtgui.createnewperson import NewPersonDialog

class Mainwindow(QMainWindow):

    def __init__(self, parent=None):
        self.dataEntries = []
        self.missingDataEntries = {}
        self.missingDataListing = []
        self.entriesListModel = None
        self.xmlDocument = None
        self.selectedEntry = None

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
        self.ui.actionCreate_a_new_Person.triggered.connect(self._createNewPerson)

        #set models.
        self.entriesListModel = EntriesListModel(self.ui.entriestListView, self)
        self.ui.entriestListView.entrySelectedSignal.connect(self._entrySelected)
        self.ui.entriestListView.setModel(self.entriesListModel)
        self.ui.entriestListView.show()

        self.ui.entriesComboBox.clear()
        self.ui.entriesComboBox.setCurrentIndex(0)
        self.ui.entriesComboBox.currentIndexChanged.connect(self._changedEntriesComboBox)
        self.ui.nextEntryTextEdit.setEnabled(False)
        self.ui.previousEntryTextEdit.setEnabled(False)
        self.ui.rawTextTextEdit.setEnabled(False)
        self.ui.toolBar.setEnabled(False)
        self.ui.rawTextTextEdit.textChanged.connect(self._editedCurrentTextField)
        self.ui.previousEntryTextEdit.textChanged.connect(self._editedPreviousTextField)
        self.ui.nextEntryTextEdit.textChanged.connect(self._editedNextTextField)

        #http://doc.qt.digia.com/4.6/itemviews-editabletreemodel.html
        self.treeModel = TreeModel([], self)

        proxyModel = QSortFilterProxyModel(self.ui.treeView)
        proxyModel.setSourceModel(self.treeModel)

        self.ui.treeView.setModel(proxyModel)
        proxyModel.sort(0, Qt.AscendingOrder)
        self.ui.treeView.resizeColumnToContents(0)
        self.ui.treeView.resizeColumnToContents(1)
        self.ui.treeView.expandAll()



    def _createNewPerson(self):
        newperson = NewPersonDialog(self.xmlDocument, self.xmlImporter, self )
        selection = newperson.exec_()

        entry = newperson.getPersonEntry()
        if entry is not None and selection == 1:
            self.dataEntries.append(entry)
            self._updateEntriesList(self.dataEntries)
            self._updateEntriesComboBox()


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
        self.ui.rawTextTextEdit.blockSignals(True)
        self.ui.previousEntryTextEdit.blockSignals(True)
        self.ui.nextEntryTextEdit.blockSignals(True)

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

        self.ui.rawTextTextEdit.blockSignals(False)
        self.ui.previousEntryTextEdit.blockSignals(False)
        self.ui.nextEntryTextEdit.blockSignals(False)

    @pyqtSlot(dict)
    def _entriesImportedFromFile(self, resultsFromFile):
        self.ui.nextEntryTextEdit.setEnabled(False)
        self.ui.previousEntryTextEdit.setEnabled(False)
        self.ui.rawTextTextEdit.setEnabled(False)
        self.ui.toolBar.setEnabled(True)
        self.selectedEntry = None

        self.xmlDocument = resultsFromFile["xmlDocument"]
        self.dataEntries = resultsFromFile["entries"]
        self.missingDataEntries = resultsFromFile["errors"]
        self._updateEntriesList(self.dataEntries)
        self._updateEntriesComboBox()
        self.treeModel.clear()
        self.ui.previousEntryTextEdit.setPlainText("")
        self.ui.nextEntryTextEdit.setPlainText("")
        self.ui.rawTextTextEdit.setPlainText("")

    def _entrySelected(self, entry):
        self.selectedEntry = entry

    def _editedCurrentTextField(self):
        if self.selectedEntry is not None:
            self.selectedEntry["xml"].text = self.ui.rawTextTextEdit.toPlainText()

    def _editedPreviousTextField(self):
        if self.selectedEntry is not None:
            previous = self.selectedEntry["xml"].getprevious()
            if previous is not None:
                previous.text = self.ui.previousEntryTextEdit.toPlainText()

    def _editedNextTextField(self):
        if self.selectedEntry is not None:
            next = self.selectedEntry["xml"].getnext()
            if next is not None:
                print(self.ui.nextEntryTextEdit.toPlainText())
                next.text = self.ui.nextEntryTextEdit.toPlainText()



def start():
    import sys
    app = QApplication(sys.argv)
    fixingtool = Mainwindow()
    fixingtool.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    start()



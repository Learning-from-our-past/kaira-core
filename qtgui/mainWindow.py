from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import pyqtSlot,QSortFilterProxyModel, Qt
from PyQt5.QtGui import QIcon
from qtgui.layouts.ui_mainwindow import Ui_MainWindow
from qtgui.services.checkupdates import CheckUpdatesOnStartup
from qtgui.xmlImport import XmlImport
from qtgui.entriesModels import *
from qtgui.entrytree import *
from qtgui.savefile import *
from qtgui.createnewperson import NewPersonDialog
from qtgui.importocrdialog import ImportOcrDialog
from app_information import ABOUT_INFORMATION

class Mainwindow(QMainWindow):

    updateEntriesListSignal = pyqtSignal(name="updatelist")

    def __init__(self, app, parent=None):

        self._app = app
        self.dataEntries = []
        self.missingDataEntries = {}
        self.missingDataListing = []
        self.entriesListModel = None
        self.xmlDocument = None
        self.selectedEntry = None


        super(Mainwindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        icon = QIcon("icon.ico")
        self.setWindowIcon(icon)

        self.setWindowTitle("Kaira " + ABOUT_INFORMATION["version"])

        self.xmlImporter = XmlImport(self)
        self.chunkFile = ImportOcrDialog(self)
        self.saveCsv = SaveCsvFile(self, self.dataEntries)
        self.saveJson = SaveJsonFile(self, self.dataEntries)
        self.saveFile = SaveXmlFile(self, self.dataEntries)
        #Connect actions to slots
        self.ui.actionOpen_XML_for_analyze.triggered.connect(self.xmlImporter.openXMLFile)
        self.ui.actionFrom_txt_OCR.triggered.connect(self.chunkFile.import_txt)
        self.xmlImporter.finishedSignal.connect(self._entriesImportedFromFile)
        self.ui.entriestListView.entrySelectedSignal.connect(self._updateEntryTextFields)
        self.ui.actionSave_changes_to_xml.triggered.connect(self.saveFile.choose_place_to_save_xml)
        self.ui.actionSave.triggered.connect(self.saveFile.save_xml)
        self.ui.actionAbout.triggered.connect(self._about)

        #shortcuts
        self.ui.actionSave.setShortcut('Ctrl+S')
        self.ui.actionOpen_XML_for_analyze.setShortcut('Ctrl+O')
        self.ui.actionCreate_a_new_Person.setShortcut('Ctrl+N')
        self.ui.actionCsv.setShortcut('Ctrl+E')
        self.ui.actionJSON.setShortcut('Ctrl+J')
        self.ui.actionFrom_txt_OCR.setShortcut('Ctrl+I')

        self.ui.actionCreate_a_new_Person.triggered.connect(self._createNewPerson)
        self.updateEntriesListSignal.connect(self._entryModelUpdated)
        self.ui.actionCsv.triggered.connect(self.saveCsv.choose_place_to_save_csv)
        self.ui.actionJSON.triggered.connect(self.saveJson.choose_place_to_save_json)

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

        self.update_checker = CheckUpdatesOnStartup()


    def _createNewPerson(self):
        newperson = NewPersonDialog(self.xmlDocument, self.xmlImporter, self )
        selection = newperson.exec_()

        entry = newperson.getPersonEntry()
        if entry is not None and selection == 1:
            self.dataEntries.append(entry)
            self._updateEntriesList(self.dataEntries)
            self._updateEntriesComboBox()


    def _entryModelUpdated(self):
        self._updateEntriesList(self.dataEntries)
        self._updateEntriesComboBox()
        self.ui.nextEntryTextEdit.setEnabled(False)
        self.ui.previousEntryTextEdit.setEnabled(False)
        self.ui.rawTextTextEdit.setEnabled(False)
        self.ui.toolBar.setEnabled(True)
        self.selectedEntry = None
        self.treeModel.clear()
        self.ui.previousEntryTextEdit.setPlainText("")
        self.ui.nextEntryTextEdit.setPlainText("")
        self.ui.rawTextTextEdit.setPlainText("")

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

    @pyqtSlot(dict, str)
    def _entriesImportedFromFile(self, resultsFromFile, filepath):
        self.xmlDocument = resultsFromFile["xmlDocument"]
        self.saveFile.set_default_filepath(filepath)
        self.dataEntries = resultsFromFile["entries"]
        self.missingDataEntries = resultsFromFile["errors"]
        self._entryModelUpdated()

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
                next.text = self.ui.nextEntryTextEdit.toPlainText()

    @pyqtSlot()
    def _about(self):
        msgbox = QMessageBox()
        msgbox.information(self, "About", "Made by Tuomas Salmi 2015\nhttps://github.com/Tumetsu/Kaira\n" + ABOUT_INFORMATION["version"])
        msgbox.show()

import sys
def start(mongodb):
    app = QApplication(sys.argv)
    fixingtool = Mainwindow(app)
    fixingtool.show()
    exit(app.exec_(), mongodb)

def exit(exitcode, mongodb):
    if mongodb is not None:
        mongodb.kill()  #close the db process
    sys.exit(exitcode)

if __name__ == '__main__':
    start()



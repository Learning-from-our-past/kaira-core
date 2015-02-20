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

class Mainwindow(QMainWindow):

    dataEntries = []
    missingDataListing = {}
    entriesListModel = None

    entrySelectedSignal = pyqtSignal(dict, name="entrySelected")

    def __init__(self, parent=None):
        super(Mainwindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.xmlImporter = XmlImport(self)
        #Connect actions to slots
        self.ui.actionOpen_XML_for_analyze.triggered.connect(self.xmlImporter.openXMLFile)
        self.xmlImporter.finishedSignal.connect(self._entriesImportedFromFile)
        self.entrySelectedSignal.connect(self._updateEntryTextFields)

        #set models.
        self.entriesListModel = EntriesListModel(self.ui.entriestListView, self)
        self.ui.entriestListView.setModel(self.entriesListModel)
        self.ui.entriestListView.show()

        #Comboboxin populointi
        self.ui.entriesComboBox.clear()
        self.ui.entriesComboBox.addItems(["A", "B", "C", "D"])
        self.ui.entriesComboBox.setCurrentIndex(1)


    def _updateEntriesList(self):
        self.entriesListModel.addItems(self.dataEntries)

    def _updateEntriesComboBox(self):
        self.ui.entriesComboBox.clear()
        self.ui.entriesComboBox.addItem("ALL " + str(len(self.dataEntries)))
        for key, value in self.missingDataListing.items():
            print(key)
            self.ui.entriesComboBox.addItem(str(key) + " " + str(len(value)))

    @pyqtSlot(dict)
    def _updateEntryTextFields(self, entry):
        self.ui.rawTextTextEdit.setPlainText(entry["xml"].text)

        previous = entry["xml"].getprevious()
        if previous is not None:
            self.ui.previousEntryTextEdit.setPlainText(previous.text)
        else:
            self.ui.previousEntryTextEdit.setPlainText("")

    @pyqtSlot(dict)
    def _entriesImportedFromFile(self, resultsFromFile):

        self.dataEntries = resultsFromFile["entries"]
        self.missingDataListing = resultsFromFile["errors"]
        self._updateEntriesList()
        self._updateEntriesComboBox()


def start():
    import sys
    app = QApplication(sys.argv)
    fixingtool = Mainwindow()
    fixingtool.show()
    sys.exit(app.exec_())

if __name__ == '__main__':

    start()



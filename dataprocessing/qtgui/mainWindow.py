from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog
from PyQt5.QtCore import pyqtSlot
from qtgui.layouts.ui_mainwindow import Ui_MainWindow
import processData
import threading
import time
import qtgui.utils
from qtgui.models import *
from qtgui.xmlImport import XmlImport

class Mainwindow(QMainWindow):

    xmlDocument = []
    missingDataListing = {}
    entriesListModel = None

    def __init__(self, parent=None):
        super(Mainwindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.xmlImporter = XmlImport(self)
        #Connect actions to slots
        self.ui.actionOpen_XML_for_analyze.triggered.connect(self.xmlImporter.openXMLFile)
        self.xmlImporter.finishedSignal.connect(self._entriesImportedFromFile)

        #set models.
        self.entriesListModel = EntriesListModel(self.ui.entriestListView)
        self.ui.entriestListView.setModel(self.entriesListModel)
        self.ui.entriestListView.show()

        #Comboboxin populointi
        self.ui.entriesComboBox.clear()
        self.ui.entriesComboBox.addItems(["A", "B", "C", "D"])
        self.ui.entriesComboBox.setCurrentIndex(1)


    def _updateEntriesList(self):
        self.ui.entriestListWidget.clear()
        for e in self.xmlDocument:
             self.ui.entriestListWidget.addItem(qtgui.utils.makeSubStrForListViews(e.text) +"...")

    def _updateEntriesComboBox(self):
        self.ui.entriesComboBox.clear()
        self.ui.entriesComboBox.addItem("ALL " + str(len(self.xmlDocument)))
        for key, value in self.missingDataListing.items():
            print(key)
            self.ui.entriesComboBox.addItem(str(key) + " " + str(len(value)))

    @pyqtSlot(dict)
    def _entriesImportedFromFile(self, entries):
        self.xmlDocument = entries["xmlDataDocument"]
        self.missingDataListing = entries["errors"]
        self._updateEntriesList()
        self._updateEntriesComboBox()

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    fixingtool = Mainwindow()
    fixingtool.show()
    sys.exit(app.exec_())

from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog, QProgressDialog
from PyQt5.QtCore import pyqtSlot, QObject
from qtgui.layouts.ui_mainwindow import Ui_MainWindow
import processData
import threading
import time


class XmlImport(QObject):

    parent = None
    processCount = 0
    threadUpdateSignal = pyqtSignal(int, int, name="progressUpdate")

    def __init__(self, parent):
        super(XmlImport, self).__init__(parent)
        self.parent = parent
        self.thread = QThread(parent = self.parent)
        self.threadUpdateSignal.connect(self._updateProgressBarInMainThread)


    @pyqtSlot()
    def openXMLFile(self):
        filename = QFileDialog.getOpenFileName(self.parent, "Open xml-file containing the data to be analyzed.",
                                               "../xmldata", "Person data files (*.xml);;All files (*)")
        print(filename)
        if filename[0] != "":
            self._analyzeOpenedXml(filename)

    def _analyzeOpenedXml(self, file):
        self.progressDialog = QProgressDialog(self.parent)
        self.progressDialog.setCancelButton(None)
        self.progressDialog.setLabelText("Extracting provided datafile...")
        self.progressDialog.open()
        self.progressDialog.setValue(0)
        self.file = file
        self.thread.run = self._runProcess
        self.thread.start()


    def _runProcess(self):
        print("JASKA")
        self.processor = processData.ProcessData(self._processUpdateCallback)
        result = self.processor.startExtractionProcess(self.file[0])

    @pyqtSlot(int, int)
    def _updateProgressBarInMainThread(self, i, max):
        self.progressDialog.setRange(0, max)
        self.progressDialog.setValue(i)

    def _processUpdateCallback(self, i, max):
        self.threadUpdateSignal.emit(i, max)
        #self.thread.emit(self.threadUpdateSignal, i)







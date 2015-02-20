from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog, QProgressDialog, QMessageBox
from PyQt5.QtCore import pyqtSlot, QObject
from qtgui.layouts.ui_mainwindow import Ui_MainWindow
import processData
import threading
import time


class XmlImport(QObject):

    parent = None
    processCount = 0
    threadUpdateSignal = pyqtSignal(int, int, name="progressUpdate")
    threadExceptionSignal = pyqtSignal(name="exceptionInProcess")
    threadResultsSignal = pyqtSignal(dict, name="results")
    finishedSignal = pyqtSignal(dict, name="processFinished")
    result = {}

    def __init__(self, parent):
        super(XmlImport, self).__init__(parent)
        self.parent = parent
        self.thread = QThread(parent = self.parent)
        self.threadUpdateSignal.connect(self._updateProgressBarInMainThread)
        self.threadExceptionSignal.connect(self._loadingFailed)
        self.threadResultsSignal.connect(self._processFinished)

    @pyqtSlot()
    def openXMLFile(self):
        filename = QFileDialog.getOpenFileName(self.parent, "Open xml-file containing the data to be analyzed.",
                                               "../xmldata", "Person data files (*.xml);;All files (*)")
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
        try:
            self.processor = processData.ProcessData(self._processUpdateCallback)
            result = self.processor.startExtractionProcess(self.file[0])
            self.threadResultsSignal.emit(result)
        except Exception as e:
            print(e)
            self.threadExceptionSignal.emit()


    @pyqtSlot(int, int)
    def _updateProgressBarInMainThread(self, i, max):
        self.progressDialog.setRange(0, max)
        self.progressDialog.setValue(i)

    @pyqtSlot()
    def _loadingFailed(self):
        self.progressDialog.cancel()
        msgbox = QMessageBox()
        msgbox.information(self.parent, "Extraction failed", "Error in data-file. Extraction failed. Is the xml valid?")
        msgbox.show()

    @pyqtSlot(dict)
    def _processFinished(self, result):
        self.result = result
        self.finishedSignal.emit(self.result)


    def _processUpdateCallback(self, i, max):
        self.threadUpdateSignal.emit(i, max)







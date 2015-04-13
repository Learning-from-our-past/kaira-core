from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal
import os
from PyQt5.QtWidgets import QFileDialog, QProgressDialog, QMessageBox
from PyQt5.QtCore import pyqtSlot, QObject
from books.soldiers import processData
import route_gui

class XmlImport(QObject):


    threadUpdateSignal = pyqtSignal(int, int, name="progressUpdate")
    threadExceptionSignal = pyqtSignal(object, name="exceptionInProcess")
    threadResultsSignal = pyqtSignal(dict, name="results")
    finishedSignal = pyqtSignal(dict, str, name="processFinished")


    def __init__(self, parent):
        super(XmlImport, self).__init__(parent)
        self.parent = parent
        self.processCount = 0
        self.result = {}
        self.thread = QThread(parent = self.parent)
        self.threadUpdateSignal.connect(self._updateProgressBarInMainThread)
        self.threadExceptionSignal.connect(self._loadingFailed)
        self.threadResultsSignal.connect(self._processFinished)
        self.filepath = ""

    def importOne(self, xmlEntry):
        if self.processor is not None:
            result = self.processor.extractOne(xmlEntry)
            return result
        else:
            return None

    @pyqtSlot()
    def openXMLFile(self):
        filename = QFileDialog.getOpenFileName(self.parent, "Open xml-file containing the data to be analyzed.",
                                               ".", "Person data files (*.xml);;All files (*)")
        if filename[0] != "":
            self.filepath = filename[0]
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
            self.processor = route_gui.Router.get_processdata_class(route_gui.Router.KARELIANS)(self._processUpdateCallback)
            result = self.processor.startExtractionProcess(self.file[0])
            self.threadResultsSignal.emit(result)
        except Exception as e:
            if "DEV" in os.environ and os.environ["DEV"]:
                raise e
            else:
                print(e)
                self.threadExceptionSignal.emit(e)


    @pyqtSlot(int, int)
    def _updateProgressBarInMainThread(self, i, max):
        self.progressDialog.setRange(0, max)
        self.progressDialog.setValue(i)

    @pyqtSlot(object)
    def _loadingFailed(self, e):
        self.progressDialog.cancel()
        msgbox = QMessageBox()
        msgbox.information(self.parent, "Extraction failed", "Error in data-file. Extraction failed. Is the xml valid and in utf-8 format? More info: " + str(e))
        msgbox.show()

    @pyqtSlot(dict)
    def _processFinished(self, result):
        self.result = result
        self.finishedSignal.emit(self.result, self.filepath)


    def _processUpdateCallback(self, i, max):
        self.threadUpdateSignal.emit(i, max)






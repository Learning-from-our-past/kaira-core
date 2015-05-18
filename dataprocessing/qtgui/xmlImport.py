from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal
import os
from PyQt5.QtWidgets import QFileDialog, QProgressDialog, QMessageBox
from PyQt5.QtCore import pyqtSlot, QObject
from books.soldiers import processData
import route_gui
from lxml import etree
import multiprocessing
import math


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
            xmlDataDocument = self._getXMLroot(self.file[0])
            #TODO: Lue xml:n metadata
            try:
                #TODO: Moniprosarituki?
                self.processor = route_gui.Router.get_processdata_class(xmlDataDocument.attrib["bookseries"])(self._processUpdateCallback)
                result = self.processor.startExtractionProcess(xmlDataDocument, self.file[0])
                self.threadResultsSignal.emit(result)
            except KeyError:
                raise MetadataException()
        except Exception as e:
            if "DEV" in os.environ and os.environ["DEV"]:
                raise e
            else:
                print(e)
                self.threadExceptionSignal.emit(e)

    #Experimental, not working
    """
    def _extractMultiprocessing(self):
        processors = multiprocessing.cpu_count()
        xmlDataDocument = self._getXMLroot(self.file[0])
        chunks = list(self._partitionXml(xmlDataDocument, processors))
        resultList = list() #lista tuloslistoista:
        for x in range(0, processors):
            resultList.append(list())

        #luo prosessit jokaiselle palaselle:
        id = 0
        jobs = []
        progress_queue = multiprocessing.Queue()
        for part in chunks:
            q = multiprocessing.Queue()             #luo prosessille jono johon palauttaa tulokset
            p = Worker(id, part, q, progress_queue)  #varsinainen prosessi
            jobs.append((p, q))
            p.start()
            id += 1;

         #odota kunnes prosessit ovat valmiita:
        for val in jobs:
            val[0].join()                       #odottaja
            result = val[1].get()
            print(result)
        print("prossut päällä")



    def _partitionXml(self, l, chunks):

        n = int(math.ceil(len(l) / chunks))
        for i in range(0, len(l), n):
            yield l[i:i+n]

    """

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


    def _getXMLroot(self, filepath):

        #read the data in XML-format to be processed
        tree = etree.parse(filepath) #ET.parse(filepath)


        return tree.getroot()


class MetadataException(Exception):

    def __init__(self):
        self.msg = "ERROR: The document doesn't contain bookseries attribute in the beginning of the file. Couldn't import. Try " \
                   "to generate new xml-file from the source ocr-text or add the missing attribute to the file manually."
    def __str__(self):
        return repr(self.msg)


class Worker(multiprocessing.Process):

    def __init__(self, threadID, xmlDocument, resultqueue, updatequeue):
        super(Worker, self).__init__()  #muuta
        self.threadID = threadID
        self.xmlDocument = xmlDocument
        self.resultqueue = resultqueue              #jono johon tulokset lopuksi palautetaan
        self.updatequeue = updatequeue

    def _processUpdateCallback(self):
        self.updatequeue.put(1)

    def run(self):
        self.processor = route_gui.Router.get_processdata_class(self.xmlDocument.attrib["bookseries"])(self._processUpdateCallback)
        result = self.processor.startExtractionProcess(self.xmlDocument, self.file[0])
        self.resultqueue.put(result)
        return

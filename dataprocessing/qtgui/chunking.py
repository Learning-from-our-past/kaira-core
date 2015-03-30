from PyQt5.QtCore import pyqtSlot, pyqtSignal, QDate, QDateTime, QDir, QObject
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog, QInputDialog, QMessageBox, QCompleter
from PyQt5.QtCore import pyqtSlot, QEvent, QSettings, QStandardPaths
from lxml import etree
from PyQt5.QtGui import QStatusTipEvent, QDesktopServices
import chunktextfile

class ChunkFile(QObject):

    def __init__(self, parent):
        super(ChunkFile, self).__init__(parent)
        self.parent = parent

    def import_txt(self):
        try:
            self._open_text_file()
        except Exception as e:
            msgbox = QMessageBox()
            msgbox.information(self.parent, "Chunking process failed", "Error in data-file. Was it saved in utf-8/unicode format? More info: " + str(e))
            msgbox.show()

    def choose_place_to_save_xml(self, chunked_text):
            paths = QStandardPaths.standardLocations(0)
            if len(paths) > 0:
                path = paths[0]
            else:
                path = ""
            filename = QFileDialog.getSaveFileName(self.parent, "Save xml-data containing the chunked data:",
                                                   path +"/data_from_ocr.xml", "XML-files (*.xml);;All files (*)")
            if filename[0] != "":
                self._save_to_xml(chunked_text, filename[0])


    def _open_text_file(self):
        print("open")
        filename = QFileDialog.getOpenFileName(self.parent, "Open text-file containing the data to be chunked.",
                                               ".", "Person data text files (*.txt);;All files (*)")
        if filename[0] != "":
            chunked_text = self._chunk_text_file(filename)
            self.choose_place_to_save_xml(chunked_text)

    def _chunk_text_file(self, filename):
        f = open(filename[0], "r", encoding="utf8")
        text = f.read()
        return chunktextfile.chunkTextFile(text)

    def _save_to_xml(self, chunkedtext, path):
        print ("Kirjoitetaan ")
        f = open(path, 'w', encoding="utf8")
        f.write(chunkedtext)
        f.close()


    def _remove_empty_elements(self, xmldocument):
        for child in xmldocument:
            if child.text.strip() == "":
                xmldocument.remove(child)
                for i in range(0, len(self.dataEntries)):
                    print(self.dataEntries[i]["xml"])
                    if self.dataEntries[i]["xml"] == child:
                        self.dataEntries.pop(i)
                        break
        self.parent.updateEntriesListSignal.emit()

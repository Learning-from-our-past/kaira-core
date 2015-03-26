from PyQt5.QtCore import pyqtSlot, pyqtSignal, QDate, QDateTime, QDir, QObject
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog, QInputDialog, QMessageBox, QCompleter
from PyQt5.QtCore import pyqtSlot, QEvent, QSettings, QStandardPaths
from lxml import etree
from PyQt5.QtGui import QStatusTipEvent, QDesktopServices


class SaveFile(QObject):

    def __init__(self, parent, dataEntries):
        super(SaveFile, self).__init__(parent)
        self.parent = parent
        self.dataEntries = dataEntries


    def choose_place_to_save_xml(self):
            paths = QStandardPaths.standardLocations(0)
            if len(paths) > 0:
                path = paths[0]
            else:
                path = ""
            filename = QFileDialog.getSaveFileName(self.parent, "Save xml-data containing the original data:",
                                                   path +"/originaldata.xml", "XML-files (*.xml);;All files (*)")
            if filename[0] != "":
                self._save_to_xml(self.parent.xmlDocument, filename[0])

    def _save_to_xml(self, xmldata, path):
        #write modifications to a new xml-file:
        self.dataEntries = self.parent.dataEntries
        self._remove_empty_elements(xmldata)
        print ("Kirjoitetaan ")
        f = open(path, 'wb')
        f.write(etree.tostring(xmldata, pretty_print=True, encoding='unicode').encode("utf8"))
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


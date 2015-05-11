from lxml import etree
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QStandardPaths
import route_gui
import os

class SaveXmlFile(QObject):

    def __init__(self, parent, dataEntries):
        super(SaveXmlFile, self).__init__(parent)
        self.parent = parent
        self.dataEntries = dataEntries
        self.path = ""

    def set_default_filepath(self, path):
        self.path = path

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

    def save_xml(self):
        #Ask path if it is not defined yet:
        if self.path == "":
            self.choose_place_to_save_xml()
        else:
            self._save_to_xml(self.parent.xmlDocument, self.path)


    def _save_to_xml(self, xmldata, path):
        #write modifications to a new xml-file:
        self.dataEntries = self.parent.dataEntries
        self._remove_empty_elements(xmldata)
        print ("Kirjoitetaan ")
        f = open(path, 'wb')
        f.write(etree.tostring(xmldata, pretty_print=True, encoding='unicode').encode("utf8"))
        f.close()


    def _remove_empty_elements(self, xmldocument):
        removed = False
        for child in xmldocument:
            if child.text.strip() == "":
                xmldocument.remove(child)
                for i in range(0, len(self.dataEntries)):
                    print(self.dataEntries[i]["xml"])
                    if self.dataEntries[i]["xml"] == child:
                        removed = True
                        self.dataEntries.pop(i)
                        break
        if removed:
            self.parent.updateEntriesListSignal.emit()


class SaveCsvFile(QObject):

    def __init__(self, parent, dataEntries):
        super(SaveCsvFile, self).__init__(parent)
        self.parent = parent
        self.dataEntries = dataEntries


    def choose_place_to_save_csv(self):
            paths = QStandardPaths.standardLocations(0)
            if len(paths) > 0:
                path = paths[0]
            else:
                path = ""
            filename = QFileDialog.getSaveFileName(self.parent, "Save csv-data containing the extracted data:",
                                                   path +"/extraction_results.csv", "CSV-files (*.csv);;All files (*)")
            if filename[0] != "":
                self._save_to_csv(self.parent.dataEntries, filename[0])

    def _save_to_csv(self, entries, path):
        #write modifications to a new xml-file:
        writer = route_gui.Router.get_csvbuilder_class(self.parent.xmlDocument.attrib["bookseries"])()
        writer.openCsv(path)
        for entry in self.parent.dataEntries:
            try:
                writer.writeRow(entry["extractionResults"])
            except KeyError as e:
                if "DEV" in os.environ and os.environ["DEV"]:
                    raise e

        writer.closeCsv()

class SaveJsonFile(QObject):

    def __init__(self, parent, dataEntries):
        super(SaveJsonFile, self).__init__(parent)
        self.parent = parent
        self.dataEntries = dataEntries


    def choose_place_to_save_json(self):
            paths = QStandardPaths.standardLocations(0)
            if len(paths) > 0:
                path = paths[0]
            else:
                path = ""
            filename = QFileDialog.getSaveFileName(self.parent, "Save json-data containing the extracted data:",
                                                   path +"/extraction_results.json", "JSON-files (*.json);;All files (*)")
            if filename[0] != "":
                self._save_to_json(self.parent.dataEntries, filename[0])

    def _save_to_json(self, entries, path):
        #write modifications to a new xml-file:
        print("tallenna json")
        writer = route_gui.Router.get_jsonbuilder_class(self.parent.xmlDocument.attrib["bookseries"])()
        writer.openJson(path)
        for entry in self.parent.dataEntries:
            try:
                writer.writeEntry(entry["extractionResults"])
            except KeyError as e:
                if "DEV" in os.environ and os.environ["DEV"]:
                    raise e

        writer.closeJson()


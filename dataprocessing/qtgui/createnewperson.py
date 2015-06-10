from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QDialog, QProgressDialog, QMessageBox
from PyQt5.QtCore import pyqtSlot, QObject
from qtgui.layouts.ui_newpersondialog import Ui_CreateNewPersonDialog
from lxml import etree

class NewPersonDialog(QDialog):

    def __init__(self, xmlDocument, xmlImporter, parent = None):
        super(NewPersonDialog, self).__init__(parent)
        self.ui = Ui_CreateNewPersonDialog()
        self.ui.setupUi(self)
        self.xmlDocument = xmlDocument
        self.xmlImporter = xmlImporter
        self.newPersonText = ""
        self.newPersonName = ""
        self.ui.plainTextEdit.textChanged.connect(self._textChanged)
        self.ui.nameField.textChanged.connect(self._nameChanged)

    def setupUi(self):
        pass

    def _textChanged(self):
        self.newPersonText = self.ui.plainTextEdit.toPlainText()

    def _nameChanged(self):
        self.newPersonName = self.ui.nameField.text()

    def getPersonEntry(self):
        if self.newPersonText.strip() != "":
            child = etree.SubElement(self.xmlDocument, "PERSON")
            child.text = self.newPersonText
            child.attrib["name"] = self.newPersonName
            child.attrib["createdFromEditor"] = "True"
            return self.xmlImporter.importOne(child)
        else:
            return None




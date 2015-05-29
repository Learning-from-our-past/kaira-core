from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox, QDialogButtonBox, QRadioButton
from PyQt5.QtCore import QStandardPaths
from books.soldiers.chunktextfile import ChunkTextFile
from qtgui.layouts.ui_importdialog import Ui_ImportDialog
import route_gui
import os

class ImportOcrDialog(QDialog):

    def __init__(self, parent):
        super(ImportOcrDialog, self).__init__(parent)
        self.parent = parent
        self.ui = Ui_ImportDialog()
        self.ui.setupUi(self)
        self.radiobuttons = []
        self._create_radiobuttons()
        self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        self.ui.sourceButton.clicked.connect(self._browse_sourcefile)
        self.ui.destinationButton.clicked.connect(self._browse_destinationfile)


    def _create_radiobuttons(self):
        series = route_gui.Router.get_bookseries_list()
        for item in series:
            r = QRadioButton(self)
            r.setText(item)
            self.radiobuttons.append(r)
            self.ui.groupBox.layout().addWidget(r)
        self.radiobuttons[0].setChecked(True)

    def _browse_sourcefile(self):
        filename = QFileDialog.getOpenFileName(self.parent, "Open text-file containing the data to be chunked.",
                                               ".", "Person data text files (*.txt *.htm *.html);;All files (*)")
        if filename[0] != "":
            self.source_file = filename[0]
            self.ui.sourcepathLabel.setText(self.source_file[-20:])
            self._activate_ok()
        else:
            self.source_file = ""
            self.ui.sourcepathLabel.setText("<not selected>")
            self._activate_ok()

    def _browse_destinationfile(self):
        paths = QStandardPaths.standardLocations(0)
        if len(paths) > 0:
            path = paths[0]
        else:
            path = ""
        filename = QFileDialog.getSaveFileName(self.parent, "Save xml-data containing the chunked data:",
                                               path +"/data_from_ocr.xml", "XML-files (*.xml);;All files (*)")
        if filename[0] != "":
            self.destination_file = filename[0]
            self.ui.destinationpathLabel.setText(self.destination_file[-20:])
            self._activate_ok()
        else:
            self.destination_file = ""
            self.ui.destinationpathLabel.setText("<not selected>")
            self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
            self._activate_ok()

    def _activate_ok(self):
        if self.destination_file != "" and self.source_file != "":
            self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
        else:
            self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

    def import_txt(self):
        self.source_file = ""
        self.destination_file = ""
        self.ui.sourcepathLabel.setText("<not selected>")
        self.ui.destinationpathLabel.setText("<not selected>")
        self._activate_ok()

        if self.exec_():
            try:
                chunked_text = self._chunk_text_file(self.source_file)
                self._save_to_xml(chunked_text, self.destination_file)
                msgbox = QMessageBox()
                msgbox.information(self.parent, "Done", "OCR conversion done! File saved to the disk.")
                msgbox.show()
            except Exception as e:
                if "DEV" in os.environ and os.environ["DEV"]:
                    raise e
                else:
                    msgbox = QMessageBox()
                    msgbox.information(self.parent, "Chunking process failed", "Error in data-file. Was it saved in utf-8/unicode format? More info: " + str(e))
                    msgbox.show()

    def _chunk_text_file(self, filename):
        working_dir = os.getcwd()
        os.chdir(os.path.dirname(filename))
        f = open(filename, "r", encoding="utf8")
        text = f.read()
        os.chdir(working_dir)

        for radio in self.radiobuttons:
            if radio.isChecked():
                chunker = route_gui.Router.get_chunktext_class(radio.text())()
                break

        return chunker.chunk_text(text, self.destination_file)



    def _save_to_xml(self, chunkedtext, path):
        print ("Kirjoitetaan ")
        f = open(path, 'w', encoding="utf8")
        f.write(chunkedtext)
        f.close()




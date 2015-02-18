from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QAbstractListModel, QVariant, QModelIndex
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog
from PyQt5.QtCore import pyqtSlot



class EntriesListModel(QAbstractListModel):
    #http://pyqt.sourceforge.net/Docs/PyQt4/qabstractlistmodel.html

    def __init__(self, parent):
        super(EntriesListModel, self).__init__(parent)
        self.listdata = [1, 2, 3, 4]

    def rowCount(self, parent=QModelIndex()):
        return len(self.listdata)

    def data(self, index, role):
        #Returns the data stored under the given role for the item referred to by the index.
        print("adsf")
        if index.isValid():
            print(self.listdata[index.row()])
            return QVariant(self.listdata[index.row()])
        else:
            return QVariant()
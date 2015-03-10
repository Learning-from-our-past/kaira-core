from PyQt5.QtGui import  QStandardItem, QStandardItemModel
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog, QListView, QTreeView

#http://doc.qt.digia.com/4.6/itemviews-editabletreemodel.html

class EntryTreeView(QTreeView):
    pass

class TreeModel(QStandardItemModel):
    pass

class TreeItem():

    _parent = None
    _children = []
    _itemData = []
    def __init__(self, data, parent):
        self._parent = parent
        self._itemData = data
        #super(TreeItem, self).__init__(data)

    def child(self, number):
        return self._children[number]

    def childCount(self):
        return len(self._children)

    def columnCount(self):
        return len(self._itemData)

    def insertChildren(self, position, data):
        if position < 0 or position > len(self._itemData):
            return False

        t = TreeItem(data, self)
        self._children.append(t)
        return True


    def insertColumns(self, position, columns):
        pass

    def removeChildren(self, position, columns):
        pass

    def childNumber(self):
        if self._parent is not None:
            return self._parent.childItems.indexOf(self)
        return None

    def setData(self, column, value):
        pass

    def parent(self):
        return self._parent

    def data(self, column):
        return self._itemData[column]

    def setData(self, column, value):
        if column < 0 or column > len(self._itemData):
            return False

        self._itemData[column] = value
        return True



from PyQt5 import QtCore

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QTreeView
from interface.valuewrapper import ValueWrapper

#http://doc.qt.digia.com/4.6/itemviews-editabletreemodel.html

class EntryTreeView(QTreeView):
    pass

class TreeModel(QtCore.QAbstractItemModel):
    def __init__(self, data, parent=None):
        super(TreeModel, self).__init__(parent)
        self.parents=[]
        self.dbdata = data
        self.rootItem = TreeItem([["Attributes"], ["Values"]], None)
        self.setupModelData(self.dbdata, self.rootItem)

    def clear(self):
        self.rootItem.removeChildren()
        self.layoutChanged.emit()


    def setData(self, index, value, role):

        if index.isValid() and role == QtCore.Qt.EditRole:
            prev_value = self.getValue(index, role)
            print(prev_value)
            item = index.internalPointer()
            item.setData(value, index.column())
            return True
        else:
           return False

    def removeRows(self, position=0, count=1,  parent=QtCore.QModelIndex()):

       node = self.nodeFromIndex(parent)
       self.beginRemoveRows(parent, position, position + count - 1)
       node.childItems.pop(position)
       self.endRemoveRows()

    def nodeFromIndex(self, index):
       if index.isValid():
           return index.internalPointer()
       else:
           return self.rootItem

    def getValue(self, index, role):
       item = index.internalPointer()
       return item.data(index.column(), role)

    def columnCount(self, parent):
       if parent.isValid():
           return parent.internalPointer().columnCount()
       else:
           return self.rootItem.columnCount()

    def data(self, index, role):
        if not index.isValid():
            return None
        if role == QtCore.Qt.EditRole:
            item = index.internalPointer()
            return QtCore.QVariant(item.data(index.column(), role))

        if role != QtCore.Qt.DisplayRole and role != QtCore.Qt.BackgroundRole:
            return None

        item = index.internalPointer()
        return QtCore.QVariant(item.data(index.column(), role))

    def flags(self, index):
        if not index.isValid():
           return QtCore.Qt.NoItemFlags

        if index.column() == 0 or not self.nodeFromIndex(index).isEditable():
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        else:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable


    def headerData(self, section, orientation, role):
       if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
           return QtCore.QVariant(self.rootItem.data(section, role)[0])

       return None

    def index(self, row, column, parent):

       if row < 0 or column < 0 or row >= self.rowCount(parent) or column >= self.columnCount(parent):
           return QtCore.QModelIndex()

       if not parent.isValid():
           parentItem = self.rootItem
       else:
           parentItem = parent.internalPointer()

       childItem = parentItem.child(row)
       if childItem:
           return self.createIndex(row, column, childItem)
       else:
           return QtCore.QModelIndex()

    def parent(self, index):
       if not index.isValid():
           return QtCore.QModelIndex()

       childItem = index.internalPointer()
       parentItem = childItem.parent()

       if parentItem == self.rootItem or parentItem is None:
           return QtCore.QModelIndex()

       return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent):
       if parent.column() > 0:
           return 0

       if not parent.isValid():
           parentItem = self.rootItem
       else:
           parentItem = parent.internalPointer()

       return parentItem.childCount()

    def setupModelData(self, lines, parent):
       ind = []
       self.parents.append(parent)
       ind.append(0)
       col_numb=parent.columnCount()
       numb = 0

       for line in lines:
           numb+=1
           lineData=line[0]
           self.parents[-1].appendChild(TreeItem(lineData, self.parents[-1]))

           columnData = line[1]

           self.parents.append(self.parents[-1].child(self.parents[-1].childCount() - 1))

           for j in columnData:
                self.parents[-1].appendChild(TreeItem(j, self.parents[-1]))
           if len(self.parents) > 0:
                self.parents.pop()


    def createTreeFromDict(self, data, xml, parent, top=False):
        if top:
            print(data)
            data = ValueWrapper(data)

        if isinstance(data.value, dict):
            for key, value in data.value.items():

                if key == "cursorLocation" or isinstance(value, str):
                    continue


                if isinstance(value.value, dict):
                    node = TreeItem([key, ""],xml, parent)
                    parent.appendChild(node)
                    node.setNotEditable()
                    self.createTreeFromDict(value, xml, node)

                elif isinstance(value.value, list):
                    node = TreeItem([key, ""],xml, parent)
                    parent.appendChild(node)
                    node.setNotEditable()
                    self.createTreeFromDict(value, xml, node)

                elif isinstance(value.value, ValueWrapper):
                    node = TreeItem([key, value.value],xml, parent)
                    parent.appendChild(node)
                else:
                    #print("tiedot " + str(key) + " " + str(value.value))
                    node = TreeItem([key, value],xml, parent)
                    parent.appendChild(node)

        if isinstance(data.value, list):
            for index, value in enumerate(data.value):
                if isinstance(value.value, dict):
                    node = TreeItem([index+1, ""],xml, parent)
                    parent.appendChild(node)
                    node.setNotEditable()
                    self.createTreeFromDict(value,xml, node)

                elif isinstance(value.value, list):
                    node = TreeItem([index+1, ""],xml, parent)
                    parent.appendChild(node)
                    node.setNotEditable()
                    self.createTreeFromDict(value,xml, node)

                else:
                    node = TreeItem(["juttu", value],xml, parent)
                    parent.appendChild(node)

        if top:
            self.layoutChanged.emit()



class TreeItem(object):

      EDITED_ROW_COLOR = QColor(111,199,70)
      ERROR_ROW_COLOR = QColor(218,85,85)
      MISSING_ROW_COLOR = QColor(247, 252, 117)
      def __init__(self, data, xml, parent=None):
          self.parentItem = parent
          self.itemData = data
          self.childItems = []
          self.xml = xml
          self.editable = True
          print(data)

      def setNotEditable(self):
          self.editable = False

      def isEditable(self):
          return self.editable

      def appendChild(self, item):
          self.childItems.append(item)

      def child(self, row):
          return self.childItems[row]

      def childCount(self):
          return len(self.childItems)

      def columnCount(self):
          return len(self.itemData)


      def data(self, column, role):

          try:
              if isinstance(self.itemData[column], ValueWrapper):
                  #color the row differently if it has manually edited data
                  if role == QtCore.Qt.BackgroundRole and self.itemData[column].error != False and not self.itemData[column].manuallyEdited:
                      return QtCore.QVariant(self.ERROR_ROW_COLOR)

                  if role == QtCore.Qt.BackgroundRole and self.itemData[column].manuallyEdited:
                      return QtCore.QVariant(self.EDITED_ROW_COLOR)

                  if role == QtCore.Qt.BackgroundRole and (self.itemData[column].value == "" or self.itemData[column].value is None):
                      return QtCore.QVariant(self.MISSING_ROW_COLOR)

                  return self.itemData[column].value

              else:
                    return self.itemData[column]

          except IndexError:
              return None

      def parent(self):
          return self.parentItem

      def row(self):
          if self.parentItem:
              return self.parentItem.childItems.index(self)
          return 0

      def setData(self, data, column):
          print(self.itemData[column].id)
          self.xml.attrib[self.itemData[column].id] = str(data)  #save manual data to an attribute to the xml entry
          self.itemData[column].manualEdit(data)


      def removeChildren(self):
          self.childItems = []
          return True

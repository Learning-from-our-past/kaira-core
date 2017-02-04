# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'newpersondialog.ui'
#
# Created by: PyQt5 UI code generator 5.4.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_CreateNewPersonDialog(object):
    def setupUi(self, CreateNewPersonDialog):
        CreateNewPersonDialog.setObjectName("CreateNewPersonDialog")
        CreateNewPersonDialog.resize(400, 382)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(CreateNewPersonDialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(CreateNewPersonDialog)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.nameField = QtWidgets.QLineEdit(CreateNewPersonDialog)
        self.nameField.setObjectName("nameField")
        self.verticalLayout.addWidget(self.nameField)
        self.label = QtWidgets.QLabel(CreateNewPersonDialog)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.plainTextEdit = QtWidgets.QPlainTextEdit(CreateNewPersonDialog)
        self.plainTextEdit.setBackgroundVisible(False)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.verticalLayout.addWidget(self.plainTextEdit)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(CreateNewPersonDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(CreateNewPersonDialog)
        self.buttonBox.accepted.connect(CreateNewPersonDialog.accept)
        self.buttonBox.rejected.connect(CreateNewPersonDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(CreateNewPersonDialog)

    def retranslateUi(self, CreateNewPersonDialog):
        _translate = QtCore.QCoreApplication.translate
        CreateNewPersonDialog.setWindowTitle(_translate("CreateNewPersonDialog", "Create new person entry"))
        self.label_2.setText(_translate("CreateNewPersonDialog", "Name:"))
        self.nameField.setPlaceholderText(_translate("CreateNewPersonDialog", "Person\'s name here. Not required for soldiers."))
        self.label.setText(_translate("CreateNewPersonDialog", "Person data:"))
        self.plainTextEdit.setPlaceholderText(_translate("CreateNewPersonDialog", "New person\'s text here"))


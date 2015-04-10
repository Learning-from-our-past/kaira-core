# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'importdialog.ui'
#
# Created: Fri Apr 10 12:56:59 2015
#      by: PyQt5 UI code generator 5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ImportDialog(object):
    def setupUi(self, ImportDialog):
        ImportDialog.setObjectName("ImportDialog")
        ImportDialog.resize(400, 215)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(ImportDialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(ImportDialog)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.sourceLabel = QtWidgets.QLabel(ImportDialog)
        self.sourceLabel.setObjectName("sourceLabel")
        self.horizontalLayout.addWidget(self.sourceLabel)
        self.sourcepathLabel = QtWidgets.QLabel(ImportDialog)
        self.sourcepathLabel.setObjectName("sourcepathLabel")
        self.horizontalLayout.addWidget(self.sourcepathLabel)
        self.sourceButton = QtWidgets.QPushButton(ImportDialog)
        self.sourceButton.setObjectName("sourceButton")
        self.horizontalLayout.addWidget(self.sourceButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.destinationLabel = QtWidgets.QLabel(ImportDialog)
        self.destinationLabel.setObjectName("destinationLabel")
        self.horizontalLayout_2.addWidget(self.destinationLabel)
        self.destinationpathLabel = QtWidgets.QLabel(ImportDialog)
        self.destinationpathLabel.setObjectName("destinationpathLabel")
        self.horizontalLayout_2.addWidget(self.destinationpathLabel)
        self.destinationButton = QtWidgets.QPushButton(ImportDialog)
        self.destinationButton.setObjectName("destinationButton")
        self.horizontalLayout_2.addWidget(self.destinationButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.groupBox = QtWidgets.QGroupBox(ImportDialog)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.soldierRadio = QtWidgets.QRadioButton(self.groupBox)
        self.soldierRadio.setObjectName("soldierRadio")
        self.verticalLayout_3.addWidget(self.soldierRadio)
        self.karelianRadio = QtWidgets.QRadioButton(self.groupBox)
        self.karelianRadio.setChecked(True)
        self.karelianRadio.setObjectName("karelianRadio")
        self.verticalLayout_3.addWidget(self.karelianRadio)
        self.verticalLayout_2.addWidget(self.groupBox)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.buttonBox = QtWidgets.QDialogButtonBox(ImportDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(ImportDialog)
        self.buttonBox.accepted.connect(ImportDialog.accept)
        self.buttonBox.rejected.connect(ImportDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ImportDialog)

    def retranslateUi(self, ImportDialog):
        _translate = QtCore.QCoreApplication.translate
        ImportDialog.setWindowTitle(_translate("ImportDialog", "Import OCR-data"))
        self.label.setText(_translate("ImportDialog", "Please select the file containing OCR-data and location to save the results."))
        self.sourceLabel.setText(_translate("ImportDialog", "Source file to import from:"))
        self.sourcepathLabel.setText(_translate("ImportDialog", "<not selected>"))
        self.sourceButton.setText(_translate("ImportDialog", "Browse"))
        self.destinationLabel.setText(_translate("ImportDialog", "Destination file to save to:"))
        self.destinationpathLabel.setText(_translate("ImportDialog", "<not selected>"))
        self.destinationButton.setText(_translate("ImportDialog", "Browse"))
        self.groupBox.setTitle(_translate("ImportDialog", "Book series:"))
        self.soldierRadio.setText(_translate("ImportDialog", "Suomen Rintamamiehet 1939-43"))
        self.karelianRadio.setText(_translate("ImportDialog", "Siirtokarjalaisten tie"))


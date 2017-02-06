# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'updatedialog.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_CheckUpdatesDialog(object):
    def setupUi(self, CheckUpdatesDialog):
        CheckUpdatesDialog.setObjectName("CheckUpdatesDialog")
        CheckUpdatesDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        CheckUpdatesDialog.resize(251, 81)
        CheckUpdatesDialog.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(CheckUpdatesDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.newVersion_label = QtWidgets.QLabel(CheckUpdatesDialog)
        self.newVersion_label.setObjectName("newVersion_label")
        self.verticalLayout.addWidget(self.newVersion_label)
        self.currentVersion_label = QtWidgets.QLabel(CheckUpdatesDialog)
        self.currentVersion_label.setObjectName("currentVersion_label")
        self.verticalLayout.addWidget(self.currentVersion_label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.goToDownloads_Button = QtWidgets.QPushButton(CheckUpdatesDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.goToDownloads_Button.sizePolicy().hasHeightForWidth())
        self.goToDownloads_Button.setSizePolicy(sizePolicy)
        self.goToDownloads_Button.setObjectName("goToDownloads_Button")
        self.horizontalLayout.addWidget(self.goToDownloads_Button)
        self.closeButton = QtWidgets.QPushButton(CheckUpdatesDialog)
        self.closeButton.setObjectName("closeButton")
        self.horizontalLayout.addWidget(self.closeButton)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(CheckUpdatesDialog)
        self.closeButton.clicked.connect(CheckUpdatesDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(CheckUpdatesDialog)

    def retranslateUi(self, CheckUpdatesDialog):
        _translate = QtCore.QCoreApplication.translate
        CheckUpdatesDialog.setWindowTitle(_translate("CheckUpdatesDialog", "Updates"))
        self.newVersion_label.setText(_translate("CheckUpdatesDialog", "Available Kaira version: "))
        self.currentVersion_label.setText(_translate("CheckUpdatesDialog", "Your current version is: "))
        self.goToDownloads_Button.setText(_translate("CheckUpdatesDialog", "Go to downloads"))
        self.closeButton.setText(_translate("CheckUpdatesDialog", "Close"))


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Mon Mar  2 18:07:15 2015
#      by: PyQt5 UI code generator 5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1524, 712)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.entriesFrame = QtWidgets.QFrame(self.centralwidget)
        self.entriesFrame.setFrameShape(QtWidgets.QFrame.Panel)
        self.entriesFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.entriesFrame.setObjectName("entriesFrame")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.entriesFrame)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.entriesControlLayout = QtWidgets.QFormLayout()
        self.entriesControlLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.entriesControlLayout.setObjectName("entriesControlLayout")
        self.entriesLabel = QtWidgets.QLabel(self.entriesFrame)
        self.entriesLabel.setObjectName("entriesLabel")
        self.entriesControlLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.entriesLabel)
        self.entriesComboBox = QtWidgets.QComboBox(self.entriesFrame)
        self.entriesComboBox.setMaxVisibleItems(20)
        self.entriesComboBox.setObjectName("entriesComboBox")
        self.entriesComboBox.addItem("")
        self.entriesControlLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.entriesComboBox)
        self.verticalLayout_4.addLayout(self.entriesControlLayout)
        self.entriestListView = EntriesListView(self.entriesFrame)
        self.entriestListView.setStyleSheet("QListWidget {\n"
"alternate-background-color: #EDEDED;\n"
"background-color: white;\n"
"}")
        self.entriestListView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.entriestListView.setAlternatingRowColors(True)
        self.entriestListView.setObjectName("entriestListView")
        self.verticalLayout_4.addWidget(self.entriestListView)
        self.gridLayout.addWidget(self.entriesFrame, 0, 0, 1, 1)
        self.attributesFrame = QtWidgets.QFrame(self.centralwidget)
        self.attributesFrame.setFrameShape(QtWidgets.QFrame.Panel)
        self.attributesFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.attributesFrame.setObjectName("attributesFrame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.attributesFrame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.attributesControlsLayout = QtWidgets.QHBoxLayout()
        self.attributesControlsLayout.setObjectName("attributesControlsLayout")
        self.attributesLabel = QtWidgets.QLabel(self.attributesFrame)
        self.attributesLabel.setObjectName("attributesLabel")
        self.attributesControlsLayout.addWidget(self.attributesLabel)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.attributesControlsLayout.addItem(spacerItem)
        self.toolButton = QtWidgets.QToolButton(self.attributesFrame)
        self.toolButton.setStyleSheet("")
        self.toolButton.setObjectName("toolButton")
        self.attributesControlsLayout.addWidget(self.toolButton)
        self.verticalLayout.addLayout(self.attributesControlsLayout)
        self.tableView = EntryTableView(self.attributesFrame)
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setSortingEnabled(True)
        self.tableView.setObjectName("tableView")
        self.tableView.horizontalHeader().setCascadingSectionResizes(False)
        self.tableView.horizontalHeader().setStretchLastSection(False)
        self.verticalLayout.addWidget(self.tableView)
        self.gridLayout.addWidget(self.attributesFrame, 1, 0, 1, 1)
        self.currentFrame = QtWidgets.QFrame(self.centralwidget)
        self.currentFrame.setFrameShape(QtWidgets.QFrame.Panel)
        self.currentFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.currentFrame.setObjectName("currentFrame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.currentFrame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.rawTextLabel = QtWidgets.QLabel(self.currentFrame)
        self.rawTextLabel.setObjectName("rawTextLabel")
        self.horizontalLayout.addWidget(self.rawTextLabel)
        self.rawTextCurrentLabel = QtWidgets.QLabel(self.currentFrame)
        self.rawTextCurrentLabel.setText("")
        self.rawTextCurrentLabel.setObjectName("rawTextCurrentLabel")
        self.horizontalLayout.addWidget(self.rawTextCurrentLabel)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.combineButton = QtWidgets.QToolButton(self.currentFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.combineButton.sizePolicy().hasHeightForWidth())
        self.combineButton.setSizePolicy(sizePolicy)
        self.combineButton.setAutoFillBackground(False)
        self.combineButton.setStyleSheet("")
        self.combineButton.setObjectName("combineButton")
        self.horizontalLayout.addWidget(self.combineButton)
        self.rawTextSaveButton = QtWidgets.QToolButton(self.currentFrame)
        self.rawTextSaveButton.setStyleSheet("")
        self.rawTextSaveButton.setObjectName("rawTextSaveButton")
        self.horizontalLayout.addWidget(self.rawTextSaveButton)
        self.rawTextDeleteButton = QtWidgets.QToolButton(self.currentFrame)
        self.rawTextDeleteButton.setStyleSheet("")
        self.rawTextDeleteButton.setObjectName("rawTextDeleteButton")
        self.horizontalLayout.addWidget(self.rawTextDeleteButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.rawTextTextEdit = QtWidgets.QPlainTextEdit(self.currentFrame)
        self.rawTextTextEdit.setObjectName("rawTextTextEdit")
        self.verticalLayout_2.addWidget(self.rawTextTextEdit)
        self.gridLayout.addWidget(self.currentFrame, 1, 1, 1, 1)
        self.previousFrame = QtWidgets.QFrame(self.centralwidget)
        self.previousFrame.setFrameShape(QtWidgets.QFrame.Panel)
        self.previousFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.previousFrame.setObjectName("previousFrame")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.previousFrame)
        self.verticalLayout_3.setContentsMargins(-1, -1, -1, 12)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.previousControlsLayout = QtWidgets.QHBoxLayout()
        self.previousControlsLayout.setSpacing(2)
        self.previousControlsLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.previousControlsLayout.setContentsMargins(-1, -1, -1, 0)
        self.previousControlsLayout.setObjectName("previousControlsLayout")
        self.previousEntryLabel = QtWidgets.QLabel(self.previousFrame)
        self.previousEntryLabel.setObjectName("previousEntryLabel")
        self.previousControlsLayout.addWidget(self.previousEntryLabel)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.previousControlsLayout.addItem(spacerItem2)
        self.previousENtrySaveButton = QtWidgets.QToolButton(self.previousFrame)
        self.previousENtrySaveButton.setStyleSheet("")
        self.previousENtrySaveButton.setObjectName("previousENtrySaveButton")
        self.previousControlsLayout.addWidget(self.previousENtrySaveButton)
        self.previousEntryDeleteButton = QtWidgets.QToolButton(self.previousFrame)
        self.previousEntryDeleteButton.setStyleSheet("")
        self.previousEntryDeleteButton.setObjectName("previousEntryDeleteButton")
        self.previousControlsLayout.addWidget(self.previousEntryDeleteButton)
        self.verticalLayout_3.addLayout(self.previousControlsLayout)
        self.previousEntryTextEdit = QtWidgets.QPlainTextEdit(self.previousFrame)
        self.previousEntryTextEdit.setObjectName("previousEntryTextEdit")
        self.verticalLayout_3.addWidget(self.previousEntryTextEdit)
        self.gridLayout.addWidget(self.previousFrame, 0, 1, 1, 1)
        self.horizontalLayout_2.addLayout(self.gridLayout)
        self.treeWidget = QtWidgets.QTreeWidget(self.centralwidget)
        self.treeWidget.setMinimumSize(QtCore.QSize(631, 0))
        self.treeWidget.setMaximumSize(QtCore.QSize(631, 16777215))
        self.treeWidget.setUniformRowHeights(True)
        self.treeWidget.setAnimated(True)
        self.treeWidget.setWordWrap(True)
        self.treeWidget.setExpandsOnDoubleClick(False)
        self.treeWidget.setObjectName("treeWidget")
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        item_0.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_2.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_2.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_2.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_2.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_2.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_3 = QtWidgets.QTreeWidgetItem(item_2)
        item_3 = QtWidgets.QTreeWidgetItem(item_2)
        item_4 = QtWidgets.QTreeWidgetItem(item_3)
        item_4.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        item_3 = QtWidgets.QTreeWidgetItem(item_2)
        item_4 = QtWidgets.QTreeWidgetItem(item_3)
        item_4 = QtWidgets.QTreeWidgetItem(item_3)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_3 = QtWidgets.QTreeWidgetItem(item_2)
        item_3 = QtWidgets.QTreeWidgetItem(item_2)
        item_3 = QtWidgets.QTreeWidgetItem(item_2)
        item_3 = QtWidgets.QTreeWidgetItem(item_2)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        self.treeWidget.header().setCascadingSectionResizes(True)
        self.treeWidget.header().setDefaultSectionSize(400)
        self.treeWidget.header().setMinimumSectionSize(300)
        self.horizontalLayout_2.addWidget(self.treeWidget)
        self.verticalLayout_5.addLayout(self.horizontalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1524, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuExport = QtWidgets.QMenu(self.menuFile)
        self.menuExport.setObjectName("menuExport")
        self.menuImport = QtWidgets.QMenu(self.menuFile)
        self.menuImport.setObjectName("menuImport")
        self.menuQuit = QtWidgets.QMenu(self.menubar)
        self.menuQuit.setObjectName("menuQuit")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionOpen_XML_for_analyze = QtWidgets.QAction(MainWindow)
        self.actionOpen_XML_for_analyze.setObjectName("actionOpen_XML_for_analyze")
        self.actionCsv = QtWidgets.QAction(MainWindow)
        self.actionCsv.setObjectName("actionCsv")
        self.actionJSON = QtWidgets.QAction(MainWindow)
        self.actionJSON.setObjectName("actionJSON")
        self.actionOpen_txt = QtWidgets.QAction(MainWindow)
        self.actionOpen_txt.setObjectName("actionOpen_txt")
        self.actionSave_changes_to_xml = QtWidgets.QAction(MainWindow)
        self.actionSave_changes_to_xml.setObjectName("actionSave_changes_to_xml")
        self.actionFrom_txt_OCR = QtWidgets.QAction(MainWindow)
        self.actionFrom_txt_OCR.setObjectName("actionFrom_txt_OCR")
        self.actionRun_analysis_for_all = QtWidgets.QAction(MainWindow)
        self.actionRun_analysis_for_all.setObjectName("actionRun_analysis_for_all")
        self.actionRun_analysis_for_current = QtWidgets.QAction(MainWindow)
        self.actionRun_analysis_for_current.setObjectName("actionRun_analysis_for_current")
        self.actionCreate_a_new_Person = QtWidgets.QAction(MainWindow)
        self.actionCreate_a_new_Person.setObjectName("actionCreate_a_new_Person")
        self.menuExport.addAction(self.actionCsv)
        self.menuExport.addAction(self.actionJSON)
        self.menuImport.addAction(self.actionFrom_txt_OCR)
        self.menuFile.addAction(self.actionOpen_XML_for_analyze)
        self.menuFile.addAction(self.actionSave_changes_to_xml)
        self.menuFile.addAction(self.menuExport.menuAction())
        self.menuFile.addAction(self.menuImport.menuAction())
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuQuit.menuAction())
        self.toolBar.addAction(self.actionRun_analysis_for_all)
        self.toolBar.addAction(self.actionCreate_a_new_Person)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.entriesLabel.setText(_translate("MainWindow", "Entries "))
        self.entriesComboBox.setItemText(0, _translate("MainWindow", "All"))
        self.attributesLabel.setText(_translate("MainWindow", "Found attributes of entry "))
        self.toolButton.setToolTip(_translate("MainWindow", "<html><head/><body><p>Run extraction for current entry and update attributes. Handy for testing if rawtext editing has helped.</p></body></html>"))
        self.toolButton.setText(_translate("MainWindow", "Rerun analysis"))
        self.rawTextLabel.setText(_translate("MainWindow", "Rawtext "))
        self.combineButton.setText(_translate("MainWindow", "Combine"))
        self.rawTextSaveButton.setText(_translate("MainWindow", "Save"))
        self.rawTextDeleteButton.setText(_translate("MainWindow", "Delete"))
        self.previousEntryLabel.setText(_translate("MainWindow", "Previous entry"))
        self.previousENtrySaveButton.setText(_translate("MainWindow", "Save"))
        self.previousEntryDeleteButton.setText(_translate("MainWindow", "Delete"))
        self.treeWidget.setSortingEnabled(False)
        self.treeWidget.headerItem().setText(0, _translate("MainWindow", "Attributes"))
        self.treeWidget.headerItem().setText(1, _translate("MainWindow", "Values"))
        __sortingEnabled = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        self.treeWidget.topLevelItem(0).setText(0, _translate("MainWindow", "Surname"))
        self.treeWidget.topLevelItem(0).setText(1, _translate("MainWindow", "Matikainen"))
        self.treeWidget.topLevelItem(1).setText(0, _translate("MainWindow", "First names"))
        self.treeWidget.topLevelItem(1).setText(1, _translate("MainWindow", "Jarkko Juhani"))
        self.treeWidget.topLevelItem(2).setText(0, _translate("MainWindow", "Birthday"))
        self.treeWidget.topLevelItem(2).child(0).setText(0, _translate("MainWindow", "year"))
        self.treeWidget.topLevelItem(2).child(0).setText(1, _translate("MainWindow", "1923"))
        self.treeWidget.topLevelItem(2).child(1).setText(0, _translate("MainWindow", "place"))
        self.treeWidget.topLevelItem(2).child(1).setText(1, _translate("MainWindow", "Suonenjoki"))
        self.treeWidget.topLevelItem(2).child(2).setText(0, _translate("MainWindow", "month"))
        self.treeWidget.topLevelItem(2).child(2).setText(1, _translate("MainWindow", "1"))
        self.treeWidget.topLevelItem(2).child(3).setText(0, _translate("MainWindow", "day"))
        self.treeWidget.topLevelItem(2).child(3).setText(1, _translate("MainWindow", "12"))
        self.treeWidget.topLevelItem(3).setText(0, _translate("MainWindow", "Death"))
        self.treeWidget.topLevelItem(3).child(0).setText(0, _translate("MainWindow", "year"))
        self.treeWidget.topLevelItem(3).child(1).setText(0, _translate("MainWindow", "month"))
        self.treeWidget.topLevelItem(3).child(2).setText(0, _translate("MainWindow", "fallen"))
        self.treeWidget.topLevelItem(3).child(3).setText(0, _translate("MainWindow", "day"))
        self.treeWidget.topLevelItem(4).setText(0, _translate("MainWindow", "Profession"))
        self.treeWidget.topLevelItem(4).setText(1, _translate("MainWindow", "mv"))
        self.treeWidget.topLevelItem(5).setText(0, _translate("MainWindow", "Service"))
        self.treeWidget.topLevelItem(5).child(0).setText(0, _translate("MainWindow", "Talvisota"))
        self.treeWidget.topLevelItem(5).child(0).setText(1, _translate("MainWindow", "True"))
        self.treeWidget.topLevelItem(5).child(0).child(0).setText(0, _translate("MainWindow", "Regiments"))
        self.treeWidget.topLevelItem(5).child(0).child(0).setText(1, _translate("MainWindow", "ErP 33"))
        self.treeWidget.topLevelItem(5).child(1).setText(0, _translate("MainWindow", "Rank"))
        self.treeWidget.topLevelItem(5).child(1).setText(1, _translate("MainWindow", "ylil 44"))
        self.treeWidget.topLevelItem(5).child(2).setText(0, _translate("MainWindow", "Medals"))
        self.treeWidget.topLevelItem(5).child(2).setText(1, _translate("MainWindow", "Vm 1, Vm 2"))
        self.treeWidget.topLevelItem(5).child(3).setText(0, _translate("MainWindow", "Jatkosota"))
        self.treeWidget.topLevelItem(5).child(3).setText(1, _translate("MainWindow", "True"))
        self.treeWidget.topLevelItem(5).child(3).child(0).setText(0, _translate("MainWindow", "Regiments"))
        self.treeWidget.topLevelItem(5).child(3).child(0).setText(1, _translate("MainWindow", "JR 1, JR49"))
        self.treeWidget.topLevelItem(5).child(4).setText(0, _translate("MainWindow", "Demobilization"))
        self.treeWidget.topLevelItem(5).child(4).child(0).setText(0, _translate("MainWindow", "year"))
        self.treeWidget.topLevelItem(5).child(4).child(0).setText(1, _translate("MainWindow", "1944"))
        self.treeWidget.topLevelItem(5).child(4).child(1).setText(0, _translate("MainWindow", "place"))
        self.treeWidget.topLevelItem(5).child(4).child(1).setText(1, _translate("MainWindow", "Kotka"))
        self.treeWidget.topLevelItem(5).child(4).child(2).setText(0, _translate("MainWindow", "month"))
        self.treeWidget.topLevelItem(5).child(4).child(2).setText(1, _translate("MainWindow", "9"))
        self.treeWidget.topLevelItem(5).child(4).child(3).setText(0, _translate("MainWindow", "day"))
        self.treeWidget.topLevelItem(5).child(4).child(3).setText(1, _translate("MainWindow", "11"))
        self.treeWidget.topLevelItem(6).setText(0, _translate("MainWindow", "Spouses"))
        self.treeWidget.topLevelItem(6).child(0).setText(0, _translate("MainWindow", "Orvokki Pyörä"))
        self.treeWidget.topLevelItem(6).child(0).child(0).setText(0, _translate("MainWindow", "Wedding year"))
        self.treeWidget.topLevelItem(6).child(0).child(0).setText(1, _translate("MainWindow", "1947"))
        self.treeWidget.topLevelItem(6).child(0).child(1).setText(0, _translate("MainWindow", "Children"))
        self.treeWidget.topLevelItem(6).child(0).child(1).child(0).setText(0, _translate("MainWindow", "Woman\'s previous marriage"))
        self.treeWidget.topLevelItem(6).child(0).child(1).child(1).setText(0, _translate("MainWindow", "Man\'s previous marriage"))
        self.treeWidget.topLevelItem(6).child(0).child(1).child(1).child(0).setText(0, _translate("MainWindow", "Kaija"))
        self.treeWidget.topLevelItem(6).child(0).child(1).child(1).child(0).setText(1, _translate("MainWindow", "1946"))
        self.treeWidget.topLevelItem(6).child(0).child(1).child(2).setText(0, _translate("MainWindow", "Current marriage"))
        self.treeWidget.topLevelItem(6).child(0).child(1).child(2).child(0).setText(0, _translate("MainWindow", "Matti"))
        self.treeWidget.topLevelItem(6).child(0).child(1).child(2).child(0).setText(1, _translate("MainWindow", "1948"))
        self.treeWidget.topLevelItem(6).child(0).child(1).child(2).child(1).setText(0, _translate("MainWindow", "Jussi"))
        self.treeWidget.topLevelItem(6).child(0).child(1).child(2).child(1).setText(1, _translate("MainWindow", "1950"))
        self.treeWidget.topLevelItem(6).child(0).child(2).setText(0, _translate("MainWindow", "Birthday"))
        self.treeWidget.topLevelItem(6).child(0).child(2).child(0).setText(0, _translate("MainWindow", "year"))
        self.treeWidget.topLevelItem(6).child(0).child(2).child(0).setText(1, _translate("MainWindow", "1925"))
        self.treeWidget.topLevelItem(6).child(0).child(2).child(1).setText(0, _translate("MainWindow", "place"))
        self.treeWidget.topLevelItem(6).child(0).child(2).child(1).setText(1, _translate("MainWindow", "Iidesranta"))
        self.treeWidget.topLevelItem(6).child(0).child(2).child(2).setText(0, _translate("MainWindow", "month"))
        self.treeWidget.topLevelItem(6).child(0).child(2).child(2).setText(1, _translate("MainWindow", "7"))
        self.treeWidget.topLevelItem(6).child(0).child(2).child(3).setText(0, _translate("MainWindow", "day"))
        self.treeWidget.topLevelItem(6).child(0).child(2).child(3).setText(1, _translate("MainWindow", "4"))
        self.treeWidget.topLevelItem(7).setText(0, _translate("MainWindow", "Total childcount"))
        self.treeWidget.topLevelItem(7).setText(1, _translate("MainWindow", "3"))
        self.treeWidget.topLevelItem(8).setText(0, _translate("MainWindow", "Children without mother data"))
        self.treeWidget.topLevelItem(9).setText(0, _translate("MainWindow", "Hobbies"))
        self.treeWidget.topLevelItem(9).setText(1, _translate("MainWindow", "Kalastus, metsästys"))
        self.treeWidget.topLevelItem(10).setText(0, _translate("MainWindow", "Address"))
        self.treeWidget.topLevelItem(10).setText(1, _translate("MainWindow", "Mäntykaari 3, Lietsala"))
        self.treeWidget.setSortingEnabled(__sortingEnabled)
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuExport.setTitle(_translate("MainWindow", "Export"))
        self.menuImport.setTitle(_translate("MainWindow", "Import"))
        self.menuQuit.setTitle(_translate("MainWindow", "Quit"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionOpen_XML_for_analyze.setText(_translate("MainWindow", "Open xml"))
        self.actionCsv.setText(_translate("MainWindow", "CSV"))
        self.actionJSON.setText(_translate("MainWindow", "JSON"))
        self.actionOpen_txt.setText(_translate("MainWindow", "Open txt"))
        self.actionSave_changes_to_xml.setText(_translate("MainWindow", "Save changes to xml"))
        self.actionFrom_txt_OCR.setText(_translate("MainWindow", "From txt (OCR)"))
        self.actionRun_analysis_for_all.setText(_translate("MainWindow", "Run analysis for all"))
        self.actionRun_analysis_for_all.setToolTip(_translate("MainWindow", "Run analysis for all entries in current file"))
        self.actionRun_analysis_for_all.setShortcut(_translate("MainWindow", "Ctrl+Shift+R"))
        self.actionRun_analysis_for_current.setText(_translate("MainWindow", "Run analysis for current"))
        self.actionRun_analysis_for_current.setToolTip(_translate("MainWindow", "Run extraction for current person and update attributes"))
        self.actionRun_analysis_for_current.setShortcut(_translate("MainWindow", "Ctrl+R"))
        self.actionCreate_a_new_Person.setText(_translate("MainWindow", "Create a  new Person"))
        self.actionCreate_a_new_Person.setToolTip(_translate("MainWindow", "Create a new person from rawtext"))

from qtgui.entrytable import EntryTableView
from qtgui.entriesModels import EntriesListView

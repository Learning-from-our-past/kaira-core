# -*- coding: utf-8 -*-
import ntpath
import csv

class ErrorCsvBuilder:
    CSVPATH = "../csv/errors/"
    filepath = ""
    filename = ""
    openedCsv = None
    csvWriter = None

    def __init__(self):
        pass

    def openCsv(self, filepath):
        self.filepath = filepath
        self.filename = ntpath.basename(self.filepath)
        self._initCsv()


    def _initCsv(self):
        self.openedCsv = open(self.CSVPATH + self.filename+ "_errors.csv", "w", encoding="utf-8")
        self.csvWriter = csv.writer(self.openedCsv, delimiter=";")
        self._writeCsvHeaders()

    def _writeCsvHeaders(self):
         self.csvWriter.writerow(["Exception","Details", "type", "Entry text"])

    def writeRow(self, dataList):
        self.csvWriter.writerow(dataList)

    def closeCsv(self):
        self.openedCsv.close()
        self.openedCsv = None
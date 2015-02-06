# -*- coding: utf-8 -*-
import ntpath
import unicodecsv

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
        self.initCsv()


    def initCsv(self):
        self.openedCsv = open(self.CSVPATH + self.filename+ "_errors.csv", "wb")
        self.csvWriter = unicodecsv.writer(self.openedCsv, delimiter=";")
        self.writeCsvHeaders()

    def writeCsvHeaders(self):
         self.csvWriter.writerow(["Exception","Details", "type", "Entry text"])

    def writeRow(self, dataList):
        self.csvWriter.writerow(dataList)


    def closeCsv(self):
        self.openedCsv.close()
        self.openedCsv = None
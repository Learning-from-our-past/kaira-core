# -*- coding: utf-8 -*-
import ntpath
import csv
from abc import abstractmethod

class ResultCsvBuilderInterface:

    #TODO: POISTA SISÄISEN TOTETUKSEN FUNKTIOT SILLÄ NE VOIVAT VAPAASTI VAIHDELLA
    def __init__(self):
        pass

    @abstractmethod
    def openCsv(self, filepath):
        self.filepath = filepath
        self.filename = ntpath.basename(self.filepath)
        self._initCsv()

    @abstractmethod
    def writeRow(self, dataDict):
        pass

    #tranforms the dict of the entry to a format which can be written into csv
    def _createRowFromDict(self, persondatadict):
        pass


    @abstractmethod
    def closeCsv(self):
        self.openedCsv.close()
        self.openedCsv = None
# -*- coding: utf-8 -*-
import ntpath
import json
from abc import abstractmethod
from interface.jsonbuilderinterface import ResultJsonBuilderInterface

class ResultJsonBuilder(ResultJsonBuilderInterface):

    #TODO: POISTA SISÄISEN TOTETUKSEN FUNKTIOT SILLÄ NE VOIVAT VAPAASTI VAIHDELLA
    def __init__(self):
        pass

    def openJson(self, filepath):
        self.filepath = filepath
        self.filename = ntpath.basename(self.filepath)
        self._initJson()


    def _initJson(self):
        self.openedJson = open(self.filepath, "w", newline='', encoding="utf-8")
        self.jsonFormat = []

    def writeEntry(self, dataDict):
        self._writeJsonEntry(dataDict)

    def _writeJsonEntry(self, dataDict):
        person = {}
        for key, property in dataDict.items():
            if key != "cursorLocation":
                person[key] = property
        self.jsonFormat.append(person)

    def closeJson(self):
        #self.openedJson.write(json.dumps(self.jsonFormat, indent=4, ensure_ascii=False))
        json.dump(self.jsonFormat,self.openedJson, indent=4, ensure_ascii=False)
        self.openedJson.close()
        self.openedJson = None

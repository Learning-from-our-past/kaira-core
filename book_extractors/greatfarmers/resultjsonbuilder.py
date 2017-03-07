# -*- coding: utf-8 -*-
import ntpath
import json
from abc import abstractmethod
from interface.jsonbuilderinterface import ResultJsonBuilderInterface


class ResultJsonBuilder(ResultJsonBuilderInterface):

    def __init__(self):
        pass

    def openJson(self, file):
        if type(file) == str:
            self.openedJson = open(file, "w", newline='', encoding="utf-8")
        else:
            self.openedJson = file

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
        json.dump(self.jsonFormat, self.openedJson, indent=4, ensure_ascii=False)
        self.openedJson.close()
        self.openedJson = None

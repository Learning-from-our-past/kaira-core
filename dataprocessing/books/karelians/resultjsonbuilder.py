# -*- coding: utf-8 -*-
import ntpath
import json
from abc import abstractmethod
from books.karelians.extractionkeys import KEYS
from interface.valuewrapper import ValueWrapper
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
                person[key] = self._unwrap(property)
        self.jsonFormat.append(person)


    def _unwrap(self, data):
        """
        A recursive function to unwrap all the ValueWrappers and return a pure dict from them.
        :param valuewrap:
        :return:
        """
        if isinstance(data, ValueWrapper):
            if isinstance(data.value, dict):
                result = {}
                for key, value in data.value.items():
                    result[key] = self._unwrap(value)
            elif isinstance(data.value, list):
                result = []
                for index, value in enumerate(data.value):
                    result.append(self._unwrap(value))
            else:
                return data.value   #primitive data structure
        else:
            return data

        return result


    def closeJson(self):
        self.openedJson.write(json.dumps(self.jsonFormat, indent=4, ensure_ascii=False))
        self.openedJson.close()
        self.openedJson = None

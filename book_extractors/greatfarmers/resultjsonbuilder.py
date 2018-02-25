# -*- coding: utf-8 -*-
import json
from core.interface.jsonbuilderinterface import ResultJsonBuilderInterface


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

    def _remove_cursor_locations(self, l):
        if type(l) is dict:
            if 'cursorLocation' in l:
                del l['cursorLocation']

            for key, value in l.items():
                if type(value) is list or type(value) is dict:
                    self._remove_cursor_locations(value)

        if type(l) is list:
            for value in l:
                if type(value) is list or type(value) is dict:
                    self._remove_cursor_locations(value)

    def _writeJsonEntry(self, dataDict):
        person = {}
        for key, property in dataDict.items():
            if key != "cursorLocation":
                person[key] = property

        self._remove_cursor_locations(person)
        self.jsonFormat.append(person)

    def closeJson(self):
        json.dump(self.jsonFormat, self.openedJson, indent=4, ensure_ascii=False)
        self.openedJson.close()
        self.openedJson = None

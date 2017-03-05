# -*- coding: utf-8 -*-
import ntpath
import json
from abc import abstractmethod
from books.karelians.extractionkeys import KEYS
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

        self.jsonFormat.append(self._transform_data_for_export(person))

    def _transform_data_for_export(self, data):
        # Concat locations to one array
        locations = data[KEYS["karelianlocations"]] + data[KEYS["otherlocations"]]
        del data[KEYS["karelianlocations"]]
        del data[KEYS["otherlocations"]]
        data[KEYS["locations"]] = locations

        for location in locations:
            location["movedIn"] = self.int_or_none(location["movedIn"])
            location["movedOut"] = self.int_or_none(location["movedOut"])

        data['birthDay'] = self.int_or_none(data['birthDay'])
        data['birthMonth'] = self.int_or_none(data['birthMonth'])
        data['birthYear'] = self.int_or_none(data['birthYear'])

        data["spouse"]["weddingYear"] = self.int_or_none(data["spouse"]["weddingYear"])
        data["spouse"]["deathYear"] = self.int_or_none(data["spouse"]["deathYear"])
        data["spouse"]["birthData"]['birthDay'] = self.int_or_none(data["spouse"]["birthData"]['birthDay'])
        data["spouse"]["birthData"]['birthMonth'] = self.int_or_none(data["spouse"]["birthData"]['birthMonth'])
        data["spouse"]["birthData"]['birthYear'] = self.int_or_none(data["spouse"]["birthData"]['birthYear'])

        for child in data["children"]:
            child["birthYear"] = self.int_or_none(child["birthYear"])

        return data


    def closeJson(self):
        json.dump(self.jsonFormat,self.openedJson, indent=4, ensure_ascii=False)
        self.openedJson.close()
        self.openedJson = None

# -*- coding: utf-8 -*-
import json
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
        data['quantities']['sheep'] = self.int_or_none(data['quantities']['sheep'])
        data['quantities']['nuori'] = self.int_or_none(data['quantities']['nuori'])
        data['quantities']['emakko'] = self.int_or_none(data['quantities']['emakko'])
        data['quantities']['slaughterAnimal'] = self.int_or_none(data['quantities']['slaughterAnimal'])
        data['quantities']['dairyCow'] = self.int_or_none(data['quantities']['dairyCow'])
        data['quantities']['lihotussika'] = self.int_or_none(data['quantities']['lihotussika'])
        data['quantities']['chicken'] = self.int_or_none(data['quantities']['chicken'])
        data['quantities']['rooms'] = self.int_or_none(data['quantities']['rooms'])
        data['owner']['ownerFrom'] = self.int_or_none(data['owner']['ownerFrom'])

        data['owner']['birthData']['birthDay'] = self.int_or_none(data['owner']['birthData']['birthDay'])
        data['owner']['birthData']['birthMonth'] = self.int_or_none(data['owner']['birthData']['birthMonth'])
        data['owner']['birthData']['birthYear'] = self.int_or_none(data['owner']['birthData']['birthYear'])

        data['farmDetails']['wholeArea'] = self.float_or_none(data['farmDetails']['wholeArea'])
        data['farmDetails']['forestArea'] = self.float_or_none(data['farmDetails']['forestArea'])
        data['farmDetails']['meadowArea'] = self.float_or_none(data['farmDetails']['meadowArea'])
        data['farmDetails']['fieldArea'] = self.float_or_none(data['farmDetails']['fieldArea'])
        data['farmDetails']['wasteArea'] = self.float_or_none(data['farmDetails']['wasteArea'])

        data['hostess']['birthData']['birthDay'] = self.int_or_none(data['hostess']['birthData']['birthDay'])
        data['hostess']['birthData']['birthMonth'] = self.int_or_none(data['hostess']['birthData']['birthMonth'])
        data['hostess']['birthData']['birthYear'] = self.int_or_none(data['hostess']['birthData']['birthYear'])

        for child in data['children']:
            child['birthYear'] = self.int_or_none(child['birthYear'])
        return data



    def closeJson(self):
        json.dump(self.jsonFormat,self.openedJson, indent=4, ensure_ascii=False)
        self.openedJson.close()
        self.openedJson = None

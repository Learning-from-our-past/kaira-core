# -*- coding: utf-8 -*-
import ntpath
import json
from abc import abstractmethod
from interface.valuewrapper import ValueWrapper
from interface.jsonbuilderinterface import ResultJsonBuilderInterface

class ResultJsonBuilder(ResultJsonBuilderInterface):

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

        self.jsonFormat.append(self._transform_data_for_export(person))

    def _transform_data_for_export(self, data):
        data['quantities']['lammas'] = self.int_or_none(data['quantities']['lammas'])
        data['quantities']['nuori'] = self.int_or_none(data['quantities']['nuori'])
        data['quantities']['emakko'] = self.int_or_none(data['quantities']['emakko'])
        data['quantities']['teuraselain'] = self.int_or_none(data['quantities']['teuraselain'])
        data['quantities']['lypsylehma'] = self.int_or_none(data['quantities']['lypsylehma'])
        data['quantities']['lihotussika'] = self.int_or_none(data['quantities']['lihotussika'])
        data['quantities']['kanoja'] = self.int_or_none(data['quantities']['kanoja'])
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
        json.dump(self.jsonFormat,self.openedJson, indent=4, ensure_ascii=False)
        self.openedJson.close()
        self.openedJson = None

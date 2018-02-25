# -*- coding: utf-8 -*-
import json
from core.interface.jsonbuilderinterface import ResultJsonBuilderInterface


class ResultJsonBuilder(ResultJsonBuilderInterface):

    def __init__(self):
        super(ResultJsonBuilder).__init__()
        self._opened_json = None
        self._json_format = []

    def open_json(self, file):
        if type(file) == str:
            self._opened_json = open(file, 'w', newline='', encoding='utf-8')
        else:
            self._opened_json = file

        self._json_format = []

    def write_entry(self, data_dict):
        self._write_json_entry(data_dict)

    def _write_json_entry(self, data_dict):
        person = {}
        for key, property in data_dict.items():
            if key != 'cursorLocation':
                person[key] = property

        self._json_format.append(person)

    def close_json(self):
        json.dump(self._json_format, self._opened_json, indent=4, ensure_ascii=False)
        self._opened_json.close()
        self._opened_json = None

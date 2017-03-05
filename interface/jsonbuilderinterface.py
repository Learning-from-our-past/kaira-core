# -*- coding: utf-8 -*-
from abc import abstractmethod


class ResultJsonBuilderInterface:

    def __init__(self):
        pass

    @abstractmethod
    def openJson(self, filepath):
        pass

    @abstractmethod
    def writeEntry(self, dataDict):
        pass

    @abstractmethod
    def closeJson(self):
        pass

    def int_or_none(self, value):
        try:
            return int(value)
        except (TypeError, ValueError):
            return None

    def float_or_none(self, value):
        try:
            value = value.replace('\w', '')
            return float(value.replace(',', '.'))
        except (TypeError, ValueError):
            return None

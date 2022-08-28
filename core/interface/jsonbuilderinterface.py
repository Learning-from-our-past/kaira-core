# -*- coding: utf-8 -*-
from abc import abstractmethod


class ResultJsonBuilderInterface:
    def __init__(self):
        pass

    @abstractmethod
    def open_json(self, filepath):
        pass

    @abstractmethod
    def write_entry(self, dataDict):
        pass

    @abstractmethod
    def close_json(self):
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
        except (TypeError, ValueError, AttributeError):
            return None

"""
This is a temporary class which routes calls from GUI to extractor modules. Idea is that
using it is should be easy during the development to change between soldier and karelian extractors
without modifying GUI-code.
"""

from books.soldiers.chunktextfile import ChunkTextFile as SoldierChunk
from books.soldiers.processData import ProcessData as SoldierProcessdata
from books.soldiers.resultcsvbuilder import ResultCsvBuilder as SoldierCsvBuilder
from books.karelians.chunktextfile import PersonPreprocessor as KarelianChunk
from books.karelians.processData import ProcessData as KarelianProcessdata
from books.karelians.resultcsvbuilder import ResultCsvBuilder as KarelianCsvBuilder

class Router():

    #these are equivalent of the "bookseries" attribute in xml datafiles.
    SOLDIERS = "Suomen rintamamiehet"
    KARELIANS = "Siirtokarjalaisten tie"

    @staticmethod
    def get_chunktext_class(extractor):
        if extractor == Router.KARELIANS:
            return KarelianChunk
        elif extractor == Router.SOLDIERS:
            return SoldierChunk
        else:
            raise NoExtractorAvailable()

    @staticmethod
    def get_processdata_class(extractor):
        if extractor == Router.KARELIANS:
            return KarelianProcessdata
        elif extractor == Router.SOLDIERS:
            return SoldierProcessdata
        else:
            raise NoExtractorAvailable()

    @staticmethod
    def get_csvbuilder_class(extractor):
        if extractor == Router.KARELIANS:
            return KarelianCsvBuilder
        elif extractor == Router.SOLDIERS:
            return SoldierCsvBuilder
        else:
            raise NoExtractorAvailable()

class NoExtractorAvailable(Exception):

    def __init__(self):
        pass

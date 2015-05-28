"""
This is a temporary class which routes calls from GUI to extractor modules. Idea is that
using it is should be easy during the development to change between soldier and karelian extractors
without modifying GUI-code.
"""

from books.soldiers.chunktextfile import ChunkTextFile as SoldierChunk
from books.soldiers.processData import ProcessData as SoldierProcessdata
from books.soldiers.resultcsvbuilder import ResultCsvBuilder as SoldierCsvBuilder
from books.soldiers.resultjsonbuilder import ResultJsonBuilder as SoldierJsonBuilder

from books.karelians.chunktextfile import PersonPreprocessor as KarelianChunk
from books.karelians.processData import ProcessData as KarelianProcessdata
from books.karelians.resultcsvbuilder import ResultCsvBuilder as KarelianCsvBuilder
from books.karelians.resultjsonbuilder import ResultJsonBuilder as KarelianJsonBuilder

from books.farmers.chunktextfile import PersonPreprocessor as FarmersChunk
from books.farmers.processData import ProcessData as FarmersProcessdata
from books.farmers.resultcsvbuilder import ResultCsvBuilder as FarmersCsvBuilder
from books.farmers.resultjsonbuilder import ResultJsonBuilder as FarmersJsonBuilder


class Router():

    #Bookseries which tool supports. IMPORTANT: The value HAS TO BE same as
    #bookseries attribute's value in xml files!!!
    BOOKSERIES = {
        "SOLDIERS" : "Suomen rintamamiehet",
        "KARELIANS" : "Siirtokarjalaisten tie",
        "FARMERS" : "Suomen pienviljelijat"
    }




    @staticmethod
    def get_bookseries_list():
        l = list(Router.BOOKSERIES.values())
        l.sort()
        return l


    @staticmethod
    def get_chunktext_class(extractor):
        if extractor == Router.BOOKSERIES["KARELIANS"]:
            return KarelianChunk
        elif extractor == Router.BOOKSERIES["SOLDIERS"]:
            return SoldierChunk
        elif extractor == Router.BOOKSERIES["FARMERS"]:
            return FarmersChunk
        else:
            raise NoExtractorAvailable()

    @staticmethod
    def get_processdata_class(extractor):
        if extractor == Router.BOOKSERIES["KARELIANS"]:
            return KarelianProcessdata
        elif extractor == Router.BOOKSERIES["SOLDIERS"]:
            return SoldierProcessdata
        elif extractor == Router.BOOKSERIES["FARMERS"]:
            return FarmersProcessdata
        else:
            raise NoExtractorAvailable()

    @staticmethod
    def get_csvbuilder_class(extractor):
        if extractor == Router.BOOKSERIES["KARELIANS"]:
            return KarelianCsvBuilder
        elif extractor == Router.BOOKSERIES["SOLDIERS"]:
            return SoldierCsvBuilder
        elif extractor == Router.BOOKSERIES["FARMERS"]:
            return FarmersCsvBuilder
        else:
            raise NoExtractorAvailable()

    @staticmethod
    def get_jsonbuilder_class(extractor):
        if extractor == Router.BOOKSERIES["KARELIANS"]:
            return KarelianJsonBuilder
        elif extractor == Router.BOOKSERIES["SOLDIERS"]:
            return SoldierJsonBuilder
        elif extractor == Router.BOOKSERIES["FARMERS"]:
            return FarmersJsonBuilder
        else:
            raise NoExtractorAvailable()

class NoExtractorAvailable(Exception):

    def __init__(self):
        pass

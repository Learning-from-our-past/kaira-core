"""
This is a temporary class which routes calls from GUI to extractor modules. Idea is that
using it is should be easy during the development to change between soldier and karelian extractors
without modifying GUI-code.
"""

from books.soldiers.chunktextfile import ChunkTextFile as SoldierChunk
from books.soldiers.processData import ProcessData as SoldierProcessdata
from books.soldiers.resultcsvbuilder import ResultCsvBuilder as SoldierCsvBuilder

from books.karelians.chunktextfile import PersonPreprocessor as KarelianChunk

def get_chunktext_class():
    return KarelianChunk

def get_processdata_class():
    return SoldierProcessdata

def get_csvbuilder_class():
    return SoldierCsvBuilder


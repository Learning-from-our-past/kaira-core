# -*- coding: utf-8 -*-
from nose.tools import *
import lxml.etree as etree
from books.karelians.extraction.extractors.birthdayExtractor import BirthdayExtractor
from shared.exceptionlogger import ExceptionLogger
from books.karelians.extractionkeys import KEYS
from interface.valuewrapper import ValueWrapper

def build_xml_representation(text, name):
    mockXml = etree.Element("PERSON")
    mockXml.text = text
    mockXml.attrib["name"] = name
    return mockXml

def transform_date_extract_to_string(result):
    return str(result["BirthDay"].value) + str(result["BirthMonth"].value) + str(result["BirthYear"].value)


class TestBirthdayExtractor:

    mock_entries = {"nonspace": [
        { "entry": "maanviljelijä, synt. 22. 9. -09Hiitolassa. Puol. Sylvi Vilma o.s.", "result": "2291909"},
        { "entry": "Schvvarz, emäntä, synt. 30. 8. -21 Hiitolassa. Avioit. -44. Poika: ", "result": "3081921"},
        { "entry": "o.s. Sormunen, rouva, synt. 29. 9. -18 Hiitolassa. Puol. ", "result": "2991918"},
        { "entry": "Kalle Viljam, ahtaaja, synt. 12. 2.    16Ahlaisissa. Avioit. -44. Lapset: ", "result": "1221916"},
        { "entry": "o.s. Peussa, vanhaemäntä. synt. 14, 3. -84 Kuolemajärvellä. Puol. ", "result": "1431884"},
        { "entry": "Jukka, synt. Muurilassa. Kuoli. -41 Urjalassa Lapset:", "result": ""},
        { "entry": "o.s. Rehmonen. ent. Neuvonen, emäntä, synt. 1. 2. -92 Uudellakirkolla. Puol. ", "result": "121892"},
        { "entry": "Ville, maanviljelijä, synt. -91 Uudellakirkolla. Kuoli. -63 Halikossa. Lapset: ", "result": "NoneNone1891"}
    ],
    "whitespace": [
        { "entry": "o.s. Rehmonen. ent. Neuvonen, emäntä, synt. 1. 2. -92 Uudellakirkolla. Puol. ", "result": "121892"},
        { "entry": "Ville, maanviljelijä, synt. -91 Uudellakirkolla. Kuoli. -63 Halikossa. Lapset: ", "result": "NoneNone1891"},
        { "entry": "O.s. Brandt, sotilaskodin hoitaja, synt. 13. 2. -13 Viipurissa. Puol. ", "result": "1321913"},
        { "entry": "Olavi Mikael, konduktööri, synt. 22 12. 14 Yyterissä. Avioit. -41. Tytär: ", "result": "22121914"},
        { "entry": "0. s. Teräväinen, emäntä, synt. 1. 6. -10 Jaakkimassa. Puol. Toimi Johannes, ", "result": "161910"},
        { "entry": "maanviljelijä, synt. 14 7. 06 Peräseinäjoella. Avioit. -51. Tytär: ", "result": "1471906"},
        { "entry": "pienviljelijä, synt. 17. 4. -12 Korpiselällä Puol. ", "result": "1741912"},
        { "entry": "Ida Maria o.s. Smeds, emäntä, synt. 24 9. 10 Vöyrissä, Lapset; ", "result": "2491910"}
    ]}

    """
    Test that date extraction works as it should with spaces and without.
    """
    @classmethod
    def setup_class(self):
        self.eLogger = ExceptionLogger()

    def test_nonspace_dates(self):
        """
        Some of the birthdates are easier to extract by removing spaces from string and then finding the date. That
        method is tested here and should return proper dates for nonspace entries in dict.
        :return:
        """
        for testcase in self.mock_entries["nonspace"]:
            entry = build_xml_representation(testcase["entry"], "NONSPACE1")
            ValueWrapper.xmlEntry = entry
            ex = BirthdayExtractor(entry, self.eLogger, entry)
            ex.setDependencyMatchPositionToZero()
            result_extract = ex.extract(entry.text, {"xml": entry})
            result = transform_date_extract_to_string(result_extract)
            assert_equals(result, testcase["result"])

    def test_whitespace_dates(self):
        """
        Some of the birthdates are easier to extract by removing spaces from string and then finding the date. In other case
        this fails when dots are lacking so we have to try to find the date with spaces.
        :return:
        """
        for testcase in self.mock_entries["whitespace"]:
            entry = build_xml_representation(testcase["entry"], "WHITESPACE1")
            ValueWrapper.xmlEntry = entry
            ex = BirthdayExtractor(entry, self.eLogger, entry)
            ex.setDependencyMatchPositionToZero()
            result_extract = ex.extract(entry.text, {"xml": entry})
            result = transform_date_extract_to_string(result_extract)
            assert_equals(result, testcase["result"])
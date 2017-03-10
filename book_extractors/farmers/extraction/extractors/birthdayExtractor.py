# -*- coding: utf-8 -*-
import re

from book_extractors.common.base_extractor import BaseExtractor
from book_extractors.extraction_exceptions import *
from book_extractors.extraction_pipeline import ExtractionPipeline, configure_extractor
from book_extractors.farmers.extraction.extractors.dateExtractor import DateExtractor
from shared import textUtils
from book_extractors.common.extraction_keys import KEYS
from shared import regexUtils


class BirthdayExtractor(BaseExtractor):

    def extract(self, text, entry):
        super(BirthdayExtractor, self).extract(text, entry)
        self.PATTERN = r"(?:synt)\.?,?(?:(?:(?P<day>\d{1,2})(?:\.|,|:|s)(?P<month>\d{1,2})(?:\.|,|:|s)?-?(?P<year>\d{2,4}))|-(?P<yearOnly>\d{2,4})(?!\.|,|\d)(?=\D\D\D\D\D))" #r'(?:synt)\.?,? ?(?:(?:(?P<day>\d{1,2})(?:\.|,|:|s)? ?(?P<month>\d{1,2})(?:\.|,|:|s)? ?-?(?P<year>\d{2,4})))'
        self.OPTIONS = (re.UNICODE | re.IGNORECASE)    #TODO: TRY IGNORE CASE?

        self._sub_extraction_pipeline = ExtractionPipeline([
            configure_extractor(DateExtractor, extractor_options={'PATTERN': self.PATTERN, 'OPTIONS': self.OPTIONS})
        ])

        self.REQUIRES_MATCH_POSITION = True
        self.SUBSTRING_WIDTH = 100
        self.dateExtractor = None
        self.foundDate = {}
        self.preparedText = ""
        self.error = False

        self.preparedText = self._prepareTextForExtraction(text)
        self._findDate(self.preparedText)
        return self._constructReturnDict()

    def _prepareTextForExtraction(self, text):
        t = textUtils.takeSubStrBasedOnPos(text, self.matchStartPosition, self.SUBSTRING_WIDTH)
        t = textUtils.removeSpacesFromText(t)

        spouseFound = regexUtils.findFirstPositionWithRegexSearch("puol", t, re.IGNORECASE|re.UNICODE)
        if spouseFound != -1:
            t = t[0:spouseFound]

        return t

    def _findDate(self, text):
        try:
            self.foundDate = self._sub_extraction_pipeline.process({'text': text})
            self.matchFinalPosition = self.foundDate['cursorLocation'] + self.matchStartPosition - 4
        except DateException as e:
            #TODO: Better idea to have in DateExtractor class maybe?
            # TODO: Metadata logging here self.errorLogger.logError(BirthdayException.eType, self.currentChild)
            self.error = BirthdayException.eType
            self.foundDate = {"day": "","month": "",
                "year": "", "cursorLocation": ""}


    def _constructReturnDict(self):
        self.foundDate["day"] = self.foundDate["day"]
        self.foundDate["month"] = self.foundDate["month"]
        self.foundDate["year"] = self.foundDate["year"]

        return {KEYS["birthDay"]:  self.foundDate["day"], KEYS["birthMonth"]: self.foundDate["month"],
                KEYS["birthYear"]:  self.foundDate["year"]}

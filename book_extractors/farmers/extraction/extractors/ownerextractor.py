# -*- coding: utf-8 -*-
from book_extractors.common.owner_extractor import CommonOwnerExtractor
from book_extractors.farmers.extraction.extractors.birthdayExtractor import BirthdayExtractor


class OwnerExtractor(CommonOwnerExtractor):

    def __init__(self, key_of_cursor_location_dependent, options):
        if options is None:
            options = {}

        options.update({
            'OWNER_YEAR_PATTERN': r"om(?:\.|,)\s?vuodesta\s(?P<year>\d\d\d\d)",
            'OWNER_NAME_PATTERN': r"(?P<name>[A-ZÄ-Öa-zä-ö -]+(?:o\.s\.)?[A-ZÄ-Öa-zä-ö -]+)(?:\.|,)\ssynt",
            'BIRTHDAY_EXTRACTOR': BirthdayExtractor
        })

        super(OwnerExtractor, self).__init__(key_of_cursor_location_dependent, options)

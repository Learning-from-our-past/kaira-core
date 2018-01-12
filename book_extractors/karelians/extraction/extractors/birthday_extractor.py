# -*- coding: utf-8 -*-
from book_extractors.common.extraction_keys import KEYS
from book_extractors.common.extractors.birthday_extractor import CommonBirthdayExtractor


class BirthdayExtractor(CommonBirthdayExtractor):
    extraction_key = KEYS['birthData']

    def __init__(self, cursor_location_depend_on, options, dependencies_contexts=None):
        if options is None:
            options = {}
        options['PATTERN'] = r"(?:synt)\.?,?(?:\s+)?(?:(?:(?P<day>\d{1,2})(?:\.|,|:|\s+|s)\s?(?P<month>\d{1,2})(?:\.|,|:|\s+|s)?(?:\s+)?-?(?P<year>\d{2,4}))|\s?-(?P<yearOnly>\d{2,4})(?!\.|,|\s|\d)(?=\D\D\D\D\D))"
        options['remove_spaces'] = False
        super(BirthdayExtractor, self).__init__(cursor_location_depend_on, options)

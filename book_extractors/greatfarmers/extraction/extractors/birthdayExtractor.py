# -*- coding: utf-8 -*-
from book_extractors.common.birthday_extractor import CommonBirthdayExtractor


class BirthdayExtractor(CommonBirthdayExtractor):

    def __init__(self, key_of_cursor_location_dependent, options):
        if options is None:
            options = {}
        options['PATTERN'] = r"(?:synt|s)\.?,?(?:(?:(?P<day>\d{1,2})(?:\.|,|:|s)(?P<month>\d{1,2})(?:\.|,|:|s)?-?—?(?P<year>\d{2,4}))|-(?P<yearOnly>\d{2,4})(?!\.|,|\d)(?=\D\D\D\D\D))"
        super(BirthdayExtractor, self).__init__(key_of_cursor_location_dependent, options)

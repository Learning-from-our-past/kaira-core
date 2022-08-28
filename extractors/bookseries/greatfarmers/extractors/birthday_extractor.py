# -*- coding: utf-8 -*-
from extractors.common.extractors.birthday_extractor import CommonBirthdayExtractor


class BirthdayExtractor(CommonBirthdayExtractor):
    extraction_key = 'birthday'

    def __init__(self, cursor_location_depends_on=None, options=None):
        if options is None:
            options = {}
        options[
            'PATTERN'
        ] = r"(?:synt|s)\.?,?(?:(?:(?P<day>\d{1,2})(?:\.|,|:|s)(?P<month>\d{1,2})(?:\.|,|:|s)?-?—?(?P<year>\d{2,4}))|-(?P<yearOnly>\d{2,4})(?!\.|,|\d)(?=\D\D\D\D\D))"
        super(BirthdayExtractor, self).__init__(cursor_location_depends_on, options)

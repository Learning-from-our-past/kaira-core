# -*- coding: utf-8 -*-
from extractors.common.extractors.owner_extractor import CommonOwnerExtractor
from extractors.greatfarmers.extractors.birthday_extractor import BirthdayExtractor
from extractors.common.extraction_keys import KEYS


class OwnerExtractor(CommonOwnerExtractor):
    extraction_key = KEYS['ownerDetails']

    def __init__(self, cursor_location_depends_on=None, options=None):
        if options is None:
            options = {}

        options.update({
            'OWNER_YEAR_PATTERN': r"om(?:\.|,)?\s?(?:vuodesta|vsta)\s(?P<year>\d\d\d\d)",
            'OWNER_NAME_PATTERN': r"(om\s)?(?P<name>[A-ZÄ-Öa-zä-ö -]+(?:o\.s\.)?[A-ZÄ-Öa-zä-ö -]+)(\s(?:synt|s|\.)|\.)",
            'BIRTHDAY_EXTRACTOR': BirthdayExtractor
        })

        super(OwnerExtractor, self).__init__(cursor_location_depends_on, options)

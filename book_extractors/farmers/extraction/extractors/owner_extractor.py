# -*- coding: utf-8 -*-
from book_extractors.common.extractors.owner_extractor import CommonOwnerExtractor
from book_extractors.common.extraction_keys import KEYS


class OwnerExtractor(CommonOwnerExtractor):
    extraction_key = KEYS['ownerDetails']

    def __init__(self, cursor_location_depends_on=None, options=None):
        if options is None:
            options = {}

        options.update({
            'OWNER_YEAR_PATTERN': r"om(?:\.|,)\s?vuodesta\s(?P<year>\d\d\d\d)",
            'OWNER_NAME_PATTERN': r"(?P<name>[A-ZÄ-Öa-zä-ö -]+(?:o\.s\.)?[A-ZÄ-Öa-zä-ö -]+)(?:\.|,)\ssynt"
        })

        super(OwnerExtractor, self).__init__(cursor_location_depends_on, options)

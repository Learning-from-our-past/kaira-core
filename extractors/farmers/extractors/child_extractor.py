import re

from extractors.common.extractors.child_extractor import CommonChildExtractor
from extractors.common.extraction_keys import KEYS

class ChildExtractor(CommonChildExtractor):
    extraction_key = KEYS['children']

    def __init__(self, cursor_location_depends_on=None, options=None):
        super(ChildExtractor, self).__init__(cursor_location_depends_on, options)
        self.CHILD_PATTERN = r"(?:Lapset|tytär|poika|tyttäret|pojat)(;|:)(?P<children>.*?)(?:\.|Tilal{s<=1}|Edelli{s<=1}|hänen{s<=1}|joka{s<=1}|emännän{s<=1}|isännän{s<=1})"
        self.CHILD_OPTIONS = (re.UNICODE | re.IGNORECASE)

        self.SPLIT_PATTERN1 = r"(?P<child>[A-ZÄ-Öa-zä-ö\d\s-]{3,})"
        self.NAME_PATTERN = r"^(?P<name>[a-zä-ö\s-]+)"
        self.YEAR_PATTERN = r"(?P<year>(\d\d))"
        self.LOCATION_PATTERN = r"\d\d\s(?P<location>[a-zä-ö\s-]+$)"
        self.SPLIT_OPTIONS1 = (re.UNICODE | re.IGNORECASE)

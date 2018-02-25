import re
from book_extractors.common.extractors.base_extractor import BaseExtractor
from shared import regexUtils


class PreviousMarriagesFlagExtractor(BaseExtractor):
    extraction_key = 'previousMarriagesFlag'

    def __init__(self, cursor_location_depends_on=None, options=None):
        super(PreviousMarriagesFlagExtractor, self).__init__(cursor_location_depends_on, options)
        self.MANY_MARRIAGE_PATTERN = r"(toisesta|ensimmäisestä|aikaisemmasta|edellisestä|nykyisestä|avioliitosta)"

    def _extract(self, entry, extraction_results, extraction_metadata):
        many_marriages = self._check_many_marriages(entry['text'])
        return self._add_to_extraction_results(many_marriages, extraction_results, extraction_metadata)

    def _check_many_marriages(self, text):
        marriage = regexUtils.search(self.MANY_MARRIAGE_PATTERN, text, (re.UNICODE | re.IGNORECASE))
        return marriage is not None

import re
from core.pipeline_construction.base_extractor import BaseExtractor
from core.utils import regex_utils


class PreviousMarriagesFlagExtractor(BaseExtractor):
    extraction_key = 'previousMarriagesFlag'

    def __init__(self, cursor_location_depends_on=None, options=None):
        super(PreviousMarriagesFlagExtractor, self).__init__(
            cursor_location_depends_on, options
        )
        self.MANY_MARRIAGE_PATTERN = (
            r'toisesta|ensimmäisestä|aikaisemmasta|'
            r'edellisestä|nykyisestä|avioliitosta'
        )

    def _extract(self, entry, extraction_results, extraction_metadata):
        many_marriages = self._check_many_marriages(entry['text'])
        return self._add_to_extraction_results(
            many_marriages, extraction_results, extraction_metadata
        )

    def _check_many_marriages(self, text):
        marriage = regex_utils.search(
            self.MANY_MARRIAGE_PATTERN, text, (re.UNICODE | re.IGNORECASE)
        )
        return marriage is not None

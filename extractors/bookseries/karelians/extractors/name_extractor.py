import re

from extractors.common.extraction_keys import KEYS
from core.pipeline_construction.base_extractor import BaseExtractor
from core.utils.sex_extract import Sex, SexException


class NameExtractor(BaseExtractor):
    """Tries to extract the name of the person in this entry.
    Assumed that it can be found from name attribute from person
    entry.
    """

    extraction_key = 'name'

    def _extract(self, entry, extraction_results, extraction_metadata):
        result = {KEYS['surname']: '', KEYS['firstnames']: ''}

        try:
            result = self._split_names(entry['name'])
        except KeyError:
            self.metadata_collector.add_error_record('nameNotFound', 10)

        try:
            result[KEYS['gender']] = Sex.find_sex(result[KEYS['firstnames']])
        except SexException:
            self.metadata_collector.add_error_record('genderNotFound', 8)
            result[KEYS['gender']] = ''

        return self._add_to_extraction_results(
            result, extraction_results, extraction_metadata
        )

    def _split_names(self, name):
        name = re.sub(r"(?:<|>|&|')", r'', name)
        names = re.split(r'\.|,', name)

        name_results = {KEYS['surname']: names[0].strip(' '), KEYS['firstnames']: ''}

        if len(names) > 1:
            name_results[KEYS['firstnames']] = names[1].strip(' ')
        else:
            self.metadata_collector.add_error_record('nameNotFound', 10)

        return name_results

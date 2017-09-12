from book_extractors.common.extraction_keys import KEYS
from book_extractors.common.extractors.base_extractor import BaseExtractor
from book_extractors.common.extractors.bool_extractor import BoolExtractor
from book_extractors.extraction_pipeline import ExtractionPipeline, configure_extractor


class FarmDetailsExtractor(BaseExtractor):
    """
    Extract information about the farm if there is any information available. Extracted information
    concerns more about the farm rather than any single Persons, but of course persons are related to their farm.

    If all farm details are falsy, return None to denote that no farm details were found.
    """
    extraction_key = 'farmDetails'

    def __init__(self, key_of_cursor_location_dependent, options):
        super(FarmDetailsExtractor, self).__init__(key_of_cursor_location_dependent, options)

        boolean_flag_patterns = {
            KEYS['animalHusbandry']: r'karjataloutta|karjanhoitoa?\b|karjatalous\b'
        }

        self._sub_extraction_pipeline = ExtractionPipeline([
            configure_extractor(BoolExtractor, extractor_options={'patterns': boolean_flag_patterns}),
        ])

    def _extract(self, entry, extraction_results, extraction_metadata):
        results, metadata = self._extract_farm_details(entry['text'])
        return self._add_to_extraction_results(self._get_data_or_none(results), extraction_results, extraction_metadata)

    def _get_data_or_none(self, extracted_data):
        # Check if all farm properties were falsy
        for key, value in extracted_data.items():
            if value:
                return extracted_data
        return None

    def _extract_farm_details(self, text):
        results, metadata = self._sub_extraction_pipeline.process({'text': text})

        # Flatten dict flags out of the result dict:
        flags = results.pop('flags')
        return {**results, **flags}, metadata

from book_extractors.common.extractors.base_extractor import BaseExtractor
from book_extractors.extraction_pipeline import ExtractionPipeline, configure_extractor
from book_extractors.karelians.extraction.extractors.injured_in_war_flag_extractor import InjuredInWarFlagExtractor


class WarDataExtractor(BaseExtractor):
    extraction_key = 'warData'

    def __init__(self, key_of_cursor_location_dependent, options):
        super(WarDataExtractor, self).__init__(key_of_cursor_location_dependent, options)

        self._sub_extraction_pipeline = ExtractionPipeline([
            configure_extractor(InjuredInWarFlagExtractor)
        ])

    def _extract(self, entry, extraction_results, extraction_metadata):
        results, metadata = self._extract_war_data(entry['text'])
        return self._add_to_extraction_results(self._nullify_injured_flag_for_females(results, extraction_results),
                                               extraction_results,
                                               extraction_metadata)

    # FIXME: Dirty post-processing hack to null injuredInWarFlag if the person is female, fix after architecture changes
    def _nullify_injured_flag_for_females(self, extracted_data, extraction_results):
        for key, value in extracted_data.items():
            if value:
                if extraction_results['primaryPerson']['name']['gender'] == 'Female':
                    extracted_data['injuredInWarFlag'] = None

        return extracted_data

    def _extract_war_data(self, text):
        return self._sub_extraction_pipeline.process({'text': text})

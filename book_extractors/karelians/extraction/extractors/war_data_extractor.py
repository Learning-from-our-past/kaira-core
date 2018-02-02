from book_extractors.common.extractors.base_extractor import BaseExtractor


class WarDataExtractor(BaseExtractor):
    extraction_key = 'warData'

    def _extract(self, entry, extraction_results, extraction_metadata):
        results, metadata = self._extract_war_data(entry['text'])
        return self._add_to_extraction_results(results,
                                               extraction_results,
                                               extraction_metadata)

    def _extract_war_data(self, text):
        return self._sub_extraction_pipeline.process({'text': text})

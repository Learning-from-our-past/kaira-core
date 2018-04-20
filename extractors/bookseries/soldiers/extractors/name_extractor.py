from core.pipeline_construction.base_extractor import BaseExtractor


class NameExtractor(BaseExtractor):
    extraction_key = 'name'

    def __init__(self, cursor_location_depends_on=None, options=None):
        super(NameExtractor, self).__init__(cursor_location_depends_on, options)

    def _extract(self, entry, extraction_results, extraction_metadata):
        results = (None, None)
        return self._add_to_extraction_results(results[0], extraction_results, extraction_metadata, results[1])

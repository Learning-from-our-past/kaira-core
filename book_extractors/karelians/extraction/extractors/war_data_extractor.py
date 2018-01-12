from book_extractors.common.extractors.base_extractor import BaseExtractor
from book_extractors.extraction_pipeline import ExtractionPipeline, configure_extractor
from book_extractors.karelians.extraction.extractors.injured_in_war_flag_extractor import InjuredInWarFlagExtractor
from book_extractors.karelians.extraction.extractors.served_during_war_flag_extractor import ServedDuringWarFlagExtractor
from book_extractors.karelians.extraction.extractors.lotta_activity_flag_extractor import LottaActivityFlagExtractor


class WarDataExtractor(BaseExtractor):
    extraction_key = 'warData'

    def __init__(self, cursor_location_depend_on, options, dependencies_contexts=None):
        super(WarDataExtractor, self).__init__(cursor_location_depend_on, options)

        self._sub_extraction_pipeline = ExtractionPipeline([
            configure_extractor(InjuredInWarFlagExtractor,
                                extractor_options={'in_spouse_extractor': options['in_spouse_extractor']},
                                dependencies_contexts=[('main', 'primaryPerson')]),
            configure_extractor(ServedDuringWarFlagExtractor,
                                extractor_options={'in_spouse_extractor': options['in_spouse_extractor']},
                                dependencies_contexts=[('main', 'primaryPerson')]),
            configure_extractor(LottaActivityFlagExtractor,
                                extractor_options={'in_spouse_extractor': options['in_spouse_extractor']},
                                dependencies_contexts=[('main', 'primaryPerson')])
        ])

    def _extract(self, entry, extraction_results, extraction_metadata):
        results, metadata = self._extract_war_data(entry['text'],
                                                   self._get_parent_data_for_pipeline(extraction_results,
                                                                                      extraction_metadata))
        return self._add_to_extraction_results(results,
                                               extraction_results,
                                               extraction_metadata)

    def _extract_war_data(self, text, parent_data):
        return self._sub_extraction_pipeline.process({'text': text}, parent_pipeline_data=parent_data)

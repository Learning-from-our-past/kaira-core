from book_extractors.common.extractors.base_extractor import BaseExtractor
from book_extractors.extraction_pipeline import ExtractionPipeline, configure_extractor
from book_extractors.karelians.extraction.extractors.injured_in_war_flag_extractor import InjuredInWarFlagExtractor
from book_extractors.karelians.extraction.extractors.served_during_war_flag_extractor import ServedDuringWarFlagExtractor
from book_extractors.karelians.extraction.extractors.lotta_activity_flag_extractor import LottaActivityFlagExtractor


class WarDataExtractor(BaseExtractor):
    extraction_key = 'warData'

    def __init__(self, key_of_cursor_location_dependent, options):
        super(WarDataExtractor, self).__init__(key_of_cursor_location_dependent, options)

        exclude = None

        if options is not None and 'exclude_extractors' in options:
            exclude = options['exclude_extractors']

        self._sub_extraction_pipeline = ExtractionPipeline([
            self._configure_extractor(InjuredInWarFlagExtractor, exclude),
            self._configure_extractor(ServedDuringWarFlagExtractor, exclude),
            self._configure_extractor(LottaActivityFlagExtractor, exclude)
        ])

    def _configure_extractor(self, extractor, exclude):
        run_extractor = True
        if exclude is not None:
            run_extractor = extractor not in exclude

        return configure_extractor(extractor, extractor_options={'run_extractor': run_extractor})

    def _extract(self, entry, extraction_results, extraction_metadata):
        results, metadata = self._extract_war_data(entry['text'])
        return self._add_to_extraction_results(self._postprocess_extracted_data(results, extraction_results),
                                               extraction_results,
                                               extraction_metadata)

    def _postprocess_extracted_data(self, extracted_data, extraction_results):
        extracted_data = self._nullify_relevant_flags_for_females(extracted_data, extraction_results)
        extracted_data = self._transfer_lotta_flag_to_spouse_if_male(extracted_data, extraction_results)
        return extracted_data

    # FIXME: Dirty post-processing hack to null injuredInWarFlag and servedDuringWarFlag if the person is female,
    # fix after architecture changes
    def _nullify_relevant_flags_for_females(self, extracted_data, extraction_results):
        if extraction_results['primaryPerson']['name']['gender'] == 'Female':
            extracted_data['injuredInWarFlag'] = None
            extracted_data['servedDuringWarFlag'] = None

        return extracted_data

    def _transfer_lotta_flag_to_spouse_if_male(self, extracted_data, extraction_results):
        if extraction_results['primaryPerson']['name']['gender'] == 'Male':
            flag_holder = extracted_data['lottaActivityFlag']
            extracted_data['lottaActivityFlag'] = None

            if 'spouse' in extraction_results:
                extraction_results['spouse']['lottaActivityFlag'] = flag_holder

        return extracted_data

    def _extract_war_data(self, text):
        return self._sub_extraction_pipeline.process({'text': text})

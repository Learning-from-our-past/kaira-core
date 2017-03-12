import re


class ExtractionPipeline:

    def __init__(self, extractor_configurations):
        self._extractor_configurations = extractor_configurations
        self._extractors = self._build_extraction_pipeline()

    # FIXME: Refactor extractors so that Pipeline is not built for each and every person. Should speed up and save lots of memory
    def _build_extraction_pipeline(self):
        extractors = []

        for config in self._extractor_configurations:
            extractor = config['extractor_class'](key_of_cursor_location_dependent=config['depends_on_match_position_of_extractor'], options=config['extractor_options'])
            extractors.append(extractor)

        return extractors

    def process(self, entry):
        extraction_results = {
            'data': {},
            'cursor_locations': {}
        }

        # Replace all weird invisible white space characters with regular space
        entry['text'] = re.sub(r"\s", r" ", entry['text'])

        for ext in self._extractors:
            extraction_results = ext.extract(entry, extraction_results)

        return extraction_results


def configure_extractor(extractor_class, extractor_options=None, depends_on_match_position_of_extractor=None, set_dependency_match_position_to_zero=False):
    """
    Utility function to build configure dict object for extraction pipeline.
    :param extractor_class:
    :param kwargs_for_extractor: Possible kwargs arguments which can be passed to extractor. Some extractors might need arbitrary extra parametes in their __init__
    :param depends_on_match_position_of_extractor: Extractor class this extractor is dependent on their match position.
    :param set_dependency_match_position_to_zero:
    :return:
    """

    depends_on = None
    if depends_on_match_position_of_extractor is not None:
        depends_on = depends_on_match_position_of_extractor.__class__.__name__

    config = {
        'extractor_class': extractor_class,
        'depends_on_match_position_of_extractor': depends_on,
        'extractor_options': extractor_options
    }

    return config
import re


class ExtractionPipeline:

    def __init__(self, extractor_configurations):
        self._extractor_configurations = extractor_configurations
        self._extractors = self._build_extraction_pipeline()

    def _build_extraction_pipeline(self):
        extractors = []

        for config in self._extractor_configurations:
            extractor = config['extractor_class'](key_of_cursor_location_dependent=config['depends_on_match_position_of_extractor'], options=config['extractor_options'])
            extractors.append(extractor)

        return extractors

    def process(self, entry):
        extraction_output = {}
        extraction_metadata = {}

        # FIXME: This is not really responsibility of this class. Move to some kind of preprocessor instead.
        # Replace invisible whitespace and control characters
        entry['text'] = re.sub(r"\s", r" ", entry['text'])

        for ext in self._extractors:
            extraction_output, extraction_metadata = ext.extract(entry, extraction_output, extraction_metadata)

        return extraction_output, extraction_metadata


def configure_extractor(extractor_class, extractor_options=None, path=None, depends_on_match_position_of_extractor=None):
    """
    Utility function to build configure dict object for extraction pipeline.
    :param extractor_class:
    :param extractor_options: Possible kwargs arguments which can be passed to extractor. Some extractors might need arbitrary extra parametes in their __init__
    :param path: Path of the extractor's results in the dict and json output. Can be used to define parent groups for the output of the extractor.
    :param depends_on_match_position_of_extractor: Extractor class this extractor is dependent on their match position.
    :return:
    """

    depends_on = None
    if depends_on_match_position_of_extractor is not None:
        depends_on = depends_on_match_position_of_extractor.extraction_key

    if extractor_options is not None:
        extractor_options['output_path'] = path
    else:
        extractor_options = {'output_path': path}

    config = {
        'extractor_class': extractor_class,
        'depends_on_match_position_of_extractor': depends_on,
        'extractor_options': extractor_options,
    }

    return config
import re


class ExtractionPipeline:

    def __init__(self, extractors):
        """
        Build the pipeline from either extractor configuration objects or from already
        instantiated extractors. This is a temporary solution to support both YAML-based pipeline
        configuration and old code-based configuration.
        :param extractors:
        :param pass_extractors_directly:
        """

        self._extractors = extractors

    def process(self, entry, parent_pipeline_data=None):
        extraction_output = {}
        extraction_metadata = {}

        # FIXME: This is not really responsibility of this class. Move to some kind of preprocessor instead.
        # Replace invisible whitespace and control characters
        entry['text'] = re.sub(r"\s", r" ", entry['text'])

        for ext in self._extractors:
            extraction_output, extraction_metadata = ext.extract(entry,
                                                                 extraction_output,
                                                                 extraction_metadata,
                                                                 parent_pipeline_data=parent_pipeline_data)

        return extraction_output, extraction_metadata


def configure_extractor(extractor_class, dependencies_contexts=None, extractor_options=None, path=None, depends_on_match_position_of_extractor=None):
    """
    Utility function to build configure dict object for extraction pipeline.
    :param extractor_class:
    :param dependencies_contexts: Used to find the location (pipelinewise) where the extractor or extractors that we
                                  depend on reside. The extractor needs this information to get the extraction results
                                  its operation depends on.
    :param extractor_options: Possible kwargs arguments which can be passed to extractor. Some extractors might need
                              arbitrary extra parametes in their __init__
    :param path: Path of the extractor's results in the dict and json output. Can be used to define parent groups for
                 the output of the extractor.
    :param depends_on_match_position_of_extractor: Extractor class this extractor is dependent on their match position.
    :return:
    """

    depends_on = None
    if depends_on_match_position_of_extractor is not None:
        depends_on = depends_on_match_position_of_extractor

    if extractor_options is not None:
        extractor_options['output_path'] = path
    else:
        extractor_options = {'output_path': path}

    config = {
        'extractor_class': extractor_class,
        'cursor_location_depend_on': depends_on,
        'extractor_options': extractor_options,
        'dependencies_contexts': dependencies_contexts
    }

    return config

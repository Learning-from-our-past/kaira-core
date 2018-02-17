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

        # Some pipelines might be provided only sub text of the whole text while some extractors in the pipeline
        # might need the whole text. So make sure one is available always.
        if 'full_text' in entry:
            entry['full_text'] = re.sub(r"\s", r" ", entry['full_text'])
        else:
            entry['full_text'] = entry['text']

        for ext in self._extractors:
            extraction_output, extraction_metadata = ext.extract(entry,
                                                                 extraction_output,
                                                                 extraction_metadata,
                                                                 parent_pipeline_data=parent_pipeline_data)

        return extraction_output, extraction_metadata

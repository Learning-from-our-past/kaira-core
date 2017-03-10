import re


class ExtractionPipeline:

    def __init__(self, extractor_configurations):
        self._extractor_configurations = extractor_configurations

    def _find_extractor_by_class_name(self, class_to_find, extractors):
        return next(e for e in extractors if type(e).__name__ == class_to_find.__name__)

    # FIXME: Refactor extractors so that Pipeline is not built for each and every person. Should speed up and save lots of memory
    def _build_extraction_pipeline(self, entry):
        extractors = []

        for config in self._extractor_configurations:
            extractor = config['extractor_class'](entry, config['extractor_options'])
            extractors.append(extractor)

        return extractors

    def process(self, entry):
        extractors = self._build_extraction_pipeline(entry)
        extraction_results = {}

        # Replace all weird invisible white space characters with regular space
        entry['text'] = re.sub(r"\s", r" ", entry['text'])

        for ext in zip(self._extractor_configurations, extractors):
            # FIXME: Because of how current implementation of extractors, these functions has to be called here. Not ideal.
            # Instead figure out a way to save match positions to pipeline level outside of extractor class and make extractors stateless.
            # This way we could possibly get rid of reflection and set kind of symbol table to pipeline level where extractors could check
            # the match locations of others when required.
            if ext[0]['set_dependency_match_position_to_zero']:
                ext[1].setDependencyMatchPositionToZero()

            if ext[0]['depends_on_match_position_of_extractor'] is not None:
                dependency_extractor = self._find_extractor_by_class_name(ext[0]['depends_on_match_position_of_extractor'], extractors)
                ext[1].dependsOnMatchPositionOf(dependency_extractor)

            extraction_results.update(ext[1].extract(entry['text'], entry))

        extraction_results["originalText"] = entry['text']  #FIXME: Make own extractor for this. Not a responsibility of this class.
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
    config = {
        'extractor_class': extractor_class,
        'set_dependency_match_position_to_zero': set_dependency_match_position_to_zero,
        'depends_on_match_position_of_extractor': depends_on_match_position_of_extractor,
        'extractor_options': extractor_options
    }

    return config
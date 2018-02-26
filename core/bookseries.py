import os
from core.utils.gender_extract import Gender
from core.dependency_resolver import ExtractorResultsMap
from core.yaml_parser import YamlParser
from core.processdata import ProcessData


class BookSeries:
    """
    A class which wraps all logic of the bookseries to a common interface. Gives access to the
    extraction, chunking etc. operations. Actual implementation of said operations are in plugins. This class
    just holds references to them.
    """

    def __init__(self, manifest, update_callback):
        Gender.load_names()
        self._manifest = manifest
        self._extraction_result_map = ExtractorResultsMap()
        self._parser = YamlParser(self._extraction_result_map)
        self._extractor_pipeline = self._parser.build_pipeline_from_yaml(os.path.join(manifest['path'], 'config.yaml'))
        self._extractor = ProcessData(self._extractor_pipeline, self._extraction_result_map, update_callback)
        self._results = None

    def _xml_to_extractor_format(self, xml_document):
        """
        Transform xml file to dict format. Pick all attributes available in the entry and add text
        properties.
        :param xml_document:
        :return:
        """

        return [{**child.attrib, 'text': child.text, 'full_text': child.text} for child in xml_document]

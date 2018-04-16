import os
from importlib import util as import_util

from core.resultjsonbuilder import ResultJsonBuilder
from core.utils.sex_extract import Sex
from core.pipeline_construction.dependency_resolver import ExtractorResultsMap
from core.pipeline_construction.yaml_parser import YamlParser
from core.processdata import ProcessData


class BookSeries:
    """
    A class which wraps all logic of the bookseries to a common interface. Gives access to the
    extraction, chunking etc. operations. Actual implementation of said operations are in plugins. This class
    just holds references to them.
    """

    def __init__(self, manifest, update_callback):
        Sex.load_names()
        self._manifest = manifest
        self._extraction_result_map = ExtractorResultsMap()
        self._parser = YamlParser(self._extraction_result_map)

        self._extractor_pipeline = None
        self._extractor = None
        self._results = None
        self._update_callback = update_callback

    def extract_data(self, data_xml):
        self._extractor_pipeline = self._parser.build_pipeline_from_yaml(os.path.join(self._manifest['path'],
                                                                                      'config.yaml'))
        self._extractor = ProcessData(self._extractor_pipeline, self._extraction_result_map, self._update_callback)

        person_data = self._xml_to_extractor_format(data_xml)
        self._results = self._extractor.run_extraction(person_data)

    def save_results(self, file, file_format='json'):
        if file_format == 'json':
            writer = ResultJsonBuilder()
            writer.open_json(file)

            for entry in self._results['entries']:
                try:
                    writer.write_entry(entry['extractionResults'][0])    # Leave metadata objects out
                except KeyError as e:
                    raise e

            writer.close_json()

    def chunk(self, input_files, output_files, book_numbers, filter_duplicates=False, callback=None):
        # Import the chunking implementation from the plugin directory
        chunking_spec = import_util.spec_from_file_location('chunktextfile',
                                                            os.path.join(
                                                                self._manifest['path'],
                                                                self._manifest['chunker']))
        chunking_module = import_util.module_from_spec(chunking_spec)
        chunking_spec.loader.exec_module(chunking_module)

        # And then call the actual implementation in the imported module
        chunking_module.convert_html_file_to_xml(
            self._manifest['book_series_id'],
            input_files,
            output_files,
            book_numbers,
            filter_duplicates,
            callback
        )

    def _xml_to_extractor_format(self, xml_document):
        """
        Transform xml file to dict format. Pick all attributes available in the entry and add text
        properties.
        :param xml_document:
        :return:
        """

        return [{**child.attrib, 'text': child.text, 'full_text': child.text} for child in xml_document]

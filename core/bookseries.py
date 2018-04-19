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
        self._bookseries_clean_up_entry_fn = self._load_clean_up_function()

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

    def transform_xml_data_for_fdp(self, xml_doc):
        """
        Transforms a book's entries to prepare them for fin-dep-parser.

        If the quality of the text being parsed by the fin-dep-parser is not perfect, it
        may need some clean up that will help the parser better cope with the text without
        making errors. Any errors in the text could have bigconsequences to how the parser
        interprets an entire sentence. Simple clean-up can improve it considerably so it
        does not confuse the NLP parser.

        The data is placed in a .txt file with comments that keep the entries clearly separated
        from each other. It takes a while to start the parser and doing so for each entry
        individually is unfeasible, so we want to process them all in one go.
        :param xml_doc: An XML document opened with e.g. lxml.etree.parse
        :return: String containing path to outputted file with transformed text
        """
        xml_root = xml_doc.getroot()

        transformed_data = []
        for idx, child in enumerate(xml_root):
            raw = child.find('RAW')
            entry = self._clean_up_entry_for_nlp(raw)
            entry = '###C: {{\'entry_num\': {}}}\n{}'.format(idx, entry)
            transformed_data.append(entry)

        return transformed_data

    def _clean_up_entry_for_nlp(self, entry):
        """
        Cleans up an entry from a book in a bookseries. Default implementation in the
        framework is not to do any clean up at all. Setting the 'nlp_clean_up' key in
        the manifest to a value that specifies the location of a file containing a
        function called "clean_up_entry" with the same signature as this function has
        (excluding self) will make this function call that function for clean up instead.

        What the clean up actually is is completely determined by the plugin itself, but
        common clean up operations may include identifying patterns in the text that the
        fin-dep-parser has trouble interpreting, and transforming those into something
        more palatable for the parser, using simple regular expression replacements.
        For example, "mm." can mean either "muun muassa", in which case the parser will
        not interpret the dot following "mm" to terminate the sentence. But it can also
        mean "muistomitali" followed by a dot signifying the termination of a sentence.
        Writing a regular expression to disambiguate the occurrences of "mm." can
        significantly improve the quality of the parser's output.
        :param entry: Entry from book in bookseries
        :return: Cleaned up entry
        """
        if self._bookseries_clean_up_entry_fn is not None:
            return self._bookseries_clean_up_entry_fn(entry)
        else:
            return entry

    def _load_clean_up_function(self):
        clean_up_module_path = self._manifest.get('nlp_clean_up', None)
        if clean_up_module_path is not None:
            return self._load_plugin_module('clean_up', clean_up_module_path).clean_up_entry
        return None

    def _load_plugin_module(self, module_name, file):
        module_spec = import_util.spec_from_file_location(module_name,
                                                          os.path.join(
                                                              self._manifest['path'],
                                                              file))
        module = import_util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)
        return module

    def _xml_to_extractor_format(self, xml_document):
        """
        Transform xml file to dict format. Pick all attributes available in the entry and add text
        properties.
        :param xml_document:
        :return:
        """

        return [{**child.attrib, 'text': child.text, 'full_text': child.text} for child in xml_document]

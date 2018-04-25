import os
from importlib import util as import_util

from core.resultjsonbuilder import ResultJsonBuilder
from core.utils.sex_extract import Sex
from core.pipeline_construction.dependency_resolver import ExtractorResultsMap
from core.pipeline_construction.yaml_parser import YamlParser
from core.processdata import ProcessData
from core.nlp.parsing.transform_xml import run_xml_data_transformation
from core.nlp.parsing.parse_with_fdp import parse_through_fdp_and_output_file
from core.nlp.parsing.join_nlp_data_to_xml import add_conllu_data_to_xml
from conllu import parser


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
        self._custom_convert_xml_to_dict = self._load_custom_xml_conversion_function()

    def extract_data(self, xml_stream):
        self._extractor_pipeline = self._parser.build_pipeline_from_yaml(os.path.join(self._manifest['path'],
                                                                                      'config.yaml'))
        self._extractor = ProcessData(self._extractor_pipeline, self._extraction_result_map, self._update_callback)

        self._results = self._extractor.run_extraction(xml_stream)

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
        chunking_module = self._load_plugin_module('chunktextfile', self._manifest['chunker'])

        # And then call the actual implementation in the imported module
        chunking_module.convert_html_file_to_xml(
            self._manifest['book_series_id'],
            input_files,
            output_files,
            book_numbers,
            filter_duplicates,
            callback
        )

    def parse_with_nlp(self, xml_doc, base_path, output_file, clean_up):
        print('Transforming data...')
        transformed_file_path = run_xml_data_transformation(self, xml_doc, base_path)

        print('Running transformed data through fin-dep-parser...')
        nlp_data_file = parse_through_fdp_and_output_file(transformed_file_path, base_path)
        if clean_up:
            os.remove(transformed_file_path)

        print('Joining NLP data to XML file with the original data...')
        output_path = add_conllu_data_to_xml(xml_doc, nlp_data_file, output_file)
        if clean_up:
            os.remove(nlp_data_file)

        print('Done! XML file with NLP data created: {}'.format(output_path))

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

    def convert_xml_to_dict(self, person_element):
        """
        Transform xml person element to dict format. Pick all attributes available in the
        entry and add text properties from <RAW> and <CONLLU> if it is available.

        This can be overridden for specific bookseries with a customized xml conversion
        function by setting up the key "xml_to_dict" in the manifest file of a bookseries
        and setting the value of that key to the path to a file which contains a function
        with the name "convert_xml_to_dict".

        :param person_element: A <PERSON>...</PERSON> element from the XML
        :return: dict with data from XML mapped
        """
        if self._custom_convert_xml_to_dict is not None:
            return self._custom_convert_xml_to_dict(person_element)

        person_entry = {**person_element.attrib,
                        'text': person_element.find('RAW').text}

        conllu_data = BookSeries._get_conllu_data_from_xml(person_element)
        if conllu_data is not None:
            person_entry['conllu'] = conllu_data

        person_entry['full_text'] = person_entry['text']

        return person_entry

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

    @staticmethod
    def _get_conllu_data_from_xml(element):
        conllu = element.find('CONLLU')
        if conllu is not None:
            conllu = parser.parse(conllu.text)

        return conllu

    def _load_custom_xml_conversion_function(self):
        """
        Loads a customized function for converting XML person entries to extractor dict
        format.
        :param xml_to_dict: Path to file containing convert_xml_to_dict function, relative
        to the location of the manifest file
        :return: convert_xml_to_dict function from file specified by xml_to_dict
        """
        xml_to_dict_module_path = self._manifest.get('xml_to_dict', None)
        if xml_to_dict_module_path is None:
            return None
        xml_conversion_module = self._load_plugin_module('xml_to_dict', xml_to_dict_module_path)
        return xml_conversion_module.convert_xml_to_dict

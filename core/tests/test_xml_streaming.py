from core.streaming_xml_reader import StreamingXMLReader
from core.tests.mock_data.mock_streaming_xml import *


def basic_xml_to_extractor(person_element):
    return {**person_element.attrib, 'text': person_element.find('RAW').text}


class TestStreamingXMLReader:
    def should_stream_basic_xml_with_one_element_correctly(self):
        reader = StreamingXMLReader(
            mock_file(XML_WITH_SIMPLE_PERSON_ENTRIES),
            basic_xml_to_extractor,
            chunk_size=2,
        )
        entries = [entry for entry in reader.read_entry_from_xml()]

        assert entries[0]['text'] == 'foo'
        assert entries[0]['name'] == 'TESTIKÄS, TESTAAJA'
        assert entries[1]['text'] == 'bar'
        assert entries[1]['name'] == 'TOINEN, TESTERI'

    def should_stream_xml_with_multiple_elements_correctly(self):
        def xml_to_extractor(person_element):
            _raw, _conllu = person_element
            return {**person_element.attrib, 'raw': _raw.text, 'conllu': _conllu.text}

        reader = StreamingXMLReader(
            mock_file(XML_WITH_COMPLEX_PERSON_ENTRIES), xml_to_extractor, chunk_size=2
        )
        entries = [entry for entry in reader.read_entry_from_xml()]

        expected_data = (
            ('TESTIKÄS, TESTAAJA', ('foo', 'fooconllu')),
            ('TOINEN, TESTERI', ('bar', 'barconllu')),
        )

        for entry, (name, (raw, conllu)) in zip(entries, expected_data):
            assert entry['name'] == name
            assert entry['raw'] == raw
            assert entry['conllu'] == conllu

    def should_correctly_stream_data_when_number_of_entries_is_greater_than_chunk_size(
        self,
    ):
        reader = StreamingXMLReader(
            mock_file(XML_WITH_SIMPLE_PERSON_ENTRIES),
            basic_xml_to_extractor,
            chunk_size=1,
        )
        entries = [entry for entry in reader.read_entry_from_xml()]
        expected_len = XML_WITH_SIMPLE_PERSON_ENTRIES.count('<PERSON')
        assert len(entries) == expected_len

    def should_correctly_stream_data_when_number_of_entries_is_lesser_thank_chunk_size(
        self,
    ):
        reader = StreamingXMLReader(
            mock_file(XML_WITH_SIMPLE_PERSON_ENTRIES),
            basic_xml_to_extractor,
            chunk_size=100,
        )
        entries = [entry for entry in reader.read_entry_from_xml()]
        expected_len = XML_WITH_SIMPLE_PERSON_ENTRIES.count('<PERSON')
        assert len(entries) == expected_len

    def should_correctly_stream_data_when_chunk_size_is_not_a_multiple_of_number_of_entries(
        self,
    ):
        reader = StreamingXMLReader(
            mock_file(XML_WITH_MANY_SIMPLE_PERSON_ENTRIES),
            basic_xml_to_extractor,
            chunk_size=3,
        )
        entries = [entry for entry in reader.read_entry_from_xml()]
        expected_len = XML_WITH_MANY_SIMPLE_PERSON_ENTRIES.count('<PERSON')
        assert len(entries) == expected_len

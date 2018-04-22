from lxml import etree


class StreamingXMLReader:
    def __init__(self, input_file, convert_xml_to_dict, chunk_size=100, encoding='utf8'):
        """
        A class for streaming person entries from an XML file.
        :param input_file: String, path to file to stream person entries from
        :param convert_xml_to_dict: Function used to turn XML elements into person entries
        :param chunk_size: Number of person entries to read at a time
        :param encoding: Encoding to open file with
        """
        self._xml_file = etree.iterparse(input_file, encoding=encoding)
        self._convert_xml_to_dict = convert_xml_to_dict
        self._chunk_size = chunk_size

    def read_entry_from_xml(self):
        """
        Streams data from XML file, in the person data format that the extractor expects.
        """
        for chunk in self._read_chunk():
            for entry in chunk:
                yield entry

    def _read_chunk(self):
        """
        Reads data from the XML file till there are enough person entries to constitute a
        chunk, then yields the chunk.
        :return: A list of data entries in the current chunk
        """
        current_chunk = []
        for event, element in self._xml_file:
            if element.tag.casefold() == 'person':
                entry_data = self._convert_xml_to_dict(element)
                current_chunk.append(entry_data)
                # Clears the contents of element. This is needed because while etree.iterparse does
                # essentially stream elements from the XML one by one, it still builds the element
                # tree in memory as it does its thing. If we clear the elements in memory after they
                # are no longer needed, we save that memory.
                element.clear()

            if len(current_chunk) == self._chunk_size:
                yield current_chunk
                current_chunk.clear()
        yield current_chunk
        raise StopIteration

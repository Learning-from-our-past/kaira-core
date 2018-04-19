from lxml.html import *
from lxml import etree
from lxml import html
import re
from core.interface.chunktextinterface import ChunkTextInterface


def read_html_file(path):
    return parse(path)


class PersonPreprocessor(ChunkTextInterface):
    def __init__(self, bookseries_id):
        super(PersonPreprocessor, self).__init__(bookseries_id)
        self._save_path = None
        self._book_number = None
        self._persons_document = None
        self._page_number = None
        self._current_person = None

    def chunk_text(self, text, destination_path, book_number):
        self._save_path = destination_path
        self._book_number = book_number
        text = re.sub(r'(\<sup\>)|\<\/sup\>', '', text)
        parsed = html.document_fromstring(text)
        persons = self._process(parsed)
        return etree.tostring(persons, pretty_print=True, encoding='unicode')

    def _process(self, tree):
        self._persons_document = etree.Element('DATA')
        self._persons_document.attrib['bookseries'] = self._bookseries_id
        self._persons_document.attrib['book_number'] = str(self._book_number)
        self._current_person = None
        self._page_number = 1

        person_document = self._walk_tree(tree)
        return person_document

    def _walk_tree(self, tree):
        for e in tree.iter():
            if e.text is not None:
                print(e.text)



def convert_html_file_to_xml(bookseries_id, input_file, output_file, book_number, filter_duplicates=False, callback=None):
    text = input_file[0].read()
    p = PersonPreprocessor(bookseries_id)
    persons = p.chunk_text(text, output_file[0].name, book_number[0])
    output_file[0].write(persons)
    output_file[0].close()
    print('File converted to xml and saved!')

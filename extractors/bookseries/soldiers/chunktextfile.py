from lxml.html import *
from lxml import etree
from lxml import html
import re
from core.interface.chunktextinterface import ChunkTextInterface


def read_html_file(path):
    return parse(path)


class PersonPreprocessor(ChunkTextInterface):
    """
    This is a proof of concept chunker and therefore is not optimized to handle all corner cases which
    will appear in ABBYY html-files such as cases where another person entry begins "inside" previous
    person's entry.
    """

    def __init__(self, bookseries_id):
        super(PersonPreprocessor, self).__init__(bookseries_id)
        self._save_path = None
        self._book_number = None
        self._persons_document = None
        self._page_number = None
        self._current_person = None
        self._current_person_raw = None

        # A regex which is used to identify <p> tag which begins a new person entry. extremely naive since it
        # just assumes that if the tag begins with three uppercase letters, the paragraph begins a new entry.
        self._ENTRY_BEGINS_REGEX = re.compile(r'^[A-ZÄÖ]{3,}', re.UNICODE)

    def chunk_text(self, text, destination_path, book_number):
        self._save_path = destination_path
        self._book_number = book_number
        text = re.sub(r'(<sup>)|</sup>', '', text)
        text = re.sub(r'&nbsp;', ' ', text)
        parsed = html.document_fromstring(text)
        persons = self._process(parsed)
        return etree.tostring(persons, pretty_print=True, encoding='unicode')

    def _process(self, tree):
        self._persons_document = etree.Element('DATA')
        self._persons_document.attrib['bookseries'] = self._bookseries_id
        self._persons_document.attrib['book_number'] = str(self._book_number)
        self._current_person = None
        self._current_person_raw = None
        self._page_number = 1

        person_document = self._walk_tree(tree)
        return person_document

    def _walk_tree(self, tree):
        for e in tree.iter():
            if 'src' in e.attrib:
                # We are not interested in images for now
                continue

            if e.text is not None:
                try:
                    self._page_number = int(e.text)
                except ValueError:
                    if self._ENTRY_BEGINS_REGEX.search(e.text) is not None:
                        self._add_person(self._current_person)
                        self._current_person = self._create_person(e.text)
                        self._current_person_raw = self._current_person.find('RAW')
                    elif self._current_person is not None:
                        self._add_element_to_person(e)

        self._add_person(self._current_person)
        return self._persons_document

    def _add_element_to_person(self, e):
        if len(e.text) > 40:
            # TODO: Here we could try to identify person entries which begin midst of the current person entry
            # See a reference implementation in siirtokarjalaisten tie chunker

            # For now just concatenate the element's text to the current person
            self._current_person_raw.text += e.text
            self._current_person_raw.text = re.sub(
                '\n', ' ', self._current_person_raw.text
            )
            self._current_person_raw.text = re.sub(
                '\s{2,4}', ' ', self._current_person_raw.text
            )

    def _create_person(self, entry):
        person = etree.Element('PERSON')
        person.attrib['approximated_page'] = '{}-{}'.format(
            self._page_number - 1, self._page_number + 1
        )
        raw = etree.Element('RAW')
        raw.text = entry
        person.append(raw)
        return person

    def _add_person(self, person):
        if person is not None and len(person.find('RAW').text) > 4:
            self._persons_document.append(person)


def convert_html_file_to_xml(
    bookseries_id,
    input_file,
    output_file,
    book_number,
    filter_duplicates=False,
    callback=None,
):
    text = input_file[0].read()
    p = PersonPreprocessor(bookseries_id)
    persons = p.chunk_text(text, output_file[0].name, book_number[0])
    output_file[0].write(persons)
    output_file[0].close()
    print('File converted to xml and saved!')

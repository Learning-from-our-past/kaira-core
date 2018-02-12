import regex
from copy import deepcopy
from lxml import etree as ET
import argparse
import sys

"""
Use a file that contains newline separated KairaIDs to generate an XML file
with the person entries corresponding to those KairaIDs. This tool is meant
to be used directly from a CLI. It is possible to utilize this class in your
code, but it will just take the input in the form of a text file and place the
output in an .xml file. The constructor contains all the interesting settings
that need to be configured, after that it's just a call to the function 
make_xml_file_from_kairaids.

This script will get both primary people and spouses, as in the case of spouses
it will fetch the primary person entry that the spouse's data is gathered from.
As such, you may end up with "duplicates" in your XML files, even though in
reality they come from different KairaIDs.
"""


class KairaID2XML:
    # TODO: Add a setting and code to omit spouses.
    def __init__(self, input_file=None, output_file=None, book_paths=None):
        if input_file is None:
            print('Input file has to be specified!')
            sys.exit(1)
        elif output_file is None:
            print('Output file has to be specified!')
            sys.exit(1)
        elif book_paths is None:
            print('Book paths have to be specified!')
            sys.exit(1)

        self._input_file = input_file
        self._output_file = output_file
        self._books = []

        for book_path in book_paths:
            self._books.append(self.open_xml_file(book_path))

        kairaid_regex_pattern = r'_(?P<book_number>\d)_(?P<entry_number>\d+)'
        self._kairaid_regex = regex.compile(kairaid_regex_pattern,
                                            regex.UNICODE | regex.IGNORECASE)

    @staticmethod
    def open_xml_file(book_path):
        xml_doc = ET.parse('{}'.format(book_path))
        return xml_doc.getroot()

    def _get_xml_entry_by_kairaid(self, kairaid):
        matches = self._kairaid_regex.search(kairaid)
        book_num = int(matches.group('book_number')) - 1
        entry_num = int(matches.group('entry_number')) - 1

        entry = deepcopy(self._books[book_num][entry_num])

        return book_num, entry

    def make_xml_file_from_kairaids(self):
        ids_file = open(self._input_file, 'r', encoding='utf-8')

        book = ET.Element('DATA')
        book.attrib['bookseries'] = 'siirtokarjalaiset'
        book.attrib['book_number'] = '1'

        for kairaid in ids_file:
            book_num, entry = self._get_xml_entry_by_kairaid(kairaid)
            book.append(entry)

        output_file = open(self._output_file, 'w', encoding='utf-8')
        output_file.write(ET.tostring(book,
                                      encoding='unicode',
                                      pretty_print=True))
        output_file.close()
        ids_file.close()


parser = argparse.ArgumentParser()
parser.add_argument('-input', help='The input file with the KairaIDs.',
                    type=str)
parser.add_argument('-output', help='The output file to store the XML in.')
parser.add_argument('-books', nargs='*', help='The books used for finding the entries corresponding to the KairaIDs.')
args = parser.parse_args()

xml_maker = KairaID2XML(input_file=args.input,
                        output_file=args.output,
                        book_paths=args.books)
xml_maker.make_xml_file_from_kairaids()

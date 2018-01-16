import sys
import os
import subprocess
import argparse
import re
import shutil
from lxml import etree
from book_extractors.karelians.main import KarelianBooksExtractor, get_karelian_data_entry, BOOK_SERIES_ID as KARELIAN_BOOK_ID
import book_extractors.karelians.chunktextfile as karelian_converter
from book_extractors.farmers.main import SmallFarmersBooksExtractor, get_small_farmers_data_entry, BOOK_SERIES_ID as SMALL_FARMERS_BOOK_ID
import book_extractors.farmers.chunktextfile as small_farmers_converter
from book_extractors.greatfarmers.main import GreatFarmersBooksExtractor, get_great_farmers_data_entry, BOOK_SERIES_ID as GREAT_FARMERS_BOOK_ID
import book_extractors.greatfarmers.chunktextfile as great_farmers_converter
import book_extractors.extraction_constants as extraction_constants

supported_bookseries = {
    KARELIAN_BOOK_ID: {'extractor': KarelianBooksExtractor, 'converter': karelian_converter.convert_html_file_to_xml},
    SMALL_FARMERS_BOOK_ID: {'extractor': SmallFarmersBooksExtractor, 'converter': small_farmers_converter.convert_html_file_to_xml},
    GREAT_FARMERS_BOOK_ID: {'extractor': GreatFarmersBooksExtractor, 'converter': great_farmers_converter.convert_html_file_to_xml}
}

help_str = 'Bookseries where data is from: {}'.format(', '.join(list(supported_bookseries.keys())))
progress_str = 'Progress: {}% - {}/{}'
progress_bar_str = '{} [{}{}] \r'

parser = argparse.ArgumentParser(description='Extract information from matrikel books.')
parser.add_argument('-i', nargs='?', type=argparse.FileType('r', encoding='utf8'), help='Input file to extract data from. Should be XML.', default=None)
parser.add_argument('-o', nargs='*', type=argparse.FileType('w', encoding='utf8'), help='Output file to save data to.', default=None, )
parser.add_argument('-c', nargs='*', type=argparse.FileType('r', encoding='utf8'), help='Input file to transform into analyzable XML file.', default=None)
parser.add_argument('-b', nargs='?', type=str, help=help_str, default=None)
parser.add_argument('-n', nargs='*', type=int, help='Number of book in series', default=None)
parser.add_argument('--filter', action='store_true', help='Whether to delete duplicates.')

def callback(current, max):
    percentage = round((current / max) * 100)
    progress_bar = progress_str.format(percentage, current, max)
    console_width = int(shutil.get_terminal_size()[0] / 2)
    bar_width = console_width - len(progress_bar)
    bar_fill = round(percentage * bar_width / 100)
    progress_bar = progress_bar_str.format(progress_bar, '#' * bar_fill, '-' * (bar_width - bar_fill))
    sys.stdout.write(progress_bar)
    sys.stdout.flush()

def xml_to_extractor_format(xml_document):
    """
    Transform xml file to dict format. This could be skipped if person raw data were saved as
    json not in xml...
    :param xml_document:
    :return:
    """
    book_series = xml_document.attrib["bookseries"]

    persons = []

    if book_series == KARELIAN_BOOK_ID:
        for child in xml_document:
            if 'img_path' in child.attrib:
                path = child.attrib['img_path']
            else:
                path = ''
            persons.append(get_karelian_data_entry(child.attrib["name"], child.attrib['approximated_page'], child.text, path))
    elif book_series == SMALL_FARMERS_BOOK_ID:
        for child in xml_document:
            persons.append(get_small_farmers_data_entry(child.attrib["name"], child.attrib["location"], child.attrib['approximated_page'], child.text))
    elif book_series == GREAT_FARMERS_BOOK_ID:
        for child in xml_document:
            persons.append(get_great_farmers_data_entry(child.attrib["name"], child.attrib["location"], child.attrib['approximated_page'], child.text))

    return persons


def extract(args):
    input_file = args['i']
    output_files = args['o']
    xml_parser = etree.XMLParser(encoding="utf8")
    xml_document = etree.parse(input_file, parser=xml_parser).getroot()
    book_series = xml_document.attrib["bookseries"]
    extraction_constants.BOOK_NUMBER = xml_document.attrib["book_number"]
    extraction_constants.BOOK_SERIES = book_series

    if book_series not in supported_bookseries:
        print('Error: Provided book series is not supported.')
        sys.exit(1)

    print('Book series:', book_series)
    extractor = supported_bookseries[book_series]['extractor'](callback)
    extractor.process(xml_to_extractor_format(xml_document))
    extractor.save_results(output_files[0], file_format='json')
    print('Process finished successfully.')


def chunk(args):
    book_series = args['b']
    input_files = args['c']
    output_files = args['o']
    book_numbers = args['n']

    if book_series is None or book_numbers is None:
        print('Error: Both book series argument and book number in series should be provided when starting conversion process. Example: -b siirtokarjalaiset -n 1')
        raise CommandLineParameterException()

    if book_series not in supported_bookseries:
        print('Error: Provided book series is not supported. Try one from', ', '.join(list(supported_bookseries.keys())))
        raise CommandLineParameterException()

    if output_files is None:
        print('Error: Both input file and the output file should be provided.')
        raise CommandLineParameterException()

    if len(output_files) != len(input_files) or len(output_files) != len(book_numbers):
        print('Error: The number of files to chunk should match the number of output files and the number of book numbers.')
        raise CommandLineParameterException()

    print('Converting...')
    supported_bookseries[book_series]['converter'](
        input_files,
        output_files,
        book_numbers,
        filter_duplicates=args['filter'],
        callback=callback
    )


def main():
    args = vars(parser.parse_args())

    if args['c'] is not None:
        try:
            chunk(args)
        except CommandLineParameterException:
            sys.exit(1)
    else:
        extract(args)


class CommandLineParameterException(Exception):
    pass

if __name__ == '__main__':
    main()

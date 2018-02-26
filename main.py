import sys
import argparse
import shutil
from lxml import etree
import core.extraction_constants as extraction_constants
from core import bootstrap

PLUGIN_DIRECTORY = './book_extractors'
AVAILABLE_BOOKSERIES = tuple(series['book_series_id'] for series in bootstrap.find_available_bookseries_from_directory(PLUGIN_DIRECTORY))


help_str = 'Bookseries where data is from: {}'.format(', '.join(AVAILABLE_BOOKSERIES))
progress_str = 'Progress:{:>4}% - {:>5}/{:>5}'
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


def extract(args):
    input_file = args['i']
    output_files = args['o']
    xml_parser = etree.XMLParser(encoding="utf8")
    xml_document = etree.parse(input_file, parser=xml_parser).getroot()
    bookseries_id = xml_document.attrib["bookseries"]

    try:
        bookseries = bootstrap.setup_extraction_framework_for_bookseries(bookseries_id,
                                                                            './book_extractors',
                                                                            callback)
    except bootstrap.BookSeriesNotSupportedException as err:
        print(err)
        sys.exit(1)

    extraction_constants.BOOK_NUMBER = xml_document.attrib['book_number']
    extraction_constants.BOOK_SERIES = bookseries_id

    print('Book series:', bookseries_id)
    bookseries.extract_data(xml_document)
    bookseries.save_results(output_files[0], file_format='json')
    print('Process finished successfully.')


def chunk(args):
    bookseries_id = args['b']
    input_files = args['c']
    output_files = args['o']
    book_numbers = args['n']

    if bookseries_id is None or book_numbers is None:
        print('Error: Both book series argument and book number in series should be provided when starting '
              'conversion process. Example: -b siirtokarjalaiset -n 1')
        raise CommandLineParameterException()

    if output_files is None:
        print('Error: Both input file and the output file should be provided.')
        raise CommandLineParameterException()

    if len(output_files) != len(input_files) or len(output_files) != len(book_numbers):
        print('Error: The number of files to chunk should match the number of output '
              'files and the number of book numbers.')
        raise CommandLineParameterException()

    try:
        bookseries = bootstrap.setup_extraction_framework_for_bookseries(bookseries_id,
                                                                            './book_extractors',
                                                                            callback)
    except bootstrap.BookSeriesNotSupportedException:
        print('Error: Provided book series is not supported. Try one from',
              ', '.join(AVAILABLE_BOOKSERIES))
        raise CommandLineParameterException()

    print('Converting...')
    bookseries.chunk(input_files,
                     output_files,
                     book_numbers,
                     filter_duplicates=args['filter'],
                     callback=callback)


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

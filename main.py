import sys
import argparse
import regex
import core.extraction_constants as extraction_constants
from core import bootstrap
from core.nlp.parsing.run_nlp_parsing import run_nlp_parsing
from core.streaming_xml_reader import StreamingXMLReader

PLUGIN_DIRECTORY = './extractors/bookseries'
AVAILABLE_BOOKSERIES = tuple(
    series['book_series_id']
    for series in bootstrap.find_available_bookseries_from_directory(PLUGIN_DIRECTORY)
)

help_str = 'Bookseries where data is from: {}'.format(', '.join(AVAILABLE_BOOKSERIES))
progress_fmt = 'Processing entry {}\r'

parser = argparse.ArgumentParser(description='Extract information from matrikel books.')
parser.add_argument(
    '-i',
    nargs='?',
    type=argparse.FileType('r', encoding='utf8'),
    help='Input file to extract data from. Should be XML.',
    default=None,
)
parser.add_argument(
    '-o',
    nargs='*',
    type=argparse.FileType('w', encoding='utf8'),
    help='Output file to save data to.',
    default=None,
)
parser.add_argument(
    '-c',
    nargs='*',
    type=argparse.FileType('r', encoding='utf8'),
    help='Input file to transform into analyzable XML file.',
    default=None,
)
parser.add_argument(
    '-t', nargs='?', type=str, help='Input file to tag with NLP data.', default=None
)
parser.add_argument('-b', nargs='?', type=str, help=help_str, default=None)
parser.add_argument(
    '-n', nargs='*', type=int, help='Number of book in series', default=None
)
parser.add_argument(
    '--filter', action='store_true', help='Whether to delete duplicates.'
)
parser.add_argument(
    '--no-clean-up',
    action='store_true',
    help='Do not clean up files after NLP tagging',
    default=False,
)


def callback(current):
    progress = progress_fmt.format(current)
    sys.stdout.write(progress)
    sys.stdout.flush()


def read_bookseries_header(file):
    first_line = file.readline()
    bookseries_match = regex.search(
        r'bookseries="(?P<bookseries_id>\w+)"[\s>]', first_line, flags=regex.UNICODE
    )
    booknumber_match = regex.search(
        r'book_number="(?P<book_number>\w+)"[\s>]', first_line, flags=regex.UNICODE
    )
    return bookseries_match.group('bookseries_id'), booknumber_match.group(
        'book_number'
    )


def extract(args):
    input_file = args['i']
    output_files = args['o']
    bookseries_id, book_number = read_bookseries_header(input_file)

    try:
        bookseries = bootstrap.setup_extraction_framework_for_bookseries(
            bookseries_id, PLUGIN_DIRECTORY, callback
        )
    except bootstrap.BookSeriesNotSupportedException as err:
        print(err)
        sys.exit(1)

    xml_reader = StreamingXMLReader(input_file.name, bookseries.convert_xml_to_dict)
    extraction_constants.BOOK_NUMBER = book_number
    extraction_constants.BOOK_SERIES = bookseries_id

    print('Book series:', bookseries_id)
    bookseries.extract_data(xml_reader)
    bookseries.save_results(output_files[0], file_format='json')
    print('Process finished successfully.')


def chunk(args):
    bookseries_id = args['b']
    input_files = args['c']
    output_files = args['o']
    book_numbers = args['n']

    if bookseries_id is None or book_numbers is None:
        print(
            'Error: Both book series argument and book number in '
            'series should be provided when starting conversion '
            'process. Example: -b siirtokarjalaiset -n 1'
        )
        raise CommandLineParameterException()

    if output_files is None:
        print('Error: Both input file and the output file should be provided.')
        raise CommandLineParameterException()

    if len(output_files) != len(input_files) or len(output_files) != len(book_numbers):
        print(
            'Error: The number of files to chunk should match the number of output '
            'files and the number of book numbers.'
        )
        raise CommandLineParameterException()

    try:
        bookseries = bootstrap.setup_extraction_framework_for_bookseries(
            bookseries_id, PLUGIN_DIRECTORY, callback
        )
    except bootstrap.BookSeriesNotSupportedException:
        print(
            'Error: Provided book series is not supported. Try one from',
            ', '.join(AVAILABLE_BOOKSERIES),
        )
        raise CommandLineParameterException()

    print('Converting...')
    bookseries.chunk(
        input_files,
        output_files,
        book_numbers,
        filter_duplicates=args['filter'],
        callback=callback,
    )


def main():
    args = vars(parser.parse_args())

    if args['c'] is not None:
        try:
            chunk(args)
        except CommandLineParameterException:
            sys.exit(1)
    elif args['t'] is not None:
        run_nlp_parsing(args, PLUGIN_DIRECTORY)
    else:
        extract(args)


class CommandLineParameterException(Exception):
    pass


if __name__ == '__main__':
    main()

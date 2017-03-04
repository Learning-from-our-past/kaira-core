import sys
import argparse
from lxml import etree
from books.karelians.main import KarelianExtractor
from books.farmers.main import SmallFarmersExtractor

parser = argparse.ArgumentParser(description='Extract information from matrikel books.')
parser.add_argument('-i', nargs='?', type=argparse.FileType('r', encoding='utf8'), help='Input file to extract data from. Should be XML.', default=sys.stdin)
parser.add_argument('-o', nargs='?', type=argparse.FileType('w', encoding='utf8'), help='Output file to save data to.', default=sys.stdout)


def callback(current, max):
    percentage = round((current / max)*100)
    sys.stdout.write("Progress: %d%% - %d/%d   \r" % (percentage, current, max))
    sys.stdout.flush()


def main():
    args = vars(parser.parse_args())

    xml_parser = etree.XMLParser(encoding="utf-8")
    xml_document = etree.parse(args['i'], parser=xml_parser).getroot()

    book_series = xml_document.attrib["bookseries"]
    if book_series == 'Siirtokarjalaisten tie':
        print('Book series:', book_series)
        extractor = KarelianExtractor(callback)
        extractor.process(xml_document)
        extractor.save_results(args['o'], file_format='json')
        print('Process finished successfully.')

    elif book_series == 'Suomen pienviljelijat':
        print('Book series:', book_series)
        extractor = SmallFarmersExtractor(callback)
        extractor.process(xml_document)
        extractor.save_results(args['o'], file_format='json')
        print('Process finished successfully.')

    else:
        print('Error: File does not contain supported book series data', file = sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
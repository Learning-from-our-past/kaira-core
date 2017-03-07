import sys
import os
import subprocess
import argparse
from lxml import etree
from book_extractors.karelians.main import KarelianExtractor, get_karelian_data_entry
from book_extractors.farmers.main import SmallFarmersExtractor, get_small_farmers_data_entry
from book_extractors.greatfarmers.main import GreatFarmersExtractor, get_great_farmers_data_entry

parser = argparse.ArgumentParser(description='Extract information from matrikel books.')
parser.add_argument('-i', nargs='?', type=argparse.FileType('r', encoding='utf8'), help='Input file to extract data from. Should be XML.', default=sys.stdin)
parser.add_argument('-o', nargs='?', type=argparse.FileType('w', encoding='utf8'), help='Output file to save data to.', default=sys.stdout)


def callback(current, max):
    percentage = round((current / max)*100)
    sys.stdout.write("Progress: %d%% - %d/%d   \r" % (percentage, current, max))
    sys.stdout.flush()


def start_mongodb():
    if 'DEVELOPMENT' not in os.environ and 'TEST' not in os.environ:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        return subprocess.Popen(['mongodb/bin/mongod', '--dbpath', "mongodb/data/db"], startupinfo=startupinfo)
    else:
        return None


def xml_to_extractor_format(xml_document):
    """
    Transform xml file to dict format. This could be skipped if person raw data were saved as
    json not in xml...
    :param xml_document:
    :return:
    """
    book_series = xml_document.attrib["bookseries"]

    persons = []

    if book_series == 'Siirtokarjalaisten tie':
        for child in xml_document:
            if 'img_path' in child.attrib:
                path = child.attrib['img_path']
            else:
                path = ''
            persons.append(get_karelian_data_entry(child.attrib["name"], child.attrib['approximated_page'], child.text, path))
    elif book_series == 'Suomen pienviljelijat':
        for child in xml_document:
            persons.append(get_small_farmers_data_entry(child.attrib["name"], child.attrib["location"], child.attrib['approximated_page'], child.text))
    elif book_series == 'Suuret maatilat':
        for child in xml_document:
            persons.append(get_great_farmers_data_entry(child.attrib["name"], child.attrib["location"], child.attrib['approximated_page'], child.text))

    return persons

def main():
    args = vars(parser.parse_args())
    mongodb = None

    xml_parser = etree.XMLParser(encoding="utf-8")
    xml_document = etree.parse(args['i'], parser=xml_parser).getroot()

    book_series = xml_document.attrib["bookseries"]

    if book_series == 'Siirtokarjalaisten tie':
        print('Book series:', book_series)
        #mongodb = start_mongodb() # FIXME: Invent a sensible way to check if mongo start is required or not
        extractor = KarelianExtractor(callback)
        extractor.process(xml_to_extractor_format(xml_document))
        extractor.save_results(args['o'], file_format='json')
        print('Process finished successfully.')

    elif book_series == 'Suomen pienviljelijat':
        print('Book series:', book_series)
        #mongodb = start_mongodb()
        extractor = SmallFarmersExtractor(callback)
        extractor.process(xml_to_extractor_format(xml_document))
        extractor.save_results(args['o'], file_format='json')
        print('Process finished successfully.')

    elif book_series == 'Suuret maatilat':
        print('Book series:', book_series)
        #mongodb = start_mongodb()
        extractor = GreatFarmersExtractor(callback)
        extractor.process(xml_to_extractor_format(xml_document))
        extractor.save_results(args['o'], file_format='json')
        print('Process finished successfully.')
    else:
        print('Error: File does not contain supported book series data', file = sys.stderr)
        sys.exit(1)

    if mongodb is not None:
        mongodb.kill()


if __name__ == '__main__':
    main()

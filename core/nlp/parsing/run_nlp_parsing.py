import os
import sys
import xml.etree.ElementTree as ElementTree
from core import bootstrap


def run_nlp_parsing(args, plugin_dir):
    """
    Generates XML file with NLP data added to it based on existing XML file.
    :param args: Args from argparse. Expects at least 't' (input file to use for NLP tagging),
    'o' (list of output files, though we only use one). 'no_clean_up' (boolean) can also be
    specified.
    :param plugin_dir: Path where bookseries plugins can be found
    """
    file_path = args['t']
    clean_up = not args['no_clean_up']
    output_file = args['o'][0]

    base_path = os.path.splitext(file_path)[0]
    xml_doc = _get_xml_doc(file_path)

    xml_root = xml_doc.getroot()
    bookseries_id = xml_root.attrib['bookseries']

    try:
        bookseries = bootstrap.setup_extraction_framework_for_bookseries(
            bookseries_id, plugin_dir, None
        )
    except bootstrap.BookSeriesNotSupportedException as err:
        print(err)
        sys.exit(1)

    bookseries.parse_with_nlp(xml_doc, base_path, output_file, clean_up)


def _get_xml_doc(path):
    parser = ElementTree.XMLParser(encoding='utf-8')
    return ElementTree.parse(path, parser=parser)

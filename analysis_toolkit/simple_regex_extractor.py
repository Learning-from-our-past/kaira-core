from lxml import etree as ET
import regex
import argparse
import shutil
import sys
from shared.text_utils import remove_hyphens_from_text
from shared.text_utils import remove_spaces_from_text

"""
Run an "extraction" test using regex and get information about what kind of
strings the regex matched and the frequency of each match. This should be used
from a CLI, and if you are doing that, you can run the file with the --help 
option to get instructions on usage.
"""


progress_str = 'b[{}]:{:>4}% - {:>5}/{:>5}'
progress_bar_str = '{} [{}{}] \r'


def callback(b_num, current, max):
    percentage = round((current / max) * 100)
    progress_bar = progress_str.format(b_num + 1, percentage, current + 1, max)
    console_width = int(shutil.get_terminal_size()[0] / 2)
    bar_width = console_width - len(progress_bar)
    bar_fill = round(percentage * bar_width / 100)
    progress_bar = progress_bar_str.format(progress_bar, '#' * bar_fill, '-' * (bar_width - bar_fill))
    sys.stdout.write(progress_bar)
    sys.stdout.flush()


def open_xml_file(book_path):
        xml_doc = ET.parse('{}'.format(book_path))
        return xml_doc.getroot()


class SimpleRegexExtractor:
    def __init__(self, book_paths=None, extractor_regex=None, remove_whitespace=False, remove_hyphens=False, update_callback=None, display_texts=None, ignore_case=False):
        if book_paths is None:
            print('Book paths have to be specified!')
            sys.exit(1)

        self._books = []

        for book_path in book_paths:
            self._books.append(open_xml_file(book_path))

        if not extractor_regex:
            print('Failure! You must specify extractor_regex when using this class.')
            sys.exit(1)

        self._update_callback = update_callback

        self._options = {'remove_whitespace': remove_whitespace,
                         'remove_hyphens': remove_hyphens,
                         'display_texts': display_texts}

        if ignore_case:
            regex_options = (regex.UNICODE | regex.IGNORECASE)
        else:
            regex_options = regex.UNICODE

        self._EXTRACTION_REGEX = regex.compile(extractor_regex, regex_options)

        self._extracted_words = {}
        self._texts = []

    def find_frequencies_for_regex(self):
        uniques_total = 0
        for idx, book in enumerate(self._books):
            b_len = len(book)
            for idy, child in enumerate(book):
                if self._update_callback:
                    self._update_callback(idx, idy, b_len)

                text = child.text
                if self._options['remove_whitespace']:
                    text = remove_spaces_from_text(text)
                if self._options['remove_hyphens']:
                    text = remove_hyphens_from_text(text)

                matches = self._check_for_regex(text)
                found_match = False
                for match in matches:
                    if match[0] in self._extracted_words:
                        self._extracted_words[match[0]] += 1
                        found_match = True
                    else:
                        self._extracted_words[match[0]] = 1
                        found_match = True

                if found_match:
                    uniques_total += 1
                    if self._options['display_texts']:
                        self._texts.append(child.text)

            print('')

        regex_total = 0
        for word in sorted(self._extracted_words, key=self._extracted_words.get, reverse=True):
            if self._extracted_words[word] > 0:
                regex_total += self._extracted_words[word]
                print('  {:>5}:{:>25}'.format(self._extracted_words[word], word))

        if self._options['display_texts']:
            for text in self._texts:
                print('\n')
                print(text)

        print('total: {:>7}\nunique: {:>6}'.format(regex_total, uniques_total))

    def _check_for_regex(self, text):
        regex_matches = self._EXTRACTION_REGEX.finditer(text)

        return regex_matches


parser = argparse.ArgumentParser()
parser.add_argument('regex', help='The regular expression to use for extraction.',
                    type=str)
parser.add_argument('-books', nargs='*', help='The input file to look at.',
                    type=str)
parser.add_argument('--hyphens', action='store_true', help='Specify this to remove hyphens from text.')
parser.add_argument('--spaces', action='store_true', help='Specify this to remove spaces from text.')
parser.add_argument('--display-text', action='store_true', help='Whether to show the texts with matches at the end.')
parser.add_argument('--ignore-case', action='store_true', help='Whether to ignore case in regex matches.')

args = parser.parse_args()

r = SimpleRegexExtractor(book_paths=args.books,
                         extractor_regex=args.regex,
                         remove_hyphens=args.hyphens,
                         remove_whitespace=args.spaces,
                         update_callback=callback,
                         display_texts=args.display_text,
                         ignore_case=args.ignore_case)
r.find_frequencies_for_regex()
print('regex: {}'.format(args.regex))

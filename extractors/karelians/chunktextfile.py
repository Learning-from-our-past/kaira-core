from lxml.html import *
from lxml import etree
from lxml import html
import re
import os, nturl2path
import shutil
from core.interface.chunktextinterface import ChunkTextInterface
from extractors.karelians.duplicate_deleter import DuplicateDeleter


def read_html_file(path):
    return parse(path)


class PersonPreprocessor(ChunkTextInterface):

    def __init__(self, bookseries_id):
        super(PersonPreprocessor, self).__init__(bookseries_id)
        self._save_path = None
        self._book_number = None
        self._persons_document = None
        self._map_name_to_person = None
        self._current_person = None
        self._page_number = None
        self._images = None

        # This regular expression tries to match a name by the following pattern:
        # First there should be a name containing your typical alphabet and a hyphen, and it can be in
        # two parts, separated by a space. After that, there can be a space or a hyphen, followed by
        # a dot or a comma, followed by another possible space or hyphen. Then there can be up to three
        # words (names) after that, each at least one character long.
        self._ENTRY_NAME_REGEX = re.compile(r'(?:[A-ZÄÖ-]+\s?){1,2}[\s-]?[.,][\s-]?(?:\w+[\s-]?){1,3}',
                                            re.UNICODE)
        
        # This regular expression is used to detect when a person's entry in the .html file begins from
        # within another person's entry. This regex is quite a bit more refined than the original one and
        # does not pick up non-names, like military unit/regiment abbreviations. It also has a better rate
        # of getting both the first and surnames of a person, instead of just one of them.
        self._MID_ENTRY_NAME_REGEX = re.compile(r'(?:[A-ZÄ-Ö0-9!^%#]{4,}\s?){1,3}\s?[.,]\s?(?:[A-ZÄ-Ö0-9!^%#]{4,}\s?){1,3}',
                                                re.UNICODE)

    def chunk_text(self, text, destination_path, book_number):
        self._save_path = destination_path
        self._book_number = book_number
        text = re.sub(r'(<sup>)|</sup>', '', text)  # remove sup tags
        parsed = html.document_fromstring(text)
        persons = self._process(parsed)
        return persons

    def _process(self, tree):
        self._persons_document = etree.Element('DATA')
        self._persons_document.attrib['bookseries'] = self._bookseries_id
        self._persons_document.attrib['book_number'] = str(self._book_number)
        self._map_name_to_person = {}
        self._current_person = None
        self._page_number = 1
        self._images = []
        person_document = self._walk_tree(tree)
        self._join_images_to_persons()
        return person_document

    def _walk_tree(self, tree):
        for e in tree.iter():
            if 'src' in e.attrib:
                self._parse_image(e)

            if e.text is not None:
                try:
                    self._page_number = int(e.text)
                except ValueError:
                    if e.text[0:100].isupper() and self._ENTRY_NAME_REGEX.search(e.text) is not None:
                        self._add_person(self._current_person)
                        self._current_person = self._create_person(name=e.text, entry='')
                    elif self._current_person is not None:
                        self._process_element(e)

        self._add_person(self._current_person)
        return self._persons_document

    def _process_element(self, e):
        if len(e.text) > 40:
            # Attempt to detect people, whose entries start from within other people
            mid_entry_person = self._MID_ENTRY_NAME_REGEX.search(e.text)

            # TODO: Rough. Should be made recursive, so that if there are more than two people
            # TODO: in the same entry, they get separated as well.
            if mid_entry_person is not None:
                self._current_person.text += e.text[0:mid_entry_person.start()]
                self._add_person(self._current_person)
                new_person_name = mid_entry_person.group(0).strip(' ').strip('\xa0')
                self._current_person = self._create_person(name=new_person_name, entry=e.text[mid_entry_person.end():])
            else:
                self._current_person.text += e.text

            self._current_person.text = re.sub('\n', ' ', self._current_person.text)
            self._current_person.text = re.sub('\s{2,4}', ' ', self._current_person.text)

    def _parse_image(self, element):
        image_path = element.attrib['src']
        image_path = nturl2path.url2pathname(image_path)
        name = ''

        # Find caption text
        found_prev = self._find_prev_caption_text(element)

        if found_prev['found']:
            name = found_prev['prev'].text
        else:
            found_next = self._find_next_caption_text(element)
            if found_next['found']:
                name = found_next['next'].text

        if name != '':
            new_path = '{}.jpg'.format(re.sub(r'(?:[^a-zä-ö0-9]|(?<=[\'"])s)', r'', name, flags=re.IGNORECASE))
            file_prefix = os.path.basename(os.path.splitext(self._save_path)[0])
            new_path = os.path.join('{}_images'.format(file_prefix), new_path)
            self._copy_rename_image_files(new_path, image_path)
            self._images.append({'name': self._convert_image_name(name), 'image': new_path})

    def _find_prev_caption_text(self, element):
        prev_element = element.getprevious()
        found_prev = False
        counter = 1
        while not found_prev:
            try:
                if (prev_element is not None and prev_element.text is not None
                        and re.search('[A-ZÄ-Ö][a-zä-ö]+', prev_element.text) is not None
                        and len(prev_element.text) < 30):
                    found_prev = True
                else:
                    prev_element = prev_element.getprevious()
                    counter -= 1

                if counter == 0:
                    break
            except AttributeError:
                break
        return {'prev': prev_element, 'found': found_prev}

    def _find_next_caption_text(self, element):
        found_next = False
        next_element = element.getnext()
        counter = 1
        while not found_next:
            try:
                if (next_element is not None and next_element.text is not None
                        and re.search('[A-ZÄ-Ö][a-zä-ö]+', next_element.text) is not None
                        and len(next_element.text) < 30):
                    found_next = True
                else:
                    next_element = next_element.getnext()
                    counter -= 1
                if counter == 0:
                    break
            except AttributeError:
                break
        return {'next': next_element, 'found': found_next}

    def _copy_rename_image_files(self, new_path, image_path):
        # TODO: It would be nice to provide error message to user rather than fail silently
        try:
            # copy the image files and rename them according to person's name
            file_prefix = os.path.basename(os.path.splitext(self._save_path)[0])
            new_path = os.path.join(os.path.dirname(self._save_path), new_path)
            os.makedirs('{}/{}_images'.format(os.path.dirname(self._save_path), file_prefix), exist_ok=True)
            if not os.path.isfile(os.path.join(new_path)):
                old_image_path = os.path.join(os.getcwd(), os.path.join(*image_path.split('\\')))
                shutil.copy(old_image_path, new_path)
        except Exception:
            pass

    def _convert_image_name(self, name):
        name = name.upper()
        names = name.split(' ')
        names.reverse()
        new_name = ''
        new_name = '{}{}, '.format(new_name, names[0])
        names.pop(0)
        for n in names:
            new_name = '{}{} '.format(new_name, n)
        new_name = new_name.strip()
        return new_name

    def _join_images_to_persons(self):
        for image in self._images:
            if image['name'] in self._map_name_to_person:
                self._map_name_to_person[image['name']].attrib['img_path'] = image['image']

    def _create_person(self, name, entry):
        person = etree.Element('PERSON')
        person.attrib['name'] = name
        person.attrib['approximated_page'] = '{}-{}'.format(self._page_number - 1, self._page_number + 1)
        person.text = entry
        self._map_name_to_person[name] = person
        return person

    def _add_person(self, person):
        if person is not None and len(person.text) > 4:
            self._persons_document.append(person)


def convert_html_file_to_xml(bookseries_id, input_files, output_files, book_numbers, filter_duplicates=False, callback=None):
    books = []
    
    for input_file, output_file, book_number in zip(input_files, output_files, book_numbers):
        text = input_file.read()
        p = PersonPreprocessor(bookseries_id)
        persons = p.chunk_text(text, output_file.name, book_number)
        books.append(persons)
    
    if filter_duplicates:
        deleter = DuplicateDeleter(update_callback=callback)
        books = deleter.delete_duplicate_persons(books)

    for output_file, book in zip(output_files, books):
        output_file.write(etree.tostring(book, pretty_print=True, encoding='unicode'))
        output_file.close()
        print('File converted to xml and saved!')

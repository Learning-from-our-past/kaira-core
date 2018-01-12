from lxml.html import *
from lxml import etree
from lxml import html
import re
import os, nturl2path
import shutil
from interface.chunktextinterface import ChunkTextInterface
from book_extractors.karelians.main import BOOK_SERIES_ID


def read_html_file(path):
    return parse(path)


class PersonPreprocessor(ChunkTextInterface):

    def __init__(self):
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
        self.save_path = destination_path
        self.book_number = book_number
        text = re.sub(r'(<sup>)|</sup>', '', text)  # remove sup tags
        parsed = html.document_fromstring(text)
        persons = self.process(parsed)
        return etree.tostring(persons, pretty_print=True, encoding='unicode')

    def process(self, tree):
        self.persons_document = etree.Element('DATA')
        self.persons_document.attrib['bookseries'] = BOOK_SERIES_ID
        self.persons_document.attrib['book_number'] = str(self.book_number)
        self.map_name_to_person = {}
        self.current_person = None
        self.page_number = 1
        self.images = []
        person_document = self._walk_tree(tree)
        self._join_images_to_persons()
        return person_document

    def _walk_tree(self, tree):
        for e in tree.iter():
            if 'src' in e.attrib:
                self._parse_image(e)

            if e.text is not None:
                try:
                    self.page_number = int(e.text)
                except ValueError:
                    if e.text[0:100].isupper() and self._ENTRY_NAME_REGEX.search(e.text) is not None:
                        self._add_person(self.current_person)
                        self.current_person = self._create_person(name=e.text, entry='')
                    elif self.current_person is not None:
                        self._process_element(e)

        return self.persons_document

    def _process_element(self, e):
        if len(e.text) > 40:
            # pyritään huomaamaan ihmiset joiden entry alkaa toisen sisältä
            mid_entry_person = self._MID_ENTRY_NAME_REGEX.search(e.text)

            # TODO: Karkea. Pitäisi muuttaa rekursiiviseksi, jotta jos samassa entryssä on > 2
            # TODO: ihmistä, heidät eroteltaisiin myös.
            if mid_entry_person is not None:
                self.current_person.text += e.text[0:mid_entry_person.start()]
                self._add_person(self.current_person)
                new_person_name = mid_entry_person.group(0).strip(' ').strip('\xa0')
                self.current_person = self._create_person(name=new_person_name, entry=e.text[mid_entry_person.end():])
            else:
                self.current_person.text += e.text

            self.current_person.text = re.sub('\n', ' ', self.current_person.text)
            self.current_person.text = re.sub('\s{2,4}', ' ', self.current_person.text)

    def _parse_image(self, element):
        image_path = element.attrib['src']
        image_path = nturl2path.url2pathname(image_path)
        name = ''

        # Find caption text
        foundPrev = self._find_prev_caption_text(element)

        if foundPrev['found']:
            name = foundPrev['prev'].text
        else:
            foundNext = self._find_next_caption_text(element)
            if foundNext['found']:
                name = foundNext['next'].text

        if name != '':
            new_path = re.sub(r'(?:[^a-zä-ö0-9]|(?<=[\'"])s)', r'', name, flags=re.IGNORECASE) + '.jpg'
            file_prefix = os.path.basename(os.path.splitext(self.save_path)[0])
            new_path = os.path.join(file_prefix + '_images', new_path)
            self._copy_rename_imagefiles(new_path, image_path)
            self.images.append({'name': self._convert_image_name(name), 'image': new_path})

    def _find_prev_caption_text(self, element):
        prev = element.getprevious()
        foundPrev = False
        counter = 1
        while not foundPrev:
            try:
                if prev is not None and prev.text is not None and \
                                re.search('[A-ZÄ-Ö][a-zä-ö]{1,}', prev.text) is not None and len(prev.text) < 30:
                    foundPrev = True
                else:
                    prev = prev.getprevious()
                    counter -= 1

                if counter == 0:
                    break
            except AttributeError:
                break
        return {'prev': prev, 'found': foundPrev}

    def _find_next_caption_text(self, element):
        foundNext = False
        next = element.getnext()
        counter = 1
        while not foundNext:
            try:
                if next is not None and next.text is not None and \
                                re.search('[A-ZÄ-Ö][a-zä-ö]{1,}', next.text) is not None and len(next.text) < 30:
                    foundNext = True
                else:
                    next = next.getnext()
                    counter -= 1
                if counter == 0:
                    break
            except AttributeError:
                break
        return {'next': next, 'found': foundNext}

    def _copy_rename_imagefiles(self, new_path, image_path):
        # TODO: It would be nice to provide error message to user rather than fail silently
        try:
            # copy the image files and rename them according to person's name
            file_prefix = os.path.basename(os.path.splitext(self.save_path)[0])
            new_path = os.path.join(os.path.dirname(self.save_path), new_path)
            os.makedirs(os.path.dirname(self.save_path) + '/' + file_prefix + '_images', exist_ok=True)
            if not os.path.isfile(os.path.join(new_path)):
                shutil.copy(os.path.join(os.getcwd(), image_path), new_path)
        except Exception:
            pass

    def _convert_image_name(self, name):
        name = name.upper()
        names = name.split(' ')
        names.reverse()
        newname = ''
        newname += names[0] + ', '
        names.pop(0)
        for n in names:
            newname += n + ' '
        newname = newname.strip()
        return newname

    def _join_images_to_persons(self):
        for image in self.images:
            if image['name'] in self.map_name_to_person:
                self.map_name_to_person[image['name']].attrib['img_path'] = image['image']

    def _create_person(self, name, entry):
        person = etree.Element('PERSON')
        person.attrib['name'] = name
        person.attrib['approximated_page'] = str(self.page_number-1) + '-' + str(self.page_number+1)
        person.text = entry
        self.map_name_to_person[name] = person
        return person

    def _add_person(self, person):
        if person is not None and len(person.text) > 4:
            self.persons_document.append(person)


def convert_html_file_to_xml(input_file, output_file, book_number):
    text = input_file.read()
    p = PersonPreprocessor()
    persons = p.chunk_text(text, output_file.name, book_number)
    output_file.write(persons)
    output_file.close()
    print('File converted to xml and saved!')

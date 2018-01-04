from lxml.html import *
from lxml import etree
from lxml import html
import re
from interface.chunktextinterface import ChunkTextInterface
from book_extractors.farmers.main import BOOK_SERIES_ID

def read_html_file(path):
    return parse(path)


class PersonPreprocessor(ChunkTextInterface):

    def chunk_text(self, text, destination_path, book_number):
        self.save_path = destination_path
        self.book_number = book_number
        text = re.sub(r"(\<sup\>)|\<\/sup\>", "", text) #remove sup tags
        parsed = html.document_fromstring( text)
        persons = self.process(parsed)
        return etree.tostring(persons, pretty_print=True, encoding='unicode')

    def process(self, tree):
        self.persons_document = etree.Element("DATA")
        self.persons_document.attrib["bookseries"] = BOOK_SERIES_ID
        self.persons_document.attrib["book_number"] = str(self.book_number)
        self.map_name_to_person = {}
        self.current_person = None
        self.page_number = 1
        self.location = ""
        self.images = []
        person_document = self._walk_tree(tree)
        return person_document

    def _walk_tree(self, tree):
        for e in tree.iter():
            if e.text is not None:
                try:
                    if int(e.text) > 10:
                        self.page_number = int(e.text)
                except ValueError:
                    name = re.search("^[A-ZÄ-Ö -]{4,}", e.text)
                    if len(e.text) > 25 and name is not None:
                        self._add_person(self.current_person)
                        self.current_person = self._create_person(name=name.group(0).strip(" "), entry=e.text[name.end():])
                    elif self.current_person is not None:
                        if name is not None:
                            self._save_location(name.group(0).strip(" "))
                        else:
                            self._process_element(e)

                    if self.current_person is None:
                        if name is not None:
                            self._save_location(name.group(0).strip(" "))


        self._add_person(self.current_person)
        return self.persons_document

    def _save_location(self, name):
        self.location = re.sub(r"\s", "", name)


    def _process_element(self, e):
        if len(e.text) > 40:
            # try to notice people who start within other people
            uppercase = re.search("[A-ZÄ-Ö, ]{8,}", e.text)

            #TODO: Karkea. Pitäisi muuttaa rekursiiviseksi, jotta jos samassa entryssä on > 2
            #TODO: ihmistä, heidät eroteltaisiin myös.
            if uppercase is not None:
                self.current_person.text += e.text[0:uppercase.start()]
                self._add_person(self.current_person)
                self.current_person =  self._create_person(name=uppercase.group(0).strip(" "), entry=e.text[uppercase.end():])
            else:
                self.current_person.text += e.text

    def _create_person(self, name, entry):
        person = etree.Element("PERSON")
        person.attrib["name"] = re.sub(r"\s", "", name)
        person.attrib["location"] = self.location
        person.attrib["approximated_page"] = str(self.page_number-1) + "-" + str(self.page_number+1)
        person.text = entry
        self.map_name_to_person[name] = person
        return person

    def _add_person(self, person):
        if person is not None and len(person.text) > 4:
            self.persons_document.append(person)


def convert_html_file_to_xml(input_file, output_file, book_number, filter_duplicates=False):
    text = input_file[0].read()
    p = PersonPreprocessor()
    persons = p.chunk_text(text, output_file[0].name, book_number[0])
    output_file[0].write(persons)
    output_file[0].close()
    print('File converted to xml and saved!')
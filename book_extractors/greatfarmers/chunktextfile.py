from lxml.html import *
from lxml import etree
from lxml import html
import re
import cProfile
import os, nturl2path
import shutil
from interface.chunktextinterface import ChunkTextInterface

def read_html_file(path):
    return parse(path)


class PersonPreprocessor(ChunkTextInterface):

    def chunk_text(self, text, destination_path):
        self.save_path = destination_path
        text = re.sub(r"(\<sup\>)|\<\/sup\>", "", text) #remove sup tags
        parsed = html.document_fromstring( text)
        persons = self.process(parsed)
        return etree.tostring(persons, pretty_print=True, encoding='unicode')

    def process(self, tree):
        self.persons_document = etree.Element("DATA")
        self.persons_document.attrib["bookseries"] = "Suuret maatilat"
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
            #pyritään huomaamaan ihmiset joiden entry alkaa toisen sisältä
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
        if person is not None and len(person.text) > 4 and not self._remove_swedes(person):
            self.persons_document.append(person)

    def _remove_swedes(self, person):
        if re.search(r"gärd|ligger|ägare|andra|ägt|Totalarealen", person.text, re.UNICODE|re.IGNORECASE):
            return True

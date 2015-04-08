from lxml.html import *
from lxml import etree
import re
import json




def read_html_file(path):
    return parse(path)


class PersonPreprocessor:

    def parse_tree(self, tree):
        self.persons = []
        self.current_person = None
        for e in tree.iter():
            if e.text is not None:
                if e.text[0:100].isupper() and re.search("[A-ZÄ-Ö]{3,},[A-ZÄ-Ö ]{8,}", e.text) is not None:
                    self.add_person(self.current_person)
                    self.current_person = {"name": e.text, "entry" : ""}
                elif self.current_person is not None:
                    if len(e.text) > 40:
                        #pyritään huomaamaan ihmiset joiden entry alkaa toisen sisältä
                        uppercase = re.search("[A-ZÄ-Ö, ]{8,}", e.text)

                        #TODO: Karkea. Pitäisi muuttaa rekursiiviseksi, jotta jos samassa entryssä on > 2
                        #TODO: ihmistä, heidät eroteltaisiin myös.
                        if uppercase is not None:
                            self.current_person["entry"] += e.text[0:uppercase.start()]
                            self.add_person(self.current_person)
                            self.current_person = {"name": uppercase.group(0).strip(" "), "entry": e.text[uppercase.end():]}
                        else:
                            self.current_person["entry"] += e.text


        return self.persons

    def add_person(self, person):
        if person is not None and len(person["entry"]) > 4:
            self.persons.append(person)



parsed = read_html_file("Siirtokarjalaisten_whole_book.htm")
p = PersonPreprocessor()
persons = p.parse_tree(parsed)
f = open("results.json", "w", encoding="utf-8")
f.write(json.dumps(persons, ensure_ascii=False, indent=4))
f.close()
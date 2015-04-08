from lxml.html import *
from lxml import etree
import re
import json
import os, nturl2path
import shutil





def read_html_file(path):
    return parse(path)


class PersonPreprocessor:

    def parse_tree(self, tree):
        self.persons_document = etree.Element("DATA")
        self.current_person = None
        self.images = []

        for e in tree.iter():
            if "src" in e.attrib:
                self.parse_image(e)

            if e.text is not None:
                if e.text[0:100].isupper() and re.search("[A-ZÄ-Ö -]{3,}(,|\.)[A-ZÄ-Ö -]{3,}", e.text) is not None:
                    self.add_person(self.current_person)
                    self.current_person = self.create_person(name=e.text, entry="")
                elif self.current_person is not None:
                    if len(e.text) > 40:
                        #pyritään huomaamaan ihmiset joiden entry alkaa toisen sisältä
                        uppercase = re.search("[A-ZÄ-Ö, ]{8,}", e.text)

                        #TODO: Karkea. Pitäisi muuttaa rekursiiviseksi, jotta jos samassa entryssä on > 2
                        #TODO: ihmistä, heidät eroteltaisiin myös.
                        if uppercase is not None:
                            self.current_person.text += e.text[0:uppercase.start()]
                            self.add_person(self.current_person)
                            self.current_person =  self.create_person(name=uppercase.group(0).strip(" "), entry=e.text[uppercase.end():])
                        else:
                            self.current_person.text += e.text

        print(json.dumps(self.images))
        return self.persons_document

    def parse_image(self, element):
        image_path = element.attrib["src"]
        image_path = nturl2path.url2pathname(image_path)
        print(image_path)
        name = ""
        #Find caption text
        foundPrev = False
        prev = element.getprevious()
        counter = 1
        while not foundPrev:
            try:
                if prev is not None and prev.text is not None and \
                                re.search("[A-ZÄ-Ö][a-zä-ö]{1,}", prev.text) is not None and len(prev.text) < 30:
                    foundPrev = True
                else:
                    prev = prev.getprevious()
                    counter -=1

                if counter == 0:
                    break
            except AttributeError:
                break


        if foundPrev:
            name = prev.text
        else:
            foundNext = False
            next = element.getnext()
            counter = 1
            while not foundNext:
                try:
                    if prev is not None and next.text is not None and \
                                    re.search("[A-ZÄ-Ö][a-zä-ö]{1,}", next.text) is not None and len(next.text) < 30:
                        foundNext = True
                    else:
                        next = next.getnext()
                        counter -=1
                    if counter == 0:
                        break
                except AttributeError:
                    break

            if foundNext:
                name = next.text

        if name != "":
            #copy the image files and rename them according to person's name
            new_path = os.path.join(os.getcwd(), "images/" + re.sub(r"(?:<|>|&|'|\.|,| )", r"", name) + ".jpg")
            os.makedirs("./images", exist_ok=True)
            shutil.copy(os.path.join(os.getcwd(), image_path), os.path.join(os.getcwd(),new_path))
            self.images.append({"name": name, "image": new_path})

    def join_images_to_persons(self):
        pass

    def create_person(self, name, entry):
        person = etree.Element("PERSON")
        person.attrib["name"] = name
        person.text = entry
        return person

    def add_person(self, person):
        if person is not None and len(person.text) > 4:
            self.persons_document.append(person)



parsed = read_html_file("siirtokarjalaisten tie I fragment_kuvat.html")
p = PersonPreprocessor()
persons = p.parse_tree(parsed)
print(len(persons))
f = open("results.xml", "wb")
f.write(etree.tostring(persons, pretty_print=True, encoding='unicode').encode("utf8"))
f.close()
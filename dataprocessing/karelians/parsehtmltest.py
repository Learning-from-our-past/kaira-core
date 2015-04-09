from lxml.html import *
from lxml import etree
import re
import json
import os, nturl2path
import shutil





def read_html_file(path):
    return parse(path)


class PersonPreprocessor:

    def process(self, tree):
        self.persons_document = etree.Element("DATA")
        self.map_name_to_person = {}
        self.current_person = None
        self.images = []
        person_document = self._walk_tree(tree)
        self.join_images_to_persons()
        return person_document


    def _walk_tree(self, tree):
        for e in tree.iter():
            if "src" in e.attrib:
                self._parse_image(e)

            if e.text is not None:
                if e.text[0:100].isupper() and re.search("[A-ZÄ-Ö -]{3,}(,|\.)[A-ZÄ-Ö -]{3,}", e.text) is not None:
                    self.add_person(self.current_person)
                    self.current_person = self.create_person(name=e.text, entry="")
                elif self.current_person is not None:
                    self._process_element(e)

        return self.persons_document

    def _process_element(self, e):
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


    def _parse_image(self, element):
        image_path = element.attrib["src"]
        image_path = nturl2path.url2pathname(image_path)
        name = ""

        #Find caption text
        foundPrev = self._find_prev_caption_text(element)

        if foundPrev["found"]:
            name = foundPrev["prev"].text
        else:
            foundNext = self._find_next_caption_text(element)
            if foundNext["found"]:
                name = foundNext["next"].text

        if name != "":
            new_path = "images/" + re.sub(r"(?:<|>|&|'|\.|,| )", r"", name) + ".jpg"
            self._copy_rename_imagefiles(new_path, image_path)
            self.images.append({"name": self.convert_image_name(name), "image": new_path})

    def _find_prev_caption_text(self, element):
        prev = element.getprevious()
        foundPrev = False
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
        return {"prev": prev, "found" : foundPrev}

    def _find_next_caption_text(self, element):
        foundNext = False
        next = element.getnext()
        counter = 1
        while not foundNext:
            try:
                if next is not None and next.text is not None and \
                                re.search("[A-ZÄ-Ö][a-zä-ö]{1,}", next.text) is not None and len(next.text) < 30:
                    foundNext = True
                else:
                    next = next.getnext()
                    counter -=1
                if counter == 0:
                    break
            except AttributeError:
                break
        return {"next": next, "found" : foundNext}

    def _copy_rename_imagefiles(self, new_path, image_path):
         #copy the image files and rename them according to person's name
        os.makedirs("./images", exist_ok=True)
        if not os.path.isfile(os.path.join(os.getcwd(), new_path)):
            shutil.copy(os.path.join(os.getcwd(), image_path), os.path.join(os.getcwd(), new_path))

    def convert_image_name(self, name):
        name = name.upper()
        names = name.split(" ")
        names.reverse()
        newname = ""
        newname +=names[0]+ ", "
        names.pop(0)
        for n in names:
            newname +=n + " "
        newname = newname.strip()
        return newname

    def join_images_to_persons(self):
        for image in self.images:
            if image["name"] in self.map_name_to_person:
                self.map_name_to_person[image["name"]].attrib["img_path"] = image["image"]

    def create_person(self, name, entry):
        person = etree.Element("PERSON")
        person.attrib["name"] = name
        person.text = entry
        self.map_name_to_person[name] = person

        return person

    def add_person(self, person):
        if person is not None and len(person.text) > 4:
            self.persons_document.append(person)



parsed = read_html_file("siirtokarjalaisten tie I fragment_kuvat.html")
p = PersonPreprocessor()
persons = p.process(parsed)
print(len(persons))
f = open("results.xml", "wb")
f.write(etree.tostring(persons, pretty_print=True, encoding='unicode').encode("utf8"))
f.close()
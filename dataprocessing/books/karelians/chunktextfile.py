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
        print(self.save_path)
        parsed = html.document_fromstring( text)
        persons = self.process(parsed)
        print(len(persons))
        return etree.tostring(persons, pretty_print=True, encoding='unicode')

    def process(self, tree):
        self.persons_document = etree.Element("DATA")
        self.persons_document.attrib["bookseries"] = "Siirtokarjalaisten tie"
        self.map_name_to_person = {}
        self.current_person = None
        self.page_number = 1
        self.images = []
        person_document = self._walk_tree(tree)
        self._join_images_to_persons()
        return person_document


    def _walk_tree(self, tree):
        for e in tree.iter():
            if "src" in e.attrib:
                self._parse_image(e)

            if e.text is not None:
                try:
                    self.page_number = int(e.text)
                except ValueError:
                    if e.text[0:100].isupper() and re.search("[A-ZÄ-Ö -]{3,}(,|\.)[A-ZÄ-Ö -]{3,}", e.text) is not None:
                        self._add_person(self.current_person)
                        self.current_person = self._create_person(name=e.text, entry="")
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
                self._add_person(self.current_person)
                self.current_person =  self._create_person(name=uppercase.group(0).strip(" "), entry=e.text[uppercase.end():])
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
            new_path = re.sub(r"(?:[^a-zä-ö0-9]|(?<=['\"])s)", r"", name, flags=re.IGNORECASE) + ".jpg"
            file_prefix = os.path.basename(os.path.splitext(self.save_path)[0])
            new_path = os.path.join(file_prefix + "_images", new_path)
            self._copy_rename_imagefiles(new_path, image_path)
            self.images.append({"name": self._convert_image_name(name), "image": new_path})

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
        #TODO: It would be nice to provide error message to user rather than fail silently
        try:
            #copy the image files and rename them according to person's name
            file_prefix = os.path.basename(os.path.splitext(self.save_path)[0])
            new_path = os.path.join(os.path.dirname(self.save_path), new_path)
            os.makedirs(os.path.dirname(self.save_path) + "/" + file_prefix + "_images", exist_ok=True)
            if not os.path.isfile(os.path.join(new_path)):
                shutil.copy(os.path.join(os.getcwd(), image_path), new_path)
        except Exception:
            pass

    def _convert_image_name(self, name):
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

    def _join_images_to_persons(self):
        for image in self.images:
            if image["name"] in self.map_name_to_person:
                self.map_name_to_person[image["name"]].attrib["img_path"] = image["image"]

    def _create_person(self, name, entry):
        person = etree.Element("PERSON")
        person.attrib["name"] = name
        person.attrib["approximated_page"] = str(self.page_number-1) + "-" + str(self.page_number+1)
        person.text = entry
        self.map_name_to_person[name] = person
        return person

    def _add_person(self, person):
        if person is not None and len(person.text) > 4:
            self.persons_document.append(person)

def start():
    os.chdir("material")
    f = open("Siirtokarjalaisten tie I fragment_kuvat.html", "r", encoding="utf8")
    text = f.read()
    #"Siirtokarjalaisten_whole_book.htm") #Siirtokarjalaisten_whole_book.htm
    p = PersonPreprocessor()
    persons = p.chunk_text(text)
    f = open("results.xml", "wb")
    f.write(persons.encode("utf8"))
    f.close()

if __name__ == "__main__":
    start()
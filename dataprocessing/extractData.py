# -*- coding: utf-8 -*-
import readData
import re
import unicodecsv
import unicodedata

#use regex to extract the person's names and birthday from given text
#returns dict containing the data
#Possible exception handling should be done in higher level.
def extractPersonNameAndBirthday(text):
    text = ' '.join(text.split())   #remove excess whitespace and linebreaks
    p = re.compile(ur'\A([A-ZÄ-Ö]{3,}), {0,100}([A-ZÄ-Öa-zä-ö ]{0,}), {0,100}s {0,100}([0-9]{1,2} {0,3}\.[0-9]{1,2} {0,3}\.[0-9]{1,2})',re.UNICODE)
    m = p.match(unicode(text))
    return {"surname": m.group(1), "firstnames": m.group(2), "birthday": m.group(3)}


errors = 0
root = readData.getXMLroot("rintamamiehet8_newtags.xml")
#save the extract4ed info to a csv file:
with open("soldiers.csv", "wb") as results:
    with open("errors.csv", "wb") as errorcsv:
        writer = unicodecsv.writer(results, delimiter=";")
        writer.writerow(["surname", "first names", "birthday"])

        ewriter = unicodecsv.writer(errorcsv, delimiter=";")
        ewriter.writerow(["Exception", "Entry text"])

        for child in root:
            try:
                d = extractPersonNameAndBirthday(child.text)
                writer.writerow([d["surname"], d["firstnames"], d["birthday"]])
            except Exception as e:
                ewriter.writerow([str(e), child.text])
                errors +=1
                continue


print "Errors encountered: " + str(errors)
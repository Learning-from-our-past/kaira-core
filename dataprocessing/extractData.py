# -*- coding: utf-8 -*-
import readData
import re
import unicodecsv
import unicodedata

root = readData.getXMLroot("rintamamiehet8_tags.xml")

def extractPersonNameAndBirthday(text):
    text = ' '.join(text.split())
    print "----"

    print text
    p = re.compile(ur'\A([A-ZÄ-Ö]{3,}), {0,100}([A-ZÄ-Öa-zä-ö ]{0,}), {0,100}s {0,100}([0-9]{1,2} {0,3}\.[0-9]{1,2} {0,3}\.[0-9]{1,2})',re.UNICODE)
    m = p.match(unicode(text))
    print
    print m.group(1)
    print m.group(3)

    return {"surname": m.group(1), "firstnames": m.group(2), "birthday": m.group(3)}

print extractPersonNameAndBirthday(root[0].text)


errors = 0
#save the extract4ed info to a csv file:
with open("soldiers.csv", "wb") as results:
    writer = unicodecsv.writer(results, delimiter=";")
    writer.writerow(["surname", "first names", "birthday"])

    for child in root:
        try:
            d = extractPersonNameAndBirthday(child.text)
            writer.writerow([d["surname"], d["firstnames"], d["birthday"]])
        except:
            errors +=1
            continue


print "Errors encountered: " + str(errors)
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
    p = re.compile(ur'\A([A-ZÄ-Öl -]{3,}), {0,100}([A-ZÄ-Öa-zä-ö ]{0,}),',re.UNICODE)    # {0,100}([0-9]{1,2} {0,3}\.[0-9]{1,2} {0,3}\.[0-9]{1,2})
    m = p.match(unicode(text))

    #print m.span()

    dateguess = text[m.span()[1]:m.span()[1]+16]    #take substring which probably contains the date.
    dateguess = dateguess.replace(" ","")                       #remove all whitespace in the substring

    try:
        #try to find the date in modified string with regexp
        dp = re.compile(ur'.*(?:s|S|5)(?:(\d{1,2}\.\d{1,2}\.\d{2,4})|(\d{2,4}))',re.UNICODE)
        date = dp.match(unicode(dateguess))

        #get the result from correct capturegroup. If there is full date (12.7.18) it is in 1, if only year it is in 2.
        #could probably be written better in regexp, which uses only one group?
        dob = ""
        if date.group(1) == None:
            dob = date.group(2)
        else:
            dob = date.group(1)

        return {"surname": m.group(1), "firstnames": m.group(2), "birthday": dob}    #, "birthday": m.group(3)
    except Exception as e:
        print "---------------------"
        print m.group()
        print dateguess
        print dob
        print "---------------------"
        raise Exception(e.message + " Error in birthday regexp.")
        raise e


errors = 0
count = 0
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
                count +=1
            except Exception as e:
                ewriter.writerow([str(e), child.text])
                errors +=1
                count +=1
                continue


print "Errors encountered: " + str(errors) + "/" + str(count)
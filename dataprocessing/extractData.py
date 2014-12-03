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
    p = re.compile(ur'\A(?P<surname>[A-ZÄ-Öl() -]{3,})(:?,|.) {0,100}(?P<firstnames>[A-ZÄ-Öa-zä-ö() ]{0,})(:?,|.)',re.UNICODE)    # {0,100}([0-9]{1,2} {0,3}\.[0-9]{1,2} {0,3}\.[0-9]{1,2})
    m = p.match(unicode(text))

    dateguess = text[m.span()[1]:m.span()[1]+16]    #take substring which probably contains the date.
    dateguess = dateguess.replace(" ","")                       #remove all whitespace in the substring

    try:
        #try to find the date in modified string with regexp
        dp = re.compile(ur'.*(?:s|S|5)(?:(?:(?P<day>\d{1,2})(?:\.|,| )(?P<month>\d{1,2})(?:\.|,| )(?P<year>\d{2,4}))|(?P<yearOnly>\d{2,4})(?!\.|,))',re.UNICODE)
        date = dp.match(unicode(dateguess))

        #get the result from correct capturegroup. If there is full date (12.7.18) it is in 1, if only year it is in 2.
        #could probably be written better in regexp, which uses only one group?
        year = ""
        if date.group("year") == None:
            year = date.group("yearOnly")
        else:
            year = date.group("year")

        #fix years to four digit format.
        if int(year) < 50:
            year = "19" + year
        elif int(year) < 1800:
            year = "18" + year

    except Exception as e:
        print "---------------------"
        print m.group(0)
        print dateguess
        print "---------------------"
        raise Exception(e.message + " Error in birthday regexp.")


     #find birthplace:
    locationName = extractBirthLocation(text[(m.span()[1]+date.span()[1]):(m.span()[1]+date.span()[1])+24])
    return {"surname": m.group("surname"), "firstnames": m.group("firstnames"), "birthDay": date.group("day"),"birthMonth": date.group("month"), "birthYear": year, "birthLocation": locationName}    #, "birthday": m.group(3)



#try to extract the location of the birth. Later the results could be compared to the list of locations
def extractBirthLocation(text):
    try:
        p = re.compile(ur'.\d+(?: |,|.)+(?P<location>[A-ZÄ-Ö]{1,1}[A-ZÄ-Öa-zä-ö -]{1,})(,|\.)',re.UNICODE)    # {0,100}([0-9]{1,2} {0,3}\.[0-9]{1,2} {0,3}\.[0-9]{1,2})
        m = p.match(unicode(text))
        return m.group("location")

    except Exception as e:
        print "----LOCATION----"
        #print m.group(0)
        print "---------------------"
        raise Exception(u"Error in LOCATION regexp: " + text.encode("utf-8"))

errors = 0
count = 0
root = readData.getXMLroot("rintamamiehet8_newtags.xml")
#save the extract4ed info to a csv file:
with open("soldiers.csv", "wb") as results:
    with open("errors.csv", "wb") as errorcsv:
        writer = unicodecsv.writer(results, delimiter=";")
        writer.writerow(["surname", "first names", "birthDay", "birthMonth", "birthYear", "birthLocation"])

        ewriter = unicodecsv.writer(errorcsv, delimiter=";")
        ewriter.writerow(["Exception", "Entry text"])

        for child in root:
            try:
                d = extractPersonNameAndBirthday(child.text)
                writer.writerow([d["surname"], d["firstnames"], d["birthDay"], d["birthMonth"], d["birthYear"], d["birthLocation"]])
                count +=1
            except Exception as e:
                ewriter.writerow([str(e), child.text])
                errors +=1
                count +=1
                continue


print "Errors encountered: " + str(errors) + "/" + str(count)
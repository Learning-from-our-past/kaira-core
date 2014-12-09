# -*- coding: utf-8 -*-
import readData
import re
import unicodecsv
import unicodedata
from extractionExceptions import *

#use regex to extract the person's names and birthday from given text
#returns dict containing the data
#Possible exception handling should be done in higher level.
class DataExtraction:
    parsingLocation = 0 #holds the location of the process in the current entry.

    def extractPersonNameAndBirthday(self, text):
        try:
            #Extract names
            p = re.compile(ur'\A(?P<surname>[A-ZÄ-Öl() -]{3,})(:?,|.) {0,100}(?P<firstnames>[A-ZÄ-Öa-zä-ö() ]{0,})(:?,|.)',re.UNICODE)
            m = p.match(unicode(text))

        except Exception as e:
            raise NameException(text)

        return {"surname": m.group("surname"), "firstnames": m.group("firstnames"), "cursorLocation": m.end()}


    def extractBirthday(self, text, cursorLocation):

        try:
            #try to find the date in modified string with regexp
            dateguess = text[cursorLocation:cursorLocation+16]    #take substring which probably contains the date.
            dateguess = dateguess.replace(" ","")           #remove all whitespace in the substring
            dp = re.compile(ur'.*(?:s|S|5)(?:(?:(?P<day>\d{1,2})(?:\.|,|:|s)(?P<month>\d{1,2})(?:\.|,|:|s)(?P<year>\d{2,4}))|(?P<yearOnly>\d{2,4})(?!\.|,|\d))',re.UNICODE)
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
            #print "----BIRTHDAY----"
            #print dateguess
            #print "---------------------"
            raise BirthdayException(dateguess)


        #find birthplace:
        #locationName = self.extractBirthLocation(text[(m.span()[1]+date.span()[1]):(m.span()[1]+date.span()[1])+24])
        return {"birthDay": date.group("day"),"birthMonth": date.group("month"), "birthYear": year, "cursorLocation": cursorLocation + date.end()}    #, "birthday": m.group(3)



    #try to extract the location of the birth. Later the results could be compared to the list of locations
    def extractBirthLocation(self, text, cursorLocation):
        text2 = text[cursorLocation:cursorLocation+24]
        try:
            p = re.compile(ur'.\d*(?: |,|.)+(?P<location>[A-ZÄ-Ö]{1,1}[A-ZÄ-Öa-zä-ö -]{1,})(,|\.)',re.UNICODE)
            m = p.match(unicode(text2))
            return { "birthLocation": m.group("location"), "cursorLocation": cursorLocation + m.end()}
        except Exception as e:
            raise BirthplaceException(text)

    #find possible spouse and all relevant information
    def extractSpouseInformation(self, text, cursorLocation):
        text2 = text[cursorLocation:cursorLocation+80]
        foundSpouse = False
        findSpouseRE = re.compile(ur'(?P<spouseExists>\b(?:P|p)so\b)',re.UNICODE)  #first find out if there is spouse:
        findSpouseREm = findSpouseRE.search(unicode(text2))
        if findSpouseREm != None:
            foundSpouse = True      #found Pso which suggests there is spouse information available.

        if foundSpouse:
            p = re.compile(ur'\bvsta\b (?P<weddingYear>\d{1,2}) (?P<spouseName>[A-ZÄ-Öa-zä-ö -]+)(?:,|.)',re.UNICODE)
            m = p.search(unicode(text2))
            try:
                weddingYear = int(m.group("weddingYear"))
            except Exception as e:
                raise SpouseException(text2, "WEDDINGYEAR")

            try:
                spouseName = m.group("spouseName")
            except Exception as e:
                raise SpouseException(text2, "SPOUSENAME")

            try:
                spouseBirthYear = self.extractBirthday(text2[m.end():], 0)
            except Exception as e:
                raise SpouseException(text2, "SPOUSEBIRTHDAY")

            try:
                birthPlace = self.extractBirthLocation(text2[m.end() + spouseBirthYear["cursorLocation"]:], 0)
            except Exception as e:
                raise SpouseException(text2, "BIRTHPLACE")

            return {"hasSpouse": foundSpouse, "weddingYear": weddingYear, "spouseName": spouseName, "spouseBirthData": spouseBirthYear, "spouseBirthLocation": birthPlace["birthLocation"]}





        else:
            return {"hasSpouse": foundSpouse, "weddingYear": "", "spouseName": "", "spouseBirthData": {"birthDay": "","birthMonth": "", "birthYear": ""}, "spouseBirthLocation": ""}






    def extraction(self,text):
        text = ' '.join(text.split())   #remove excess whitespace and linebreaks
        personData = {}
        self.parsingLocation = 0
        personData = self.extractPersonNameAndBirthday(text)
        personBirthday = self.extractBirthday(text, personData["cursorLocation"])
        personLocation= self.extractBirthLocation(text, personBirthday["cursorLocation"])
        spouse = self.extractSpouseInformation(text, personLocation["cursorLocation"])
        print spouse
        return dict(personData.items() + personBirthday.items() + personLocation.items() + spouse.items())

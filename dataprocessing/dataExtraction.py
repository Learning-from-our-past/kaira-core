# -*- coding: utf-8 -*-
import readData
import re
import unicodecsv
import unicodedata
import nltk
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

            return {"surname": m.group("surname"), "firstnames": m.group("firstnames"), "cursorLocation": m.end()}
        except Exception as e:
            raise NameException(text)




    def extractBirthday(self, text, cursorLocation, windowWidth = 16):

        try:
            #try to find the date in modified string with regexp
            dateguess = text[cursorLocation:cursorLocation+windowWidth]    #take substring which probably contains the date.
            dateguess = dateguess.replace(" ","")           #remove all whitespace in the substring
            dp = re.compile(ur'.*(?:s|S|5)(?:(?:(?P<day>\d{1,2})(?:\.|,|:|s)(?P<month>\d{1,2})(?:\.|,|:|s)(?P<year>\d{2,4}))|(?P<yearOnly>\d{2,4})(?!\.|,|\d)(?=\D\D\D\D\D))',re.UNICODE)
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


    def extractDeath(self, text, cursorLocation, windowWidth = 16 , forMan=True):

        regexPattern = ur'.*k(?:(?:(?P<day>\d{1,2})(?:\.|,|:|s)(?P<month>\d{1,2})(?:\.|,|:|s)(?P<year>\d{2,4}))|(?P<yearOnly>\d{2,4})(?!\.|,|\d)(?=\D\D\D\D\D))'
        kaatunut = False
        if forMan:
            #snip the string if there is "Pso" to avoid extracting wife name instead of location name:
            f = text.find("Pso")
            if f != -1:
                text = text[0:f]

            #check if man has died in war
            k = text.find(" kaat ")
            if k != -1:
                kaatunut = True
                regexPattern = ur'.*kaat(?:(?:(?P<day>\d{1,2})(?:\.|,|:|s)(?P<month>\d{1,2})(?:\.|,|:|s)(?P<year>\d{2,4}))|(?P<yearOnly>\d{2,4})(?!\.|,|\d)(?=\D\D\D\D\D))'

        try:
            #try to find the date in modified string with regexp
            deathLocation = ""
            dateguess = text[cursorLocation:cursorLocation+windowWidth]    #take substring which probably contains the date.
            dateguess = dateguess.replace(" ","")           #remove all whitespace in the substring
            dp = re.compile(regexPattern,re.UNICODE)
            date = dp.search(unicode(dateguess))



            #get the result from correct capturegroup. If there is full date (12.7.18) it is in 1, if only year it is in 2.
            #could probably be written better in regexp, which uses only one group?
            year = ""
            if date.group("year") == None:
                year = date.group("yearOnly")
            else:
                year = date.group("year")


            year = "19" + year



            d = self.extractLocation(text, cursorLocation+date.end(), forMan, True)
            cursorLocation = d["cursorLocation"]
            deathLocation = d["birthLocation"]  #a misnomer since we use birthlocation function to find the deathlocation. Refactor.
            #try to find the death place:
            #self.extractBirthLocation(text, )


        except Exception as e:
            #print "----BIRTHDAY----"
            #print dateguess
            #print "---------------------"
            return {"deathDay": "","deathMonth": "", "deathYear": "", "kaatunut": "", "deathLocation": deathLocation, "cursorLocation": cursorLocation}
            #raise BirthdayException(dateguess)

        return {"deathDay": date.group("day"),"deathMonth": date.group("month"), "deathYear": year, "kaatunut": kaatunut, "deathLocation": deathLocation, "cursorLocation": cursorLocation + date.end()}



    #try to extract the location of the birth. Later the results could be compared to the list of locations
    def extractLocation(self, text, cursorLocation, forMan=True, forDeath=False):

        if forMan:
            text2 = text[cursorLocation-4:cursorLocation+24]
            f = text2.find("Pso")
            if f != -1:
                text2 = text2[0:f]
        else:
            #snip the string if there is "Pso" to avoid extracting wife name instead of location name:
            text2 = text[cursorLocation:cursorLocation+24]
            f = text2.find("Pso")

            if f != -1:
                text2 = text2[0:f]

        try:
            p = re.compile(ur'\d+(?: |,|\.)(?P<location>[A-ZÄ-Ö]{1,1}[A-ZÄ-Öa-zä-ö-]{1,}(?: mlk)?)',re.UNICODE)   #.\d*(?: |,|.)+(?P<location>[A-ZÄ-Ö]{1,1}[A-ZÄ-Öa-zä-ö-]{1,})(,|\.)
            m = p.search(unicode(text2))

            #check if the string has data on death. If it is before the location, be careful to not
            #put the death location to birth location.

            checkDeathp = re.compile(ur'(\bk\b|\bkaat\b)',re.UNICODE)
            checkDeathm = checkDeathp.search(unicode(text2))
            if checkDeathm != None and forDeath == False:
                if checkDeathm.end() < m.end():
                    #print text2
                    #there is entry of death before the matched location. Discard the result:
                    return {"birthLocation": "", "cursorLocation": cursorLocation + m.end()}


            return {"birthLocation": m.group("location"), "cursorLocation": cursorLocation + m.end()}
        except Exception as e:
            raise BirthplaceException(text2)

    #find possible spouses and then call function to extract the data.
    def findSpouses(self, text, cursorLocation):
        text2 = text[cursorLocation-5:]
        spouseWindow = 120
        foundSpouse = False
        findSpouseRE = re.compile(ur'(?P<spouseExists>\b(?:P|p)so\b)',re.UNICODE)  #first find out if there is spouse:
        findSpouseREm = findSpouseRE.search(unicode(text2))

        spouseCount = findSpouseRE.finditer(text2)
        spouseCount = tuple(spouseCount)
        children = {}

        if findSpouseREm != None:
            foundSpouse = True      #found Pso which suggests there is spouse information available.

        if foundSpouse:

            wives = []
            for i in range(0, len(spouseCount)):

                #decide the end position of the substring where to find the spouse
                if i+1 < len(spouseCount):
                    endPos = spouseCount[i+1].start()
                    children = self.findChildren(text2[spouseCount[i].start():endPos+4], 0)

                else:
                    endPos = spouseCount[i].start() + spouseWindow
                    children = self.findChildren(text2[spouseCount[i].start():], 0)

                wife = self.extractSpouse(text2[spouseCount[i].start():endPos], 0)
                wife["children"] = children

                wives.append(wife)


            if len(wives) == 2:
                #print text2[spouseCount[0].start():endPos]
                print wives
                #print "----"

            if len(wives) > 2:
                #raise SpouseException(text, "TOOMUCHWIVES")
                print "Vaimot: " + str(len(wives)) +" " + text2


            spouseData = { "spouseCount" : len(wives), "wifeList": wives} #self.extractSpouse(text2, cursorLocation)

            spouseData["hasSpouse"] = foundSpouse
            spouseData["spouseCount"] = len(wives)
            return spouseData
        else:
            return {"spouseCount" : 0, "hasSpouse" : foundSpouse}


    #extract data related to single spouse. Function is provided with a substring whihc contains
    #spouse information
    def extractSpouse(self, text, cursorLocation):
        birthYearWindowLeftOffset = 10
        #try to find wedding year and the name of the spouse. Wedding year is optional.
        p = re.compile(ur'\b(?:P|p)so\b(?: \bvst?l?a ?(?P<weddingYear>\d{1,2}))? ?(?P<spouseName>[A-ZÄ-Öa-zä-ö -]+)(?:,|.)',re.UNICODE)
        m = p.search(unicode(text))
        try:
            if m.group("weddingYear") != None:
                weddingYear = int(m.group("weddingYear"))
            else:
                weddingYear = ""
        except Exception as e:
            raise SpouseException(text, "WEDDINGYEAR")

        try:
            spouseName = m.group("spouseName")
        except Exception as e:
            raise SpouseException(text, "SPOUSENAME")

        try:
            spouseBirthYear = self.extractBirthday(text[(m.end()-birthYearWindowLeftOffset):], 0, 64)
        except ExtractionException as e:
            #raise SpouseException(e.details, "SPOUSEBIRTHDAY")         #TODO: PITÄISI MERKITÄ KUITENKIN LOKIIN!
            spouseBirthYear = {"birthDay": "","birthMonth": "", "birthYear": "", "cursorLocation": m.end()-birthYearWindowLeftOffset + 64}

        try:
            #print text2[m.end() + spouseBirthYear["cursorLocation"]-birthYearWindowLeftOffset:]
            birthPlace = self.extractLocation(text[m.end() + spouseBirthYear["cursorLocation"]-birthYearWindowLeftOffset:], 0, False)
        except ExtractionException as e:
            #raise SpouseException(e.details, "SPOUSEBIRTHPLACE")
            birthPlace= {"birthLocation": ""}


        deathData = self.extractDeath(text, m.end(), 40, False)
        return {"cursorLocation": deathData["cursorLocation"], "weddingYear": weddingYear, "spouseName": spouseName, "spouseBirthData": spouseBirthYear, "spouseDeathData": deathData,"spouseBirthLocation": birthPlace["birthLocation"]}



    #try to find the list of children from the soldier and return it as a single string.
    def findChildren(self, text, cursorLocation):
        text = text[cursorLocation:]
        #print "-----"
        text = re.sub(ur'[:;\!\?\+~¨\^\'\"]', '', text)
        #print text

        p = re.compile(ur'(?:Lapset|Tytär|Poika|Lapsel|Tylär)(?P<children>[A-ZÄ-Öa-zä-ö,0-9,\.\n -]*?)((?:- ?\n?(?=(?:Ts)|(?:Js)|(?:JR)|(?:Osall))|(?=pso)))',re.UNICODE | re.IGNORECASE)
        m = p.search(unicode(text))

        if m != None:
            children = m.group("children")
            #naive implementation TODO: MAKE BETTER
            childList1 = children.split(",")
            childList2 = []
            for c in childList1:
                c = ' '.join(c.split())
                if len(c) > 2:
                    childList2.append(c)

            return {"children": m.group("children"), "childCount" : len(childList2),"cursorLocation" : cursorLocation + m.end()}
        else:
            #try to find children encoded with numbers words:
            p = re.compile(ur'(?P<count>yksi|kaksi|kolme|neljä|viisi|kuusi|seitsemän|kahdeksan|yhdeksän|kymmenen) (?:lasta|lapsi|tytär|poika)',re.UNICODE | re.IGNORECASE)
            m = p.search(unicode(text))
            numberwords = {"yksi": 1, "kaksi": 2, "kolme": 3, "neljä": 4, "viisi": 5, "kuusi": 6, "seitsemän": 7, "kahdeksan": 8, "yhdeksän": 9, "kymmenen": 10}

            if m != None:
                if m.group("count").lower() in numberwords:
                    #print "Avainsana löytyi: " + str(numberwords[m.group("count").lower()])
                    return {"children": "", "cursorLocation" : cursorLocation, "childCount": numberwords[m.group("count").lower()]}
                else:
                    return {"children": "", "cursorLocation" : cursorLocation, "childCount": 0}
            else:
                #raise ChildrenException(text)
                return {"children": "", "cursorLocation" : cursorLocation, "childCount": 0}

 #check if the count of "Js" and "Ts" makes sense.

    #figure out if the soldier has been in Ts or Js
    def warCheck(self, text):
        findJsRE = re.compile(ur'(?P<jsExists>(?:Js:|JS:|js:|jS:))',re.UNICODE)  #first find out if there is spouse:
        findJsREm = findJsRE.search(unicode(text))

        JsCount = findJsRE.finditer(text)
        JsCount = tuple(JsCount)

        result = {"talvisota": False, "jatkosota" : False}
        if len(JsCount) >= 1:
            result["jatkosota"] = True

        findTsRE = re.compile(ur'(?P<tsExists>(?:Ts:|TS:|ts:|tS:))',re.UNICODE)  #first find out if there is spouse:
        findTsREm = findTsRE.search(unicode(text))

        TsCount = findTsRE.finditer(text)
        TsCount = tuple(TsCount)

        if len(TsCount) >= 1:
            result["talvisota"] = True

        return result

    #try to find the rank of a soldier
    def findRank(self, text):
        findRankRE = re.compile(ur'(?:Sotarvo|Ylenn)(?: |\n)(?P<rank>[A-ZÄ-Öa-zä-ö0-9, \n]{2,})\.',re.UNICODE)  #first find out if there is spouse:
        findRankREm = findRankRE.search(unicode(text))

        if findRankREm != None:
            result = {"rank": findRankREm.group("rank")}
        else:
            #raise RankException(text)
            result = {"rank" : ""}

        return result

    #find if the soldier has some of the most important medals.
    def findMedals(self, text):
        


    def extraction(self,text):
        text = ' '.join(text.split())   #remove excess whitespace and linebreaks
        personData = {}
        self.parsingLocation = 0
        personData = self.extractPersonNameAndBirthday(text)
        personBirthday = self.extractBirthday(text, personData["cursorLocation"])
        personLocation= self.extractLocation(text, personBirthday["cursorLocation"])
        personDeath = self.extractDeath(text, personBirthday["cursorLocation"], 32)
        spouseData = self.findSpouses(text, personLocation["cursorLocation"])

        #if there is no spouse, try to still find children:
        if spouseData["spouseCount"] == 0:
            children = self.findChildren(text, personLocation["cursorLocation"])
        else:
            children = {}

        #check the wars the soldier has served in:
        wars = self.warCheck(text)
        rank = self.findRank(text)


        #print spouse
        return dict(personData.items() + personBirthday.items() + personLocation.items() + personDeath.items()+ spouseData.items() + children.items() + wars.items() + rank.items())

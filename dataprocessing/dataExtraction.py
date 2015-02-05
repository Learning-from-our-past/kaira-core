# -*- coding: utf-8 -*-
import readData
import re
import unicodecsv
import unicodedata
from operator import itemgetter
from extractionExceptions import *
import regex

#use regex to extract the person's names and birthday from given text
#returns dict containing the data
#Possible exception handling should be done in higher level.
class DataExtraction:
    parsingLocation = 0 #holds the location of the process in the current entry.
    errorLogger = None
    currentChild = None

    monthNameNumberMapping = {"syks": 9, "marrask": 11, "eiok": 8, "elok": 8, "heinäk": 7, "helmik": 2, "huhtik" : 4,
    "jouluk": 12, "kesäk": 6, "lokak": 10, "maalisk": 3, "maallsk": 3, "syysk": 9, "tammik": 1, "toukok": 5}

    def extractPersonName(self, text):
        try:
            #Extract names
            p = re.compile(ur'\A(?P<surname>[A-ZÄ-Öl() -]{3,})(:?,|.) {0,100}(?P<firstnames>[A-ZÄ-Öa-zä-ö() -]{0,})(:?,|.)',re.UNICODE)
            m = p.match(unicode(text))

            return {"surname": m.group("surname"), "firstnames": m.group("firstnames"), "cursorLocation": m.end()}
        except Exception as e:
            raise NameException(text)




    def extractBirthday(self, text, cursorLocation, windowWidth = 18):

        try:
            #try to find the date in modified string with regexp
            dateguess = text[cursorLocation:cursorLocation+windowWidth]    #take substring which probably contains the date.
            dateguess = dateguess.replace(" ","")           #remove all whitespace in the substring
            dp = re.compile(ur'.*?(?:s|S|5)\.?(?:(?:(?P<day>\d{1,2})(?:\.|,|:|s)(?P<month>\d{1,2})(?:\.|,|:|s)(?P<year>\d{2,4}))|(?P<yearOnly>\d{2,4})(?!\.|,|\d)(?=\D\D\D\D\D))',re.UNICODE)
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

            if int(year) > 2000 or  int(year) < 1800:
                raise BirthdayException(dateguess)

        except Exception as e:
            #print "----BIRTHDAY----"
            #print dateguess
            #print "---------------------"
            raise BirthdayException(dateguess)


        #find birthplace:
        #locationName = self.extractBirthLocation(text[(m.span()[1]+date.span()[1]):(m.span()[1]+date.span()[1])+24])
        return {"birthDay": date.group("day"),"birthMonth": date.group("month"), "birthYear": year, "cursorLocation": cursorLocation + date.end()}    #, "birthday": m.group(3)


    def extractDeath(self, text, cursorLocation, windowWidth = 16 , forMan=True):

        regexPattern = ur'k(?:(?:(?P<day>\d{1,2})(?:\.|,|:|s)(?P<month>\d{1,2})(?:\.|,|:|s)(?P<year>\d{2,4}))|(?P<yearOnly>\d{2,4})(?!\.|,|\d)(?=\D\D\D\D\D))'
        kaatunut = False
        if forMan:
            #snip the string if there is "Pso" to avoid extracting wife name instead of location name:

            r = re.finditer(ur'(?P<match>pso|ts:|js:)', text, re.IGNORECASE | re.UNICODE)
            endPos = -1
            for m in r:
                endPos = m.start()
                break


            if endPos != -1:
                text = text[0:endPos]


            #check if man has died in war
            k = text.find(" kaat ")
            if k != -1:
                kaatunut = True
                regexPattern = ur'kaat(?:(?:(?P<day>\d{1,2})(?:\.|,|:|s)(?P<month>\d{1,2})(?:\.|,|:|s)(?P<year>\d{2,4}))|(?P<yearOnly>\d{2,4})(?!\.|,|\d)(?=\D\D\D\D\D))'

            #print text

        try:
            #try to find the date in modified string with regexp
            deathLocation = ""
            dateguess = text[cursorLocation:cursorLocation+windowWidth] #text[cursorLocation:cursorLocation+windowWidth]    #take substring which probably contains the date.
            dateguess = dateguess.replace(" ","")           #remove all whitespace in the substring
            dp = re.compile(regexPattern,re.UNICODE)
            date = dp.search(unicode(dateguess))
            #print dateguess


            #get the result from correct capturegroup. If there is full date (12.7.18) it is in 1, if only year it is in 2.
            #could probably be written better in regexp, which uses only one group?
            year = ""
            if date.group("year") == None:
                year = date.group("yearOnly")
            else:
                year = date.group("year")


            year = "19" + year


            try:
                d = self.extractLocation(text, cursorLocation+date.end(), forMan, True)
                cursorLocation = d["cursorLocation"]
                deathLocation = d["location"]  #a misnomer since we use birthlocation function to find the deathlocation. Refactor.
            except Exception as e:
                deathLocation = ""
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
            if f == -1:
                f = text2.find("pso")
            if f != -1:
                text2 = text2[0:f]
        else:
            #snip the string if there is "Pso" to avoid extracting wife name instead of location name:
            text2 = text[cursorLocation:cursorLocation+24]
            f = text2.find("Pso")
            if f == -1:
                f = text2.find("pso")
            if f != -1:
                text2 = text2[0:f]

        try:
            p = re.compile(ur'(?:\d+| s)(?: |,|\.)(?P<location>[A-ZÄ-Ö]{1,1}[A-ZÄ-Öa-zä-ö-]{1,}(?: mlk)?)',re.UNICODE)   #.\d*(?: |,|.)+(?P<location>[A-ZÄ-Ö]{1,1}[A-ZÄ-Öa-zä-ö-]{1,})(,|\.)
            m = p.search(unicode(text2))

            #check if the string has data on death. If it is before the location, be careful to not
            #put the death location to birth location.

            checkDeathp = re.compile(ur'(\bk\b|\bkaat\b)',re.UNICODE)
            checkDeathm = checkDeathp.search(unicode(text2))
            if checkDeathm != None and forDeath == False:
                if checkDeathm.end() < m.end():
                    #print text2
                    #there is entry of death before the matched location. Discard the result:
                    return {"location": "", "cursorLocation": cursorLocation + m.end()}


            return {"location": m.group("location"), "cursorLocation": cursorLocation + m.end()}
        except Exception as e:
            if forMan and forDeath == False:
                self.errorLogger.logError(ManLocationException.eType, self.currentChild )

            raise BirthplaceException(text2)

    #find possible spouses and then call function to extract the data.
    def findSpouses(self, text, cursorLocation):
        text2 = text[cursorLocation-5:]
        spouseWindow = 120
        foundSpouse = False

        #snip the string if there is ts or js markers to avoid taking spouse's old men.
        r = re.finditer(ur'(?P<match>ts:|js:)', text2, re.IGNORECASE | re.UNICODE)
        endPos = -1
        for m in r:
            endPos = m.start()+10
            break
        if endPos != -1:
            text2 = text2[0:endPos]
            print text2


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

                if wife != None:
                    wife["children"] = children
                    wives.append(wife)

            if len(wives) >= 2:
                #raise SpouseException(text, "TOOMUCHWIVES")
                self.errorLogger.logError(TooManyWivesException.eType, self.currentChild)
                #print "Vaimot: " + str(len(wives)) +" " + text2


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
        p = re.compile(ur'\b(?:P|p)so\b(?: \bvst?l?a ?(?P<weddingYear>\d{1,2})\.?)? ?(?P<spouseName>[A-ZÄ-Ö][A-ZÄ-Öa-zä-ö -]+)(?:,|.)',re.UNICODE)
        m = p.search(unicode(text))
        try:
            if m.group("weddingYear") != None:
                weddingYear = int(m.group("weddingYear"))
            else:
                weddingYear = ""
        except Exception as e:
            #raise SpouseException(text, "WEDDINGYEAR")
            self.errorLogger.logError(WeddingException.eType, self.currentChild)


        if m != None:
            try:
                spouseName = m.group("spouseName")
            except Exception as e:
                self.errorLogger.logError(SpouseNameException.eType, self.currentChild)
                #raise SpouseException(text, "SPOUSENAME")
            try:
                if self.currentChild.text.find("Aino Annikki Nevalainen") != -1:
                    print "AINOOOOOO"
                    print text[(m.end()-birthYearWindowLeftOffset):]
                spouseBirthYear = self.extractBirthday(text[(m.end()-birthYearWindowLeftOffset):], 0, 64)
            except ExtractionException as e:
                #raise SpouseException(e.details, "SPOUSEBIRTHDAY")
                self.errorLogger.logError(SpouseBirthdayException.eType, self.currentChild)
                spouseBirthYear = {"birthDay": "","birthMonth": "", "birthYear": "", "cursorLocation": m.end()-birthYearWindowLeftOffset}
                #print text[m.end() + spouseBirthYear["cursorLocation"]-birthYearWindowLeftOffset-10:]
            try:
                #print text[m.end() + spouseBirthYear["cursorLocation"]-birthYearWindowLeftOffset:]
                birthPlace = self.extractLocation(text[m.end():], 0, False)
            except ExtractionException as e:
                #raise SpouseException(e.details, "SPOUSEBIRTHPLACE")
                self.errorLogger.logError(SpouseBirthplaceException.eType, self.currentChild)
                birthPlace= {"location": ""}


            deathData = self.extractDeath(text, m.end(), 40, False)
            return {"cursorLocation": deathData["cursorLocation"], "weddingYear": weddingYear, "spouseName": spouseName, "spouseBirthData": spouseBirthYear, "spouseDeathData": deathData,"spouseBirthLocation": birthPlace["location"]}
        else:
            return None


    #try to find the list of children from the soldier and return it as a single string.
    def findChildren(self, text, cursorLocation):
        text = text[cursorLocation:]
        #print "-----"
        text = re.sub(ur'[:;\!\?\+~¨\^\'\"]', '', text)
        #print text

        p = re.compile(ur'(?:Lapset|Tytär|Poika|Lapsel|Tylär)(?P<children>[A-ZÄ-Öa-zä-ö,0-9,\.\n -]*?)((?:(?:- ?\n?(?=(?:Ts)|(?:Ts)|(?:Js)|(?:JR)|(?:Osa)|(?:Osall)))|pso))',re.UNICODE | re.IGNORECASE) #Removed |(?=pso)
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

            return self.sortChildren( {"children": m.group("children"), "childCount" : len(childList2),"cursorLocation" : cursorLocation + m.end()})
        else:
            #try to find children encoded with numbers words:
            p = re.compile(ur'(?P<count>yksi|kaksi|kolme|neljä|viisi|kuusi|seitsemän|kahdeksan|yhdeksän|kymmenen) (?:lasta|lapsi|tytär|poika)',re.UNICODE | re.IGNORECASE)
            m = p.search(unicode(text))
            numberwords = {"yksi": 1, "kaksi": 2, "kolme": 3, "neljä": 4, "viisi": 5, "kuusi": 6, "seitsemän": 7, "kahdeksan": 8, "yhdeksän": 9, "kymmenen": 10}

            if m != None:
                if m.group("count").lower() in numberwords:
                    #print "Avainsana löytyi: " + str(numberwords[m.group("count").lower()])
                    return {"children": "", "cursorLocation" : cursorLocation, "childCount": numberwords[m.group("count").lower()],  "separated" : {"nyk": "", "miehEd" : "", "psoEd" : ""}}
                else:
                    return {"children": "", "cursorLocation" : cursorLocation, "childCount": 0,  "separated" : {"nyk": "", "miehEd" : "", "psoEd" : ""}}
            else:
                #raise ChildrenException(text)
                if self.currentChild.text.find(u"KATAJISTO") != -1:
                    print text
                    print "KATAJISTO LOL"
                self.errorLogger.logError(ChildrenException.eType, self.currentChild )
                return  {"children": "", "cursorLocation" : cursorLocation, "childCount": 0, "separated" : {"nyk": "", "miehEd" : "", "psoEd" : ""}}

    #sort children based on the marriage they were conceived in
    def sortChildren(self, childdict):


        if self.currentChild.text.find(u"KATAJISTO") != -1:
            print "KATAJISTO"
            print childdict["children"]

        if childdict["childCount"] > 0:
            #try to find keywords:
            psoEdp = re.compile(ur'(?P<psoed>pson ed aviol|pson aik aviol|vaimon I aviol|vaimon ed aviol|rvan ed aviol|pson? I aviol|pson I avioi|miehen I)', re.UNICODE)
            nykp = re.compile(ur'(?P<nykaviol>nyk aviol|nykyis aviol)', re.UNICODE)
            miehEdp = re.compile(ur'(?P<miehed>(?<!n )I aviol|(?<!n )ed aviol|miehen I aviol|(?<!pson )aik aviol|miehen ed aviol|(?<!n )II aviol|(?<!n )II? avlol)', re.UNICODE)

            childText = childdict["children"]
            psoEdm = psoEdp.search(childText)
            nykm = nykp.search(childText)
            miehEdm = miehEdp.search(childText)

            #figure out the positions where each section begins and ends
            substrPositions = []

            if psoEdm != None:
                substrPositions.append({"type" : "psoEd", "begin" : psoEdm.start("psoed"), "end" : psoEdm.end("psoed")})
            if miehEdm != None:
                substrPositions.append({"type" : "miehEd", "begin" : miehEdm.start("miehed"), "end" : miehEdm.end("miehed")})
            if nykm != None:
                substrPositions.append({"type" : "nyk", "begin" : nykm.start("nykaviol"), "end" : nykm.end("nykaviol")})

            #sort list in order of positions in text:
            childPosOrdered = sorted(substrPositions, key=itemgetter("begin"))
            for i in range(0, len(childPosOrdered)):
                if i+1 < len(childPosOrdered):
                    #define the end position of the substring containing the children data. It
                    #is the begnning of the next part or the end of the string.
                    childPosOrdered[i]["childEnd"] = childPosOrdered[i+1]["begin"]
                else:
                    childPosOrdered[i]["childEnd"] = len(childText)

            separatedChildren = {"nyk": "", "miehEd" : "", "psoEd" : ""}

            #if there was text before the first keyword, interpret them as current children:
            if len(childPosOrdered) > 0 and childPosOrdered[0]["begin"] > 0:
                separatedChildren["nyk"] = childText[0:childPosOrdered[0]["begin"]]

            if psoEdm != None or nykm != None or miehEdm != None:
                pass
                #print childPosOrdered


            if len(substrPositions) == 0:
                #TODO: KAIKKI LAPSET NYKYISESTÄ.
                separatedChildren["nyk"] = childText


            for item in childPosOrdered:
                separatedChildren[item["type"]] = childText[item["end"]:item["childEnd"]]
            if len(childPosOrdered) > 0:
                print childText

            childdict["separated"] = separatedChildren
            return childdict

        else:
            childdict["separated"] = {"nyk": "", "miehEd" : "", "psoEd" : ""}
            return childdict


 #check if the count of "Js" and "Ts" makes sense.

    #figure out if the soldier has been in Ts or Js
    def warCheck(self, text):
        findJsRE = re.compile(ur'(?P<jsExists>(?:Js:|JS:|js:|jS:))',re.UNICODE)  #first find out if there is spouse:
        findJsREm = findJsRE.search(unicode(text))

        JsCount = findJsRE.finditer(text)
        JsCount = tuple(JsCount)

        result = {"talvisota": False, "talvisotaregiments": "", "jatkosotaregiments" : "", "jatkosota" : False}
        if len(JsCount) >= 1:
            #find regiments
            result["jatkosotaregiments"] = self.findRegiments(text[JsCount[0].end():])
            result["jatkosota"] = True



        findTsRE = re.compile(ur'(?P<tsExists>(?:Ts:|TS:|ts:|tS:))',re.UNICODE)  #first find out if there is spouse:
        findTsREm = findTsRE.search(unicode(text))

        TsCount = findTsRE.finditer(text)
        TsCount = tuple(TsCount)

        if len(TsCount) >= 1:
            result["talvisotaregiments"] = self.findRegiments(text[TsCount[0].end():])
            result["talvisota"] = True

        return result

    def findRegiments(self, text):
        findRE = re.compile(ur'(?P<regiments>(:?[A-Za-zä-öÄ-Ö0-9 \n,])+)',re.UNICODE)  #first find out if there is spouse:
        findREm = findRE.search(unicode(text))

        #return regiments as string
        if findREm != None:
            return findREm.group("regiments")
        else:
            self.errorLogger.logError(RegimentException.eType, self.currentChild )
            return ""

    #try to find the rank of a soldier
    def findRank(self, text):
        findRankRE = regex.compile(ur'(?:(?:Sotarvo){s<=1}|(?:SOIarvo){s<=1}|(?:Ylenn){s<=1})(?: |\n)(?P<rank>[A-ZÄ-Öa-zä-ö0-9, \n]{2,})(?:\.|:|,| )',re.UNICODE|re.IGNORECASE)  #first find out if there is spouse:
        findRankREm = findRankRE.search(unicode(text))

        if findRankREm != None:
            result = {"rank": findRankREm.group("rank")}
        else:
            #raise RankException(text)
            self.errorLogger.logError(RankException.eType, self.currentChild )
            result = {"rank" : ""}

        return result

    #find if the soldier has some of the most important medals.
    def findMedals(self, text):
        medals = ""

        #find possible spousedata to try to deduce if the medal belongs to man or wife:
        rvaRE = re.compile(ur'(?P<rva>\bRva|\brva)',re.UNICODE)  #first find out if there is spouse:
        rvaREm = rvaRE.search(unicode(text))

        if rvaREm != None:
            rvaPos = rvaREm.start()
        else:
            rvaPos = -1

        #vapauden mitali
        vmRE = re.compile(ur'(?P<mitali>Vm ?1|Vm ?2)',re.UNICODE)  #first find out if there is spouse:
        vmCount = vmRE.finditer(text)

        for match in vmCount:

            if rvaPos != -1:
                if match.start() < rvaPos:
                    medals += match.group("mitali") +","


        #vapauden risti
        vrRE = re.compile(ur'(?P<mitali>VR ?suur|VR ?[1-4](?: [a-zä-ö ]{1,})?|VR ?surur)',re.UNICODE)  #first find out if there is spouse:
        vrCount = vrRE.finditer(text)

        for match in vrCount:
            if rvaPos != -1:
                if match.start() < rvaPos:
                    medals += match.group("mitali") +","


        #suomen vapauden risti
        svrRE = re.compile(ur'(?P<mitali>SVR ?suur|SVR ?[A-Za-zä-ö1-2 ]{1,})',re.UNICODE)  #first find out if there is spouse:
        svrCount = svrRE.finditer(text)

        for match in svrCount:
            if rvaPos != -1:
                if match.start() < rvaPos:
                    medals += match.group("mitali") +","



        return {"medals" : medals}

    def extractKotiutus(self, text):
        text2 = text
        text = text.replace(" ","")           #remove all whitespace in the substring
        text = text.replace("\n","")

        #Extract date
        p = re.compile(ur'(?:Kot|kot|KOI)(?:(?:(?P<day>\d{1,2})(?:\.|,|:|s)(?P<month>\d{1,2})(?:\.|,|:|s)(?P<year>\d{2,4}))|(?P<yearOnly>\d{2,4}(?=\D\D\D\D\D))|(?:(?P<monthName>[a-zä-ö]*)(?P<monthYear>\d{2,4}(?=\D\D\D\D\D))))',re.UNICODE | re.IGNORECASE)
        date = p.search(unicode(text))



        year = ""
        month = ""
        if date != None:
            if date.group("year") == None:

                if date.group("yearOnly") == None:
                    #year and month available
                    year = date.group("monthYear")
                    month = date.group("monthName")
                    #try to map month name to a number.
                    if month in self.monthNameNumberMapping:
                        month = self.monthNameNumberMapping[month]
                    else:
                        month = ""
                else:
                    year = date.group("yearOnly")   #only year available
            else:
                year = date.group("year")
                month = date.group("month")

            #fix years to four digit format.
            year = "19" + year


            try:
                #kotiutusPlace = self.extractLocation(text2, date.end())["location"]
                # customized location extraction:
                lp = re.compile(ur'\A(?P<location>[A-ZÄ-Öa-zä-ö-]+?)(?=[A-ZÄ-Ö.,:])',re.UNICODE)
                place = lp.search(text[date.end():date.end()+100])
                kotiutusPlace = place.group("location")
            except Exception as e:
                self.errorLogger.logError(DemobilizationPlaceException.eType, self.currentChild )
                kotiutusPlace = ""


            return {"kotiutusDay": date.group("day"),"kotiutusMonth": month, "kotiutusYear": year, "kotiutusPlace" : kotiutusPlace}    #, "birthday": m.group(3)
        else:
            self.errorLogger.logError(DemobilizationTimeException.eType, self.currentChild )
            return {"kotiutusDay": "","kotiutusMonth": "", "kotiutusYear": "", "kotiutusPlace" : ""}

    def extractAddress(self, text):

        osRE = re.compile(ur'(?:\W- ?Os\b|\W- ?os\b|\W- ?o5\b|\W- ?O5\b|\W- ?05\b)(?P<address>(?:.|\n)*?)(?=$|Rva|\.)',re.UNICODE | re.IGNORECASE)  #
        osREm = osRE.search(unicode(text))

        if osREm != None:
            address = osREm.group("address")
        else:
            address = ""

        return {"address" : address}

    def extractHobbies(self, text):
        hbRE = re.compile(ur'(?:Harr\b)(?P<hobbies>(?:.|\n)*?)(?=$|Rva|- os\b|\.)',re.UNICODE | re.IGNORECASE)  #
        hbREm = hbRE.search(unicode(text))

        if hbREm != None:
            hobbies = hbREm.group("hobbies")
        else:
            hobbies = ""

        return {"hobbies" : hobbies}

    def extractProfession(self, text):
        p = re.compile(ur'^ ?(?:,|\.| )(?P<profession>[A-ZÄ-Öa-zä-ö !-]+?)(?:\.|,|Pso)',re.UNICODE | re.IGNORECASE)  #
        m = p.search(unicode(text))

        if m != None:
            profession = m.group("profession")
        else:
            #print text
            self.errorLogger.logError(ProfessionException.eType, self.currentChild )
            profession = ""

        return {"profession" : profession}

    def extraction(self, text, xmlElement, eLogger):
        self.errorLogger = eLogger
        self.currentChild = xmlElement
        text = text.replace("\n", ' ')
        text = ' '.join(text.split())   #remove excess whitespace and linebreaks
        personData = {}
        self.parsingLocation = 0
        personData = self.extractPersonName(text)
        personBirthday = self.extractBirthday(text, personData["cursorLocation"])
        personLocation= self.extractLocation(text, personBirthday["cursorLocation"])
        personLocation["birthLocation"] = personLocation["location"]

        profession = self.extractProfession(text[personLocation["cursorLocation"]-4:])
        personDeath = self.extractDeath(text, personBirthday["cursorLocation"], 320)
        spouseData = self.findSpouses(text, personLocation["cursorLocation"])

        #if there is no spouse, try to still find children:
        if spouseData["spouseCount"] == 0:
            children = self.findChildren(text, personLocation["cursorLocation"])
        else:
            children = {}

        #check the wars the soldier has served in:
        wars = self.warCheck(text)
        rank = self.findRank(text)
        medals = self.findMedals(text)
        kotiutus = self.extractKotiutus(text)
        address = self.extractAddress(text)
        hobbies = self.extractHobbies(text)


        #print spouse
        return dict(personData.items() + personBirthday.items() + personLocation.items() + profession.items() + personDeath.items()+ spouseData.items() + children.items() + wars.items() + rank.items() + medals.items() + kotiutus.items() + address.items() + hobbies.items())

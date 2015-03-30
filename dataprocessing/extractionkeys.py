KEYS = {
      "surname" : "Surname",
      "firstnames" : "FirstNames",
      "birthDay" :  "BirthDay",
      "birthMonth" : "BirthMonth",
      "birthYear" : "BirthYear",
      "birthLocation" : "BirthLocation",
      "profession" : "Profession",
      "address" : "Address",
      "deathDay" : "DeathDay",
      "deathMonth" : "DeathMonth",
      "deathYear" : "DeathYear",
      "kaatunut" : "Fallen",
      "deathLocation" : "DeathLocation",
      "talvisota" : "Talvisota",
      "talvisotaregiments" : "TalvisotaRegiments",
      "jatkosota" : "Jatkosota",
      "jatkosotaregiments" : "JatkosotaRegiments",
      "rank": "Rank",
      "kotiutusDay" : "DemobilizationDay",
      "kotiutusMonth" : "DemobilizationMonth",
      "kotiutusYear" : "DemobilizationYear",
      "kotiutusPlace" : "DemobilizationLocation",
      "medals" : "Medals",
      "hobbies" : "Hobbies",
      "hasSpouse" : "HasSpouse",
      "weddingYear" : "WeddingYear",
      "spouseName" : "SpouseName",
      "spouseBirthData" : "SpouseBirthData",
      "spouseDeathData" : "SpouseDeathData",
      "children" : "Children",
      "separated" : "Separated",
      "miehEd" : "ManPreviousMarriage",
      "nyk" : "ManCurrentMarriage",
      "psoEd" : "SpousePreviousMarriage",
      "wifeList" : "Wives",
      "spouseCount" : "SpouseCount",
      "cursorLocation" : "cursorLocation",
      "childCount" : "ChildCount",
      "spouseBirthLocation" : "SpouseBirthLocation",
      "regiments" : "Regiments"


}


class ValueWrapper():
    xmlEntry = None  #Processdata sets this every time before extracting a new Entry.
    idcounter = 1000    #class variable to generate

    @staticmethod
    def reset_id_counter():
        ValueWrapper.idcounter = 1000

    def __init__(self, val):
        self.value = val
        self.id = "t" + str(ValueWrapper.idcounter)
        self.manuallyEdited = False

        if self.id in ValueWrapper.xmlEntry.attrib:
            #there is manual entered value for this field in xml, use it instead
            self.value = ValueWrapper.xmlEntry.attrib[self.id]
            self.manuallyEdited = True
        print(str(self.id) + " " +str(self.value))
        ValueWrapper.idcounter += 1


class ValueWrapper():
    xmlEntry = None     #Processdata sets this every time before extracting a new Entry.
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
        ValueWrapper.idcounter += 1
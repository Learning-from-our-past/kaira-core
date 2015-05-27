class ValueWrapper(object):
    xmlEntry = None     #Processdata sets this every time before extracting a new Entry.
    idcounter = 1000    #class variable to generate

    @staticmethod
    def reset_id_counter():
        ValueWrapper.idcounter = 1000

    def __init__(self, val):
        self._value = val
        self.id = "t" + str(ValueWrapper.idcounter)
        self.manuallyEdited = False
        self.error = False

        if self.id in ValueWrapper.xmlEntry.attrib:
            #there is manual entered value for this field in xml, use it instead
            self._value = ValueWrapper.xmlEntry.attrib[self.id]
            self.manuallyEdited = True

        print(self._value)
        ValueWrapper.idcounter += 1



    def manualEdit(self,val):
        """
        :param val: Meant to manually edit the value from GUI.
        :return:
        """
        self._value = val
        self.manuallyEdited = True

    @property
    def value(self):
        return self._value


    @value.setter
    def value(self, value):
        if not self.manuallyEdited:
            self._value = value



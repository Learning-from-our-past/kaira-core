
class ExtractionException(Exception):
    message = u""
    details = u""
    eType = "OTHER"
    def __init__(self):
       pass

    def __unicode__(self):
        return self.message


class NameException(ExtractionException):
    eType = "NAME"
    message = "ERROR in name extraction: "
    details = u""

    def __init__(self, text):
        self.details = text

    def __unicode__(self):
        return repr(self.message)


class ProfessionException(ExtractionException):
    eType = "PROFESSION"
    message = "ERROR in profession extraction: "
    details = u""

    def __init__(self, text):
        self.details = text

    def __unicode__(self):
        return repr(self.message)

class DateException(ExtractionException):
    eType = "DATE"
    message = "ERROR in date extraction: "
    details = u""

    def __init__(self, text):
        self.details = text


    def __unicode__(self):
        return repr(self.message)

class BirthdayException(ExtractionException):
    eType = "BIRTHDAY"
    message = "ERROR in birthday extraction: "
    details = u""

    def __init__(self, dateguess):
        self.details = dateguess

    def __unicode__(self):
        return repr(self.message)


class BirthLocationException(ExtractionException):
    eType = "BIRTHLOCATION MISSING"
    message = "ERROR in location extraction: "
    details = u""

    def __init__(self, text, type):
        self.details = text
        self.eType = type

    def __unicode__(self):
        return repr(self.message)

class LocationException(ExtractionException):
    eType = "LOCATION"
    message = "ERROR in location extraction: "
    details = u""

    def __init__(self, text):
        self.details = text


    def __unicode__(self):
        return repr(self.message)

class SpouseNameException(ExtractionException):
    eType = "SPOUSENAME"
    message = "ERROR in spouse name extraction: "
    details = u""

    def __init__(self, text):
        self.details = text


    def __unicode__(self):
        return repr(self.message)

class MultipleMarriagesException(ExtractionException):
    eType = "MAYBE CHILDREN FROM MANY MARRIAGES"
    message = "Found words to indicate previous marriages: "
    details = u""

    def __init__(self, text):
        self.details = text


    def __unicode__(self):
        return repr(self.message)


class KarelianLocationException(ExtractionException):
    eType = "KARELIAN LOCATION"
    message = "ERROR in karelian location extraction: "
    details = u""

    def __init__(self, text):
        self.details = text


    def __unicode__(self):
        return repr(self.message)

class NoChildrenException(ExtractionException):
    eType = "NO CHILDREN FOUND"
    message = "ERROR in children extraction: "
    details = u""

    def __init__(self, text):
        self.details = text


    def __unicode__(self):
        return repr(self.message)

class OtherLocationException(ExtractionException):
    eType = "OTHER LOCATION"
    message = "ERROR in other location extraction: "
    details = u""

    def __init__(self, text):
        self.details = text


    def __unicode__(self):
        return repr(self.message)


class OwnerYearException(ExtractionException):
    eType = "NO OWNERSHIP YEAR"
    message = "ERROR in ownership year: "
    details = u""

    def __init__(self, text):
        self.details = text


    def __unicode__(self):
        return repr(self.message)

class OwnerNameException(ExtractionException):
    eType = "NO OWNER NAME FOUND"
    message = "ERROR in ownership name: "
    details = u""

    def __init__(self, text):
        self.details = text


    def __unicode__(self):
        return repr(self.message)


class HostessNameException(ExtractionException):
    eType = "NO HOSTESS NAME FOUND"
    message = "ERROR in hostess name: "
    details = u""

    def __init__(self, text):
        self.details = text


    def __unicode__(self):
        return repr(self.message)
# -*- coding: utf-8 -*-

class ExtractionException(Exception):
    message = u""
    details = u""
    eType = "OTHER"
    def __init__(self):
       pass

    def __unicode__(self):
        return self.message

class BirthdayException(ExtractionException):
    eType = "BIRTHDAY"
    message = "ERROR in birthday extraction: "
    details = u""

    def __init__(self, dateguess):
        self.details = dateguess

    def __unicode__(self):
        return repr(self.message)

class BirthplaceException(ExtractionException):
    eType = "BIRTHPLACE"
    message = "ERROR in birthplace extraction: "
    details = u""

    def __init__(self, dateguess):
        self.details = dateguess

    def __unicode__(self):
        return repr(self.message)

class NameException(ExtractionException):
    eType = "NAME"
    message = "ERROR in name extraction: "
    details = u""

    def __init__(self, text):
        self.details = text

    def __unicode__(self):
        return repr(self.message)

class WeddingException(ExtractionException):
    eType = "WEDDING OR SPOUSENAME"
    message = "ERROR in wedding extraction: "
    details = u""

    def __init__(self, text):
        self.details = text

    def __unicode__(self):
        return repr(self.message)

class SpouseException(ExtractionException):
    eType = "SPOUSE"
    message = "ERROR in spouse extraction: "
    details = u""


    def __init__(self, text, type):
        self.details = text
        self.eType = type

    def __unicode__(self):
        return repr(self.message)

class TooManyWivesException(ExtractionException):
    eType = "TOOMANYWIVES"
    message = "ERROR in spouse extraction: "
    details = u""


    def __init__(self, text, type):
        self.details = text
        self.eType = type

    def __unicode__(self):
        return repr(self.message)

class SpouseNameException(ExtractionException):
    eType = "SPOUSENAME"
    message = "ERROR in spouse extraction: "
    details = u""

    def __init__(self, text, type):
        self.details = text
        self.eType = type

    def __unicode__(self):
        return repr(self.message)

class SpouseBirthplaceException(ExtractionException):
    eType = "SPOUSEBIRTHPLACE"
    message = "ERROR in spouse extraction: "
    details = u""


    def __init__(self, text, type):
        self.details = text
        self.eType = type

    def __unicode__(self):
        return repr(self.message)

class SpouseBirthdayException(ExtractionException):
    eType = "SPOUSEBIRTHDAY"
    message = "ERROR in spouse extraction: "
    details = u""


    def __init__(self, text, type):
        self.details = text
        self.eType = type

    def __unicode__(self):
        return repr(self.message)

class ChildrenException(ExtractionException):
    eType = "NOCHILDREN"
    message = "ERROR in child extraction: "
    details = u""

    def __init__(self, text):
        self.details = text

    def __unicode__(self):
        return repr(self.message)


class RankException(ExtractionException):
    eType = "RANK"
    message = "ERROR in rank extraction: "
    details = u""

    def __init__(self, text):
        self.details = text

    def __unicode__(self):
        return repr(self.message)

class DemobilizationPlaceException(ExtractionException):
    eType = "DEMOBILIZATIONPLACE"
    message = "ERROR in Demobilization extraction: "
    details = u""

    def __init__(self, text):
        self.details = text

    def __unicode__(self):
        return repr(self.message)

class DemobilizationTimeException(ExtractionException):
    eType = "DEMOBILIZATIONTIME"
    message = "ERROR in Demobilization extraction: "
    details = u""

    def __init__(self, text):
        self.details = text

    def __unicode__(self):
        return repr(self.message)


class RegimentException(ExtractionException):
    eType = "REGIMENT"
    message = "ERROR in regiment extraction: "
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



class ManLocationException(ExtractionException):
    eType = "MANLOCATION"
    message = "ERROR in location extraction: "
    details = u""

    def __init__(self, text, type):
        self.details = text
        self.eType = type

    def __unicode__(self):
        return repr(self.message)


class DateException(ExtractionException):
    eType = "DATE"
    message = "ERROR in date extraction: "
    details = u""

    def __init__(self, text):
        self.details = text
        self.eType = type

    def __unicode__(self):
        return repr(self.message)



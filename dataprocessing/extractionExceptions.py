# -*- coding: utf-8 -*-

class ExtractionException(Exception):
    message = u""
    details = u""
    eType = u""
    def __init__(self):
       pass

    def __unicode__(self):
        return self.message

class BirthdayException(ExtractionException):
    message = "ERROR in birthday extraction: "
    details = u""

    def __init__(self, dateguess):
        self.details = dateguess

    def __unicode__(self):
        return repr(self.message)

class BirthplaceException(ExtractionException):
    message = "ERROR in birthplace extraction: "
    details = u""

    def __init__(self, dateguess):
        self.details = dateguess

    def __unicode__(self):
        return repr(self.message)

class NameException(ExtractionException):
    message = "ERROR in name extraction: "
    details = u""

    def __init__(self, text):
        self.details = text

    def __unicode__(self):
        return repr(self.message)

class SpouseException(ExtractionException):
    message = "ERROR in spouse extraction: "
    details = u""
    eType = u""

    def __init__(self, text, type):
        self.details = text
        self.eType = type

    def __unicode__(self):
        return repr(self.message)

class ChildrenException(ExtractionException):
    message = "ERROR in child extraction: "
    details = u""

    def __init__(self, text):
        self.details = text

    def __unicode__(self):
        return repr(self.message)


class RankException(ExtractionException):
    message = "ERROR in rank extraction: "
    details = u""

    def __init__(self, text):
        self.details = text

    def __unicode__(self):
        return repr(self.message)

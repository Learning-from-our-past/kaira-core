# -*- coding: utf-8 -*-

class ExtractionException(Exception):
    message = u""
    details = u""
    def __init__(self):
       pass

    def __unicode__(self):
        return self.message

class BirthdayException(ExtractionException):
    message = u"ERROR in birthday extraction: "
    details = u""

    def __init__(self, dateguess):
        self.details = dateguess

    def __unicode__(self):
        return repr(self.message)

class BirthplaceException(ExtractionException):
    message = u"ERROR in birthplace extraction: "
    details = u""

    def __init__(self, dateguess):
        self.details = dateguess

    def __unicode__(self):
        return repr(self.message)

class NameException(ExtractionException):
    message = u"ERROR in name extraction: "
    details = u""

    def __init__(self, text):
        self.details = text

    def __unicode__(self):
        return repr(self.message)




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
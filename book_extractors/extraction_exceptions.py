
class ExtractionException(Exception):
    message = u""
    details = u""
    eType = "OTHER"

    def __init__(self):
       pass

    def __unicode__(self):
        return self.message

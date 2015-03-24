# -*- coding: utf-8 -*-

class ExceptionLogger:

    def __init__(self):
        self.errorsListing = {}

    def logError(self, exceptionType, entry):
        if exceptionType in self.errorsListing:
            self.errorsListing[exceptionType].append(entry)
        else:
            self.errorsListing[exceptionType] = [entry]

    def printErrorBreakdown(self):
        print ("ERROR breakdown: ")
        for key, value in self.errorsListing.items():
            print (key)
            print (len(value))

    def getErrors(self):
        return self.errorsListing
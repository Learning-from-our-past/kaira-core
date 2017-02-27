
class MockExceptionLogger:
    """
    Mock class for logging exceptions from extractors.
    """

    def __init__(self):
        self.errors_listing = {}

    def logError(self, exception_type, entry):
        if exception_type in self.errors_listing:
            self.errors_listing[exception_type].append(entry)
        else:
            self.errors_listing[exception_type] = [entry]

    def printErrorBreakdown(self):
        print ("ERROR breakdown: ")
        for key, value in self.errors_listing.items():
            print (key)
            print (len(value))

    def getErrors(self):
        return self.errors_listing
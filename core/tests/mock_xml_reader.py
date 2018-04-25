class MockXMLStreamer:
    def __init__(self, data):
        self.data = data

    def read_entry_from_xml(self):
        for item in self.data:
            yield item

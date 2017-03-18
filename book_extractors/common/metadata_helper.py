

class MetadataCollector:

    def __init__(self):
        self._metadata_attributes = {'errors': {}}

    def clear(self):
        self._metadata_attributes = {'errors': {}}

    def get_metadata(self):
        metadata = self._metadata_attributes
        return metadata

    def set_metadata_property(self, key, value):
        self._metadata_attributes[key] = value

    def add_error_record(self, name, severity):
        """
        Add entry to metadata's errors object. Severity level can be used to imply the
        requirement for human review related to reason of the error.
        :param name:
        :param severity: Severity level in range of 0-10
        :return:
        """
        self._metadata_attributes['errors'][name] = severity

import regex
from core.pipeline_construction.base_extractor import BaseExtractor


class NameExtractor(BaseExtractor):
    extraction_key = 'name'

    def __init__(self, cursor_location_depends_on=None, options=None):
        super(NameExtractor, self).__init__(cursor_location_depends_on, options)

        flags = regex.UNICODE | regex.IGNORECASE
        # Match both last and first names of a person from the beginning of the text entry.
        # Use commas as a separator character to stop match or a lonely s letter which most likely stands
        # for word "syntynyt" (meaning that we have already passed the name)
        last_name_pattern = '(?P<last_name>[A-ZÄÖ -]+)'
        # Use non greed matcher to avoid taking in possible ending character s (for syntyneet word)
        first_name_pattern = '(?P<first_names>[\w ()-]+?)'
        name_pattern = '^{}(?:,|\.|\(.*\),){}(?:,|\ss|\d)'.format(
            last_name_pattern, first_name_pattern
        )
        self._LAST_NAME_REGEX = regex.compile(name_pattern, flags)

    def _extract(self, entry, extraction_results, extraction_metadata):
        results, cursor_location = self._find_names(entry)
        results['sex'] = 'Male'  # All soldiers were men

        return self._add_to_extraction_results(
            results, extraction_results, extraction_metadata, cursor_location
        )

    def _find_names(self, entry):
        match = self._LAST_NAME_REGEX.search(entry['text'])
        result = {'firstNames': None, 'lastName': None}

        if match is not None:
            result['firstNames'] = match.group('first_names')
            result['lastName'] = match.group('last_name')
            return self._trim_names(result), match.endpos
        else:
            return result, 0

    def _trim_names(self, names):
        names['firstNames'] = names['firstNames'].strip()
        names['lastName'] = regex.sub(r'\s', '', names['lastName'])
        return names

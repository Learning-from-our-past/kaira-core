import regex
from extractors.common.extractors.birthday_extractor import CommonBirthdayExtractor


class BirthdayExtractor(CommonBirthdayExtractor):
    extraction_key = 'birthday'

    def __init__(self, cursor_location_depends_on=None, options=None):
        if options is None:
            options = {'remove_spaces': False}

        options[
            'PATTERN'
        ] = r's\.?\s?(?:(?:(?P<day>\d{1,2})(?:[.,:])(?P<month>\d{1,2})(?:[.,:])\s?(?P<year>\d{2,4}))|(?P<monthName>\w+)\s?(?P<monthYear>\d{2,4}))'
        super().__init__(cursor_location_depends_on, options)

    def _extract(self, entry, extraction_results, extraction_metadata):
        clipped_entry = entry.copy()
        clipped_entry['text'] = self._clip_entry_string_before_spouse_keyword(entry)

        return super(BirthdayExtractor, self)._extract(
            clipped_entry, extraction_results, extraction_metadata
        )

    def _clip_entry_string_before_spouse_keyword(self, entry):
        """
        Sometimes soldiers do not have birth dates and that is ok. To prevent taking birth dates of spouses
        we should stop search if we encounter keywords which indicate the start of spouse's information.
        :return:
        """
        spouse_marker_match = regex.search(
            r'\sPso(?:[\s.])', entry['text'], flags=regex.IGNORECASE
        )

        if spouse_marker_match:
            return entry['text'][0 : spouse_marker_match.start()]

        return entry['text']

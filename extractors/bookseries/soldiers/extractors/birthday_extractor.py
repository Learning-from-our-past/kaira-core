from extractors.common.extractors.birthday_extractor import CommonBirthdayExtractor


class BirthdayExtractor(CommonBirthdayExtractor):
    extraction_key = 'birthday'

    def __init__(self, cursor_location_depends_on=None, options=None):
        if options is None:
            options = {'remove_spaces': False}

        options['PATTERN'] = r's\.?\s?(?:(?:(?P<day>\d{1,2})(?:[.,:])(?P<month>\d{1,2})(?:[.,:])\s?(?P<year>\d{2,4}))|(?P<monthName>\w+)\s?(?P<monthYear>\d{2,4}))'
        super().__init__(cursor_location_depends_on, options)

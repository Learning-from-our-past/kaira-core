from book_extractors.common.extractors.base_extractor import BaseExtractor


class KairaIdExtractor(BaseExtractor):
    extraction_key = 'kairaId'
    _id_num = 1

    def __init__(self, key_of_cursor_location_dependent, options):
        super(KairaIdExtractor, self).__init__(key_of_cursor_location_dependent, options)

        self.bookseries = options['bookseries']
        self.book_number = options['book_number']

    def _extract(self, entry, extraction_results):
        # Form of the id: <bookseries>_<bookNumber>_<id_num>
        full_id = '{}_{}_{}'.format(self.bookseries, self.book_number, KairaIdExtractor._id_num)
        KairaIdExtractor._id_num += 1

        return self._add_to_extraction_results(full_id, extraction_results)

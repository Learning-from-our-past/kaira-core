from book_extractors.common.extractors.base_extractor import BaseExtractor
import book_extractors.extraction_constants as extraction_constants


class KairaIdProvider():
    _id_num = 1

    _allowed_person_types = {
        'P': 'primary',
        'S': 'spouse',
        'C': 'child'
    }

    def reset(self):
        KairaIdProvider._id_num = 1

    def get_new_id(self, person_type='P'):
        if person_type not in KairaIdProvider._allowed_person_types:
            raise Exception('Not a proper person type for kairaId assigned.')

        full_id = '{}_{}_{}{}'.format(extraction_constants.BOOK_SERIES, extraction_constants.BOOK_NUMBER, KairaIdProvider._id_num, person_type)
        KairaIdProvider._id_num += 1

        return full_id


class KairaIdExtractor(BaseExtractor):
    extraction_key = 'kairaId'

    def __init__(self, key_of_cursor_location_dependent, options):
        super(KairaIdExtractor, self).__init__(key_of_cursor_location_dependent, options)
        self._provider = KairaIdProvider()

    def _extract(self, entry, extraction_results):
        # Form of the id: <bookseries>_<bookNumber>_<id_num>
        full_id = self._provider.get_new_id()

        return self._add_to_extraction_results(full_id, extraction_results)

from core.base_extractor import BaseExtractor
import core.extraction_constants as extraction_constants


class KairaIdProvider:
    _main_id_num = 1
    _children_id_num = 1
    _spouse_id_num = 1

    _allowed_person_types = {
        'P': 'primary',
        'S': 'spouse',
        'C': 'child'
    }

    def reset(self):
        KairaIdProvider._main_id_num = 1
        KairaIdProvider._children_id_num = 1
        KairaIdProvider._spouse_id_num = 1

    def get_new_id(self, person_type='P'):
        if person_type not in KairaIdProvider._allowed_person_types:
            raise Exception('Not a proper person type for kairaId assigned.')

        if person_type == 'P':
            KairaIdProvider._children_id_num = 1
            KairaIdProvider._spouse_id_num = 1

            full_id = '{}_{}_{}{}'.format(extraction_constants.BOOK_SERIES, extraction_constants.BOOK_NUMBER,
                                          KairaIdProvider._main_id_num, person_type)
            KairaIdProvider._main_id_num += 1

        if person_type == 'S':
            full_id = '{}_{}_{}{}_{}'.format(extraction_constants.BOOK_SERIES, extraction_constants.BOOK_NUMBER,
                                             KairaIdProvider._main_id_num, person_type, KairaIdProvider._spouse_id_num)
            KairaIdProvider._spouse_id_num += 1

        if person_type == 'C':
            full_id = '{}_{}_{}{}_{}'.format(extraction_constants.BOOK_SERIES, extraction_constants.BOOK_NUMBER,
                                             KairaIdProvider._main_id_num, person_type, KairaIdProvider._children_id_num)
            KairaIdProvider._children_id_num += 1

        return full_id


class KairaIdExtractor(BaseExtractor):
    extraction_key = 'kairaId'

    def __init__(self, cursor_location_depends_on=None, options=None):
        super(KairaIdExtractor, self).__init__(cursor_location_depends_on, options)
        self._provider = KairaIdProvider()

    def _extract(self, entry, extraction_results, extraction_metadata):
        # Form of the id: <bookseries>_<bookNumber>_<id_num>
        full_id = self._provider.get_new_id()

        return self._add_to_extraction_results(full_id, extraction_results, extraction_metadata)

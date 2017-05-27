from book_extractors.karelians.extraction.postprocessors.returned_to_karelia import check_if_person_returned_karelia_in_between_wars
import pytest
from random import shuffle


class TestReturnedToKareliaCheck:

    def should_return_true_when_person_moved_to_karelian_region_in_between_1940_and_1944_if_they_were_in_karelia_before(self):
        data = [
            {'locationName': 'Kuolemajärvi', 'region': 'karelia', 'movedIn': None, 'movedOut': 39},
            {'locationName': 'Urjala', 'region': 'other', 'movedIn': 39, 'movedOut': 42},
            {'locationName': 'Kuolemajärvi', 'region': 'karelia', 'movedIn': 42, 'movedOut': 44},
            {'locationName': 'Piikkiö', 'region': 'other', 'movedIn': 44, 'movedOut': None}
        ]

        shuffle(data)   # Make sure the order of records does not matter

        returned_to_karelia = check_if_person_returned_karelia_in_between_wars(data)
        assert returned_to_karelia is True

    def should_return_false_when_person_moved_to_karelian_region_in_between_1940_and_1944_but_did_not_live_there_before(self):
        data = [
            {'locationName': 'Helsinki', 'region': 'other', 'movedIn': None, 'movedOut': 39},
            {'locationName': 'Urjala', 'region': 'other', 'movedIn': 39, 'movedOut': 42},
            {'locationName': 'Kuolemajärvi', 'region': 'karelia', 'movedIn': 42, 'movedOut': 44},
            {'locationName': 'Piikkiö', 'region': 'other', 'movedIn': 44, 'movedOut': None}
        ]

        shuffle(data)  # Make sure the order of records does not matter

        returned_to_karelia = check_if_person_returned_karelia_in_between_wars(data)
        assert returned_to_karelia is False

    def should_return_false_if_person_did_not_move_to_karelia_in_between_1940_and_1944(self):
        data = [
            {'locationName': 'Kuolemajärvi', 'region': 'karelia', 'movedIn': None, 'movedOut': 39},
            {'locationName': 'Urjala', 'region': 'other', 'movedIn': 39, 'movedOut': 42},
            {'locationName': 'Jyväskylä', 'region': 'other', 'movedIn': 42, 'movedOut': 44},
            {'locationName': 'Piikkiö', 'region': 'other', 'movedIn': 44, 'movedOut': None}
        ]

        shuffle(data)  # Make sure the order of records does not matter

        returned_to_karelia = check_if_person_returned_karelia_in_between_wars(data)
        assert returned_to_karelia is False

    def should_return_None_if_no_year_data_available(self):
        data = [
            {'locationName': 'Kuolemajärvi', 'region': 'karelia', 'movedIn': None, 'movedOut': None},
            {'locationName': 'Urjala', 'region': 'other', 'movedIn': None, 'movedOut': None},
            {'locationName': 'Jyväskylä', 'region': 'other', 'movedIn': None, 'movedOut': None},
            {'locationName': 'Piikkiö', 'region': 'other', 'movedIn': None, 'movedOut': None}
        ]

        shuffle(data)  # Make sure the order of records does not matter

        returned_to_karelia = check_if_person_returned_karelia_in_between_wars(data)
        assert returned_to_karelia is None

    def should_return_None_if_result_would_be_false_with_some_karelian_locations_missing_year_data(self):
        data = [
            {'locationName': 'Kuolemajärvi', 'region': 'karelia', 'movedIn': None, 'movedOut': 39},
            {'locationName': 'Urjala', 'region': 'other', 'movedIn': 39, 'movedOut': 42},
            {'locationName': 'Kuolemajärvi', 'region': 'karelia', 'movedIn': None, 'movedOut': None},   # Ambiguous entry, so can't resolve returning
            {'locationName': 'Piikkiö', 'region': 'other', 'movedIn': 44, 'movedOut': None}
        ]

        shuffle(data)  # Make sure the order of records does not matter

        returned_to_karelia = check_if_person_returned_karelia_in_between_wars(data)
        assert returned_to_karelia is None

    @pytest.mark.skip()
    def should_return_true_if_returned_to_karelia_can_be_deduced_when_movedIn_is_missing_from_other_migration_records(self):
        """
           TODO: How about the case where:
           {'locationName': 'Kuolemajärvi', 'region': 'karelia', 'movedIn': None, 'movedOut': 44},
           and person has previous migration history in somewhere else? If movedIn year is not recorded but movedOut is, and
           it hits to sensible range? Conditions would be something like:

           1) Lived in karelia before
           2) Then moved out of 'other' place in range in 40-44 and karelian location is the next in line with movedOut after previous movedOut
           3) Next location is 'other'

        """

        data = [
            {'locationName': 'Kuolemajärvi', 'region': 'karelia', 'movedIn': None, 'movedOut': 39},
            {'locationName': 'Urjala', 'region': 'other', 'movedIn': 39, 'movedOut': 42},
            {'locationName': 'Kuolemajärvi', 'region': 'karelia', 'movedIn': None, 'movedOut': 44},
            {'locationName': 'Piikkiö', 'region': 'other', 'movedIn': 44, 'movedOut': None}
        ]

        shuffle(data)  # Make sure the order of records does not matter

        returned_to_karelia = check_if_person_returned_karelia_in_between_wars(data)
        assert returned_to_karelia is True


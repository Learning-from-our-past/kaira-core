from extractors.bookseries.karelians.postprocessors.returned_to_karelia import (
    check_if_person_returned_karelia_in_between_wars,
)
from random import shuffle


class TestReturnedToKareliaCheck:
    def should_return_true_when_person_moved_to_karelian_region_in_between_1940_and_1944_if_they_were_in_karelia_before(
        self,
    ):
        data = [
            {
                'locationName': 'Kuolemajärvi',
                'region': 'karelia',
                'movedIn': None,
                'movedOut': 39,
            },
            {
                'locationName': 'Urjala',
                'region': 'other',
                'movedIn': 39,
                'movedOut': 42,
            },
            {
                'locationName': 'Kuolemajärvi',
                'region': 'karelia',
                'movedIn': 42,
                'movedOut': 44,
            },
            {
                'locationName': 'Piikkiö',
                'region': 'other',
                'movedIn': 44,
                'movedOut': None,
            },
        ]

        shuffle(data)  # Make sure the order of records does not matter

        returned_to_karelia = check_if_person_returned_karelia_in_between_wars(data)
        assert returned_to_karelia is True

    def should_return_false_when_person_moved_to_karelian_region_in_between_1940_and_1944_but_did_not_live_there_before(
        self,
    ):
        data = [
            {
                'locationName': 'Helsinki',
                'region': 'other',
                'movedIn': None,
                'movedOut': 39,
            },
            {
                'locationName': 'Urjala',
                'region': 'other',
                'movedIn': 39,
                'movedOut': 42,
            },
            {
                'locationName': 'Kuolemajärvi',
                'region': 'karelia',
                'movedIn': 42,
                'movedOut': 44,
            },
            {
                'locationName': 'Piikkiö',
                'region': 'other',
                'movedIn': 44,
                'movedOut': None,
            },
        ]

        shuffle(data)  # Make sure the order of records does not matter

        returned_to_karelia = check_if_person_returned_karelia_in_between_wars(data)
        assert returned_to_karelia is False

    def should_return_false_if_person_did_not_move_to_karelia_in_between_1940_and_1944(
        self,
    ):
        data = [
            {
                'locationName': 'Kuolemajärvi',
                'region': 'karelia',
                'movedIn': None,
                'movedOut': 39,
            },
            {
                'locationName': 'Urjala',
                'region': 'other',
                'movedIn': 39,
                'movedOut': 42,
            },
            {
                'locationName': 'Jyväskylä',
                'region': 'other',
                'movedIn': 42,
                'movedOut': 44,
            },
            {
                'locationName': 'Piikkiö',
                'region': 'other',
                'movedIn': 44,
                'movedOut': None,
            },
        ]

        shuffle(data)  # Make sure the order of records does not matter

        returned_to_karelia = check_if_person_returned_karelia_in_between_wars(data)
        assert returned_to_karelia is False

    def should_return_None_if_no_year_data_available(self):
        data = [
            {
                'locationName': 'Kuolemajärvi',
                'region': 'karelia',
                'movedIn': None,
                'movedOut': None,
            },
            {
                'locationName': 'Urjala',
                'region': 'other',
                'movedIn': None,
                'movedOut': None,
            },
            {
                'locationName': 'Jyväskylä',
                'region': 'other',
                'movedIn': None,
                'movedOut': None,
            },
            {
                'locationName': 'Piikkiö',
                'region': 'other',
                'movedIn': None,
                'movedOut': None,
            },
        ]

        shuffle(data)  # Make sure the order of records does not matter

        returned_to_karelia = check_if_person_returned_karelia_in_between_wars(data)
        assert returned_to_karelia is None

    def should_return_None_if_result_would_be_false_with_some_karelian_locations_missing_year_data(
        self,
    ):
        data = [
            {
                'locationName': 'Kuolemajärvi',
                'region': 'karelia',
                'movedIn': None,
                'movedOut': 39,
            },
            {
                'locationName': 'Urjala',
                'region': 'other',
                'movedIn': 39,
                'movedOut': 42,
            },
            {
                'locationName': 'Kuolemajärvi',
                'region': 'karelia',
                'movedIn': None,
                'movedOut': None,
            },  # Ambiguous entry, so can't resolve returning
            {
                'locationName': 'Piikkiö',
                'region': 'other',
                'movedIn': 44,
                'movedOut': None,
            },
        ]

        shuffle(data)  # Make sure the order of records does not matter

        returned_to_karelia = check_if_person_returned_karelia_in_between_wars(data)
        assert returned_to_karelia is None

    def should_return_correct_values_with_different_migration_histories(self):
        data = [
            {
                'movedIn': 38,
                'movedOut': None,
                'locationName': 'Impilahti',
                'region': 'karelia',
            },
            {
                'movedIn': 39,
                'movedOut': None,
                'locationName': 'Viinijärvi',
                'region': 'other',
            },
            {
                'movedIn': 40,
                'movedOut': 41,
                'locationName': 'Riistavesi',
                'region': 'other',
            },
            {
                'movedIn': None,
                'movedOut': 44,
                'locationName': 'Impilahti',
                'region': 'karelia',
            },
            {
                'movedIn': 44,
                'movedOut': None,
                'locationName': 'Alajärvi',
                'region': 'other',
            },
        ]

        shuffle(data)  # Make sure the order of records does not matter
        returned_to_karelia = check_if_person_returned_karelia_in_between_wars(data)
        assert returned_to_karelia is True

    def should_return_true_if_returned_to_karelia_can_be_deduced_when_movedIn_is_missing_from_other_migration_records(
        self,
    ):
        data = [
            {
                'locationName': 'Hiitola',
                'region': 'karelia',
                'movedIn': None,
                'movedOut': 39,
            },
            {
                'locationName': 'Parkano',
                'region': 'other',
                'movedIn': 39,
                'movedOut': None,
            },
            {
                'locationName': 'Hiitola',
                'region': 'karelia',
                'movedIn': None,
                'movedOut': 44,
            },
            {
                'locationName': 'Vaasa',
                'region': 'other',
                'movedIn': None,
                'movedOut': 44,
            },
            {
                'locationName': 'Ahlainen',
                'region': 'other',
                'movedIn': 48,
                'movedOut': None,
            },
        ]

        shuffle(data)  # Make sure the order of records does not matter
        returned_to_karelia = check_if_person_returned_karelia_in_between_wars(data)
        assert returned_to_karelia is True

        data = [
            {
                'movedIn': None,
                'movedOut': 44,
                'locationName': 'Impilahti',
                'region': 'karelia',
            },
            {
                'movedIn': None,
                'movedOut': 39,
                'locationName': 'Impilahti',
                'region': 'karelia',
            },
            {
                'movedIn': 39,
                'movedOut': 40,
                'locationName': 'Viinijärvi',
                'region': 'other',
            },
            {
                'movedIn': 40,
                'movedOut': 41,
                'locationName': 'Riistavesi',
                'region': 'other',
            },
            {
                'movedIn': 44,
                'movedOut': None,
                'locationName': 'Alajärvi',
                'region': 'other',
            },
        ]

        shuffle(data)  # Make sure the order of records does not matter
        returned_to_karelia = check_if_person_returned_karelia_in_between_wars(data)
        assert returned_to_karelia is True

        data = [
            {
                'locationName': 'Kuolemajärvi',
                'region': 'karelia',
                'movedIn': None,
                'movedOut': 39,
            },
            {
                'locationName': 'Urjala',
                'region': 'other',
                'movedIn': 39,
                'movedOut': 42,
            },
            {
                'locationName': 'Kuolemajärvi',
                'region': 'karelia',
                'movedIn': None,
                'movedOut': 44,
            },
            {
                'locationName': 'Piikkiö',
                'region': 'other',
                'movedIn': 44,
                'movedOut': None,
            },
        ]

        shuffle(data)  # Make sure the order of records does not matter
        returned_to_karelia = check_if_person_returned_karelia_in_between_wars(data)
        assert returned_to_karelia is True

        data = [
            {
                'movedIn': None,
                'movedOut': 39,
                'locationName': 'Impilahti',
                'region': 'karelia',
            },
            {
                'movedIn': 39,
                'movedOut': None,
                'locationName': 'Viinijärvi',
                'region': 'other',
            },
            {
                'movedIn': 40,
                'movedOut': 41,
                'locationName': 'Riistavesi',
                'region': 'other',
            },
            {
                'movedIn': None,
                'movedOut': 44,
                'locationName': 'Impilahti',
                'region': 'karelia',
            },
            {
                'movedIn': 44,
                'movedOut': None,
                'locationName': 'Alajärvi',
                'region': 'other',
            },
        ]

        shuffle(data)  # Make sure the order of records does not matter
        returned_to_karelia = check_if_person_returned_karelia_in_between_wars(data)
        assert returned_to_karelia is True

        data = [
            {
                'movedIn': 38,
                'movedOut': None,
                'locationName': 'Impilahti',
                'region': 'karelia',
            },
            {
                'movedIn': 39,
                'movedOut': None,
                'locationName': 'Viinijärvi',
                'region': 'other',
            },
            {
                'movedIn': 40,
                'movedOut': 41,
                'locationName': 'Riistavesi',
                'region': 'other',
            },
            {
                'movedIn': None,
                'movedOut': 44,
                'locationName': 'Impilahti',
                'region': 'karelia',
            },
            {
                'movedIn': 44,
                'movedOut': None,
                'locationName': 'Alajärvi',
                'region': 'other',
            },
        ]

        shuffle(data)  # Make sure the order of records does not matter
        returned_to_karelia = check_if_person_returned_karelia_in_between_wars(data)
        assert returned_to_karelia is True

        data = [
            {
                'movedIn': None,
                'movedOut': 39,
                'locationName': 'Impilahti',
                'region': 'karelia',
            },
            {
                'movedIn': None,
                'movedOut': 40,
                'locationName': 'Viinijärvi',
                'region': 'other',
            },
            {
                'movedIn': None,
                'movedOut': 41,
                'locationName': 'Riistavesi',
                'region': 'other',
            },
            {
                'movedIn': None,
                'movedOut': 44,
                'locationName': 'Impilahti',
                'region': 'karelia',
            },
            {
                'movedIn': None,
                'movedOut': 46,
                'locationName': 'Alajärvi',
                'region': 'other',
            },
        ]

        shuffle(data)  # Make sure the order of records does not matter
        returned_to_karelia = check_if_person_returned_karelia_in_between_wars(data)
        assert returned_to_karelia is True

        data = [
            {
                'movedIn': 38,
                'movedOut': None,
                'locationName': 'Impilahti',
                'region': 'karelia',
            },
            {
                'movedIn': 39,
                'movedOut': None,
                'locationName': 'Viinijärvi',
                'region': 'other',
            },
            {
                'movedIn': 40,
                'movedOut': None,
                'locationName': 'Riistavesi',
                'region': 'other',
            },
            {
                'movedIn': 42,
                'movedOut': None,
                'locationName': 'Impilahti',
                'region': 'karelia',
            },
            {
                'movedIn': 44,
                'movedOut': None,
                'locationName': 'Alajärvi',
                'region': 'other',
            },
        ]

        shuffle(data)  # Make sure the order of records does not matter
        returned_to_karelia = check_if_person_returned_karelia_in_between_wars(data)
        assert returned_to_karelia is True

        data = [
            {
                'movedIn': 38,
                'movedOut': None,
                'locationName': 'Impilahti',
                'region': 'karelia',
            },
            {
                'movedIn': 39,
                'movedOut': None,
                'locationName': 'Viinijärvi',
                'region': 'other',
            },
            {
                'movedIn': 40,
                'movedOut': 41,
                'locationName': 'Riistavesi',
                'region': 'other',
            },
            {
                'movedIn': 44,
                'movedOut': None,
                'locationName': 'Alajärvi',
                'region': 'other',
            },
        ]

        returned_to_karelia = check_if_person_returned_karelia_in_between_wars(data)
        assert returned_to_karelia is False

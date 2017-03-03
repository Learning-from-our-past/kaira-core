import pytest
from books.karelians.tests.extraction.locations.mock_person_data import LOCATION_TEXTS, EXPECTED_RESULTS, LOCATION_HEURISTICS
from books.karelians.extraction.extractors.karelianlocations import KarelianLocationsExtractor
from books.karelians.extraction.extractors.finnishlocations import FinnishLocationsExtractor
from books.karelians.tests.utils.MockErrorLogger import MockExceptionLogger
from books.karelians.tests.utils.ValueUnWrapper import unwrap
from books.karelians.extraction.extractors.bnf_parsers.migration_parser import parse_locations


class TestMigrationParser:

    def assert_locations(self, got, expected):
        """
        Assert all locations and their migration years.
        :param got:
        :param expected:
        :return:
        """
        assert len(got) == len(expected)

        for record_pair in zip(got, expected):
            assert record_pair[0]['place'] == record_pair[1]['place']

            if 'municipality' in record_pair[0]:
                assert record_pair[0]['municipality'] == record_pair[1]['municipality']
            else:
                assert ('municipality' in record_pair[0]) is ('municipality' in record_pair[1])

            if 'year_information' in record_pair[0]:
                for year_info in zip(record_pair[0]['year_information'], record_pair[1]['year_information']):
                    if 'moved_out' in year_info[0]:
                        assert year_info[0]['moved_out'] == year_info[1]['moved_out']
                    else:
                        assert ('moved_out' in year_info[0]) is ('moved_out' in year_info[1])

                    if 'moved_in' in year_info[0]:
                        assert year_info[0]['moved_in'] == year_info[1]['moved_in']
                    else:

                        assert ('moved_in' in year_info[0]) is ('moved_in' in year_info[1])
            else:
                assert ('year_information' in record_pair[0]) is ('year_information' in record_pair[1])

    def should_parse_locations_with_varying_amount_of_year_data(self):
        s1 = ("Laasola -39. 42—44", [{'place': 'Laasola', 'year_information': [{'moved_out': '39'}, {'moved_in': '42', 'moved_out': '44'}]}])
        s2 = ("Laasola -39. 42—", [{'place': 'Laasola', 'year_information': [{'moved_out': '39'}, {'moved_in': '42'}]}])
        s3 = ("Laasola -39. —44", [{'place': 'Laasola', 'year_information': [{'moved_out': '39'}, {'moved_out': '44'}]}])
        s4 = ("Laasola.", [{'place': 'Laasola'}])
        s5 = ("Laasola -39.", [{'place': 'Laasola', 'year_information': [{'moved_out': '39'}]}])
        s6 = ("Laasola 29-39. 42—44", [{'place': 'Laasola', 'year_information': [{'moved_in': '29', 'moved_out': '39'}, {'moved_in': '42', 'moved_out': '44'}]}])

        self.assert_locations(parse_locations(s1[0]), s1[1])
        self.assert_locations(parse_locations(s2[0]), s2[1])
        self.assert_locations(parse_locations(s3[0]), s3[1])
        self.assert_locations(parse_locations(s4[0]), s4[1])
        self.assert_locations(parse_locations(s5[0]), s5[1])
        self.assert_locations(parse_locations(s6[0]), s6[1])

    def should_parse_multiple_locations_correctly(self):
        s1 = "Viipurin mlk. -27, Pohjois-Karjala 31—32, Viipuri 32—. "
        results = parse_locations(s1)

        expected = [{'place': 'Viipurin mlk', 'year_information': [{'moved_out': '27'}]},
            {'place': 'Pohjois-Karjala', 'year_information': [{'moved_in': '31', 'moved_out': '32'}]},
            {'place': 'Viipuri', 'year_information': [{'moved_in': '32'}]}
        ]

        self.assert_locations(results, expected)


class TestFinnishLocationExtraction:

    @pytest.yield_fixture(autouse=True)
    def exception_logger(self):
        return MockExceptionLogger()

    @pytest.yield_fixture(autouse=True)
    def finnish_extractor(self, exception_logger):
        return FinnishLocationsExtractor(None, exception_logger, None)

    def should_extract_locations(self, finnish_extractor):
        results = unwrap(finnish_extractor.extract(LOCATION_TEXTS[0]))['otherLocations']

        assert len(results) == 4

        assert results[0] == EXPECTED_RESULTS[0]['finnish_locations'][0]
        assert results[1] == EXPECTED_RESULTS[0]['finnish_locations'][1]
        assert results[2] == EXPECTED_RESULTS[0]['finnish_locations'][2]
        assert results[3] == EXPECTED_RESULTS[0]['finnish_locations'][3]

    def should_return_empty_if_no_finnish_locations_listed(self, finnish_extractor):
        results = unwrap(finnish_extractor.extract(''))['otherLocations']
        assert len(results) == 0

    def should_leave_out_too_long_place_names(self, finnish_extractor):
        results = unwrap(finnish_extractor.extract(LOCATION_HEURISTICS['long_place_name']['text']))['otherLocations']

        assert len(results) == 4
        assert results == LOCATION_HEURISTICS['long_place_name']['expected']

    def should_leave_out_too_short_place_names(self, finnish_extractor):
        results = unwrap(finnish_extractor.extract(LOCATION_HEURISTICS['short_place_name']['text']))['otherLocations']

        assert len(results) == 4
        assert results == LOCATION_HEURISTICS['short_place_name']['expected']

    def should_extract_short_place_names_if_they_are_in_white_list(self, finnish_extractor):
        results = unwrap(finnish_extractor.extract(LOCATION_HEURISTICS['short_white_listed_name']['text']))['otherLocations']

        assert len(results) == 5
        assert results[4]['locationName'] == 'Utö'

    def should_use_alias_for_short_place_name_if_one_is_available(self, finnish_extractor):
        results = unwrap(finnish_extractor.extract(LOCATION_HEURISTICS['short_white_listed_alias_name']['text']))[
            'otherLocations']

        assert len(results) == 5
        assert results[4]['locationName'] == 'Ii'


class TestKarelianLocationExtraction:

    @pytest.yield_fixture(autouse=True)
    def exception_logger(self):
        return MockExceptionLogger()

    @pytest.yield_fixture(autouse=True)
    def karelian_extractor(self, exception_logger):
        return KarelianLocationsExtractor(None, exception_logger, None)

    def should_extract_locations_with_village_names(self, karelian_extractor):
        results = unwrap(karelian_extractor.extract(LOCATION_TEXTS[0]))['karelianLocations']

        assert len(results) == 2

        assert results[0]['locationName'] == 'Kuolemajärvi'
        assert results[0]['region'] == 'karelia'
        assert results[0]['coordinates']['longitude'] == '28.98863'
        assert results[0]['coordinates']['latitude'] == '60.33621'
        assert results[0]['movedIn'] == ''
        assert results[0]['movedOut'] == '39'

        assert results[0]['village']['locationName'] == 'Laasola'
        assert results[0]['village']['coordinates']['latitude'] == '60.38876'
        assert results[0]['village']['coordinates']['longitude'] == '28.93825'

        assert results[1]['locationName'] == 'Kuolemajärvi'
        assert results[1]['region'] == 'karelia'
        assert results[1]['coordinates']['latitude'] == '60.33621'
        assert results[1]['coordinates']['longitude'] == '28.98863'

        assert results[0]['village']['locationName'] == 'Laasola'
        assert results[0]['village']['coordinates']['latitude'] == '60.38876'
        assert results[0]['village']['coordinates']['longitude'] == '28.93825'

        assert results[1]['movedIn'] == '42'
        assert results[1]['movedOut'] == '44'


    def should_extract_locations_with_missing_village_names(self, karelian_extractor):
        results = unwrap(karelian_extractor.extract(LOCATION_TEXTS[2]))['karelianLocations']

        assert len(results) == 3

        assert results[0]['locationName'] == 'Viipurinmlk'
        assert results[0]['region'] == 'karelia'
        assert results[0]['coordinates']['longitude'] == ''
        assert results[0]['coordinates']['latitude'] == ''
        assert results[0]['movedIn'] == ''
        assert results[0]['movedOut'] == '27'

        assert results[0]['village']['locationName'] == None
        assert results[0]['village']['coordinates']['latitude'] == ''
        assert results[0]['village']['coordinates']['longitude'] == ''

        assert results[1]['locationName'] == 'Pohjois-Karjala'
        assert results[1]['region'] == 'karelia'
        assert results[1]['coordinates']['longitude'] == ''
        assert results[1]['coordinates']['latitude'] == ''
        assert results[1]['movedIn'] == '31'
        assert results[1]['movedOut'] == '32'

        assert results[1]['village']['locationName'] == None
        assert results[1]['village']['coordinates']['latitude'] == ''
        assert results[1]['village']['coordinates']['longitude'] == ''

        assert results[2]['locationName'] == 'Viipuri'
        assert results[2]['region'] == 'karelia'
        assert results[2]['coordinates']['longitude'] == '28.73333'
        assert results[2]['coordinates']['latitude'] == '60.7'
        assert results[2]['movedIn'] == '32'
        assert results[2]['movedOut'] == ''

        assert results[2]['village']['locationName'] == None
        assert results[2]['village']['coordinates']['latitude'] == ''
        assert results[2]['village']['coordinates']['longitude'] == ''

    def should_return_empty_if_no_karelian_locations_listed(self, karelian_extractor):
        results = unwrap(karelian_extractor.extract(''))['karelianLocations']
        assert len(results) == 0
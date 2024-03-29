import re
import pytest
from extractors.common.extraction_keys import KEYS
from extractors.bookseries.karelians.extractors.bnf_parsers.migration_parser import (
    parse_locations,
)
from extractors.bookseries.karelians.extractors.migration_route_extractors import (
    FinnishLocationsExtractor,
    KarelianLocationsExtractor,
)
from extractors.bookseries.karelians.extractors.tests.migrations.mock_person_data import (
    LOCATION_TEXTS,
    EXPECTED_RESULTS,
    LOCATION_HEURISTICS,
    LOCATION_TEXTS_WITH_ROUVA_WORD,
    LOCATION_TEXTS_WITH_INCORRECT_REGION,
)
from core.utils.geo.dbhandler import Place, Location


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
                assert ('municipality' in record_pair[0]) is (
                    'municipality' in record_pair[1]
                )

            if 'year_information' in record_pair[0]:
                for year_info in zip(
                    record_pair[0]['year_information'],
                    record_pair[1]['year_information'],
                ):
                    if 'moved_out' in year_info[0]:
                        assert year_info[0]['moved_out'] == year_info[1]['moved_out']
                    else:
                        assert ('moved_out' in year_info[0]) is (
                            'moved_out' in year_info[1]
                        )

                    if 'moved_in' in year_info[0]:
                        assert year_info[0]['moved_in'] == year_info[1]['moved_in']
                    else:

                        assert ('moved_in' in year_info[0]) is (
                            'moved_in' in year_info[1]
                        )
            else:
                assert ('year_information' in record_pair[0]) is (
                    'year_information' in record_pair[1]
                )

    def should_parse_locations_with_varying_amount_of_year_data(self):
        s1 = (
            'Laasola -39. 42—44',
            [
                {
                    'place': 'Laasola',
                    'year_information': [
                        {'moved_out': '39'},
                        {'moved_in': '42', 'moved_out': '44'},
                    ],
                }
            ],
        )
        s2 = (
            'Laasola -39. 42—',
            [
                {
                    'place': 'Laasola',
                    'year_information': [{'moved_out': '39'}, {'moved_in': '42'}],
                }
            ],
        )
        s3 = (
            'Laasola -39. —44',
            [
                {
                    'place': 'Laasola',
                    'year_information': [{'moved_out': '39'}, {'moved_out': '44'}],
                }
            ],
        )
        s4 = ('Laasola.', [{'place': 'Laasola'}])
        s5 = (
            'Laasola -39.',
            [{'place': 'Laasola', 'year_information': [{'moved_out': '39'}]}],
        )
        s6 = (
            'Laasola 29-39. 42—44',
            [
                {
                    'place': 'Laasola',
                    'year_information': [
                        {'moved_in': '29', 'moved_out': '39'},
                        {'moved_in': '42', 'moved_out': '44'},
                    ],
                }
            ],
        )

        self.assert_locations(parse_locations(s1[0]), s1[1])
        self.assert_locations(parse_locations(s2[0]), s2[1])
        self.assert_locations(parse_locations(s3[0]), s3[1])
        self.assert_locations(parse_locations(s4[0]), s4[1])
        self.assert_locations(parse_locations(s5[0]), s5[1])
        self.assert_locations(parse_locations(s6[0]), s6[1])

    def should_parse_multiple_locations_correctly(self):
        s1 = 'Viipurin mlk. -27, Pohjois-Karjala 31—32, Viipuri 32—. '
        results = parse_locations(s1)

        expected = [
            {'place': 'Viipurin mlk', 'year_information': [{'moved_out': '27'}]},
            {
                'place': 'Pohjois-Karjala',
                'year_information': [{'moved_in': '31', 'moved_out': '32'}],
            },
            {'place': 'Viipuri', 'year_information': [{'moved_in': '32'}]},
        ]

        self.assert_locations(results, expected)


class TestFinnishLocationExtraction:
    @pytest.fixture(autouse=True)
    def finnish_extractor(self, th):
        return th.setup_extractor(FinnishLocationsExtractor(None, None))

    def should_extract_locations(self, finnish_extractor, th):
        results, metadata = finnish_extractor.extract(
            {'text': LOCATION_TEXTS[0]}, {}, {}
        )
        locations = results['finnishLocations'][KEYS['otherlocations']]
        th.omit_property(locations, 'coordinates')
        assert len(locations) == 4

        assert locations[0] == EXPECTED_RESULTS[0]['finnish_locations'][0]
        assert locations[1] == EXPECTED_RESULTS[0]['finnish_locations'][1]
        assert locations[2] == EXPECTED_RESULTS[0]['finnish_locations'][2]
        assert locations[3] == EXPECTED_RESULTS[0]['finnish_locations'][3]

    def should_return_empty_if_no_finnish_locations_listed(self, finnish_extractor):
        results, metadata = finnish_extractor.extract({'text': ''}, {}, {})
        locations = results['finnishLocations'][KEYS['otherlocations']]
        assert len(locations) == 0

    def should_leave_out_too_long_place_names(self, finnish_extractor, th):
        results, metadata = finnish_extractor.extract(
            {'text': LOCATION_HEURISTICS['long_place_name']['text']}, {}, {}
        )
        locations = results['finnishLocations'][KEYS['otherlocations']]

        th.omit_property(locations, 'coordinates')
        assert len(locations) == 4
        assert locations == LOCATION_HEURISTICS['long_place_name']['expected']

    def should_leave_out_too_short_place_names(self, finnish_extractor, th):
        results, metadata = finnish_extractor.extract(
            {'text': LOCATION_HEURISTICS['short_place_name']['text']}, {}, {}
        )
        locations = results['finnishLocations'][KEYS['otherlocations']]

        th.omit_property(locations, 'coordinates')
        assert len(locations) == 4
        assert locations == LOCATION_HEURISTICS['short_place_name']['expected']

    def should_extract_short_place_names_if_they_are_in_white_list(
        self, finnish_extractor
    ):
        results, metadata = finnish_extractor.extract(
            {'text': LOCATION_HEURISTICS['short_white_listed_name']['text']}, {}, {}
        )
        locations = results['finnishLocations'][KEYS['otherlocations']]

        assert len(locations) == 5
        assert locations[4]['locationName'] == 'Utö'

    def should_use_alias_for_short_place_name_if_one_is_available(
        self, finnish_extractor
    ):
        results, metadata = finnish_extractor.extract(
            {'text': LOCATION_HEURISTICS['short_white_listed_alias_name']['text']},
            {},
            {},
        )
        locations = results['finnishLocations'][KEYS['otherlocations']]

        assert len(locations) == 5
        assert locations[4]['locationName'] == 'Ii'

    def should_accept_any_name_if_mlk_pattern_in_the_end(self, finnish_extractor):
        results, metadata = finnish_extractor.extract(
            {'text': LOCATION_HEURISTICS['long_name_with_mlk']['text']}, {}, {}
        )
        locations = results['finnishLocations'][KEYS['otherlocations']]

        assert len(locations) == 5
        assert locations[4]['locationName'] == 'Kristiinankaupungin mlk'

    def should_remove_hyphens_from_beginning_of_the_place_name(self, finnish_extractor):
        results, metadata = finnish_extractor.extract(
            {'text': LOCATION_HEURISTICS['name_with_extra_hyphens']['text']}, {}, {}
        )
        locations = results['finnishLocations'][KEYS['otherlocations']]

        assert len(locations) == 5
        assert locations[3]['locationName'] == 'Ähtäri'  # Hyphen from beginning removed


class TestKarelianLocationExtraction:
    @pytest.fixture(autouse=True)
    def karelian_extractor(self, th):
        return th.setup_extractor(KarelianLocationsExtractor(None, None))

    def should_extract_locations_with_village_names(self, karelian_extractor):
        results, metadata = karelian_extractor.extract(
            {'text': LOCATION_TEXTS[0]}, {}, {}
        )
        locations = results['karelianLocations']['karelianLocations']

        assert len(locations) == 2

        assert locations[0]['locationName'] == 'Kuolemajärvi'
        assert locations[0]['region'] == 'karelia'
        assert locations[0]['movedIn'] is None
        assert locations[0]['movedOut'] == 39

        assert locations[0]['village']['locationName'] == 'Laasola'
        assert locations[0]['village']['coordinates']['latitude'] is None
        assert locations[0]['village']['coordinates']['longitude'] is None

        assert locations[1]['locationName'] == 'Kuolemajärvi'
        assert locations[1]['region'] == 'karelia'

        assert locations[0]['village']['locationName'] == 'Laasola'

        assert locations[1]['movedIn'] == 42
        assert locations[1]['movedOut'] == 44

    def should_extract_locations_with_missing_village_names(self, karelian_extractor):
        results, metadata = karelian_extractor.extract(
            {'text': LOCATION_TEXTS[2]}, {}, {}
        )
        locations = results['karelianLocations']['karelianLocations']

        assert len(locations) == 3

        assert locations[0]['locationName'] == 'Viipurin mlk'
        assert locations[0]['region'] == 'karelia'
        assert locations[0]['coordinates']['latitude'] == '60.7116853059'
        assert locations[0]['coordinates']['longitude'] == '28.7769366303'
        assert locations[0]['movedIn'] is None
        assert locations[0]['movedOut'] == 27

        assert locations[0]['village'] is None

        assert locations[1]['locationName'] == 'Pohjois Karjala'
        assert locations[1]['region'] == 'karelia'
        assert locations[1]['coordinates']['longitude'] is None
        assert locations[1]['coordinates']['latitude'] is None
        assert locations[1]['movedIn'] == 31
        assert locations[1]['movedOut'] == 32

        assert locations[1]['village'] is None

        assert locations[2]['locationName'] == 'Viipuri'
        assert locations[2]['region'] == 'karelia'
        assert locations[2]['movedIn'] == 32
        assert locations[2]['movedOut'] is None

        assert locations[2]['village'] is None

    def should_return_empty_if_no_karelian_locations_listed(self, karelian_extractor):
        results, metadata = karelian_extractor.extract({'text': ''}, {}, {})
        locations = results['karelianLocations']['karelianLocations']

        assert len(locations) == 0

    def should_leave_out_too_long_place_names(self, karelian_extractor):
        results, metadata = karelian_extractor.extract(
            {'text': LOCATION_HEURISTICS['long_place_name']['text']}, {}, {}
        )
        locations = results['karelianLocations']['karelianLocations']

        assert len(locations) == 1

    def should_leave_out_too_short_place_names(self, karelian_extractor):
        results, metadata = karelian_extractor.extract(
            {'text': LOCATION_HEURISTICS['short_place_name']['text']}, {}, {}
        )
        locations = results['karelianLocations']['karelianLocations']

        assert len(locations) == 1

    def should_extract_short_place_names_if_they_are_in_white_list(
        self, karelian_extractor
    ):
        results, metadata = karelian_extractor.extract(
            {'text': LOCATION_HEURISTICS['short_white_listed_name']['text']}, {}, {}
        )
        locations = results['karelianLocations']['karelianLocations']

        assert len(locations) == 1
        assert locations[0]['locationName'] == 'Eno'

    def should_use_alias_for_short_place_name_if_one_is_available(
        self, karelian_extractor
    ):
        results, metadata = karelian_extractor.extract(
            {'text': LOCATION_HEURISTICS['short_white_listed_alias_name']['text']},
            {},
            {},
        )
        locations = results['karelianLocations']['karelianLocations']

        assert len(locations) == 1
        assert locations[0]['locationName'] == 'Ii'

    def should_accept_any_name_if_mlk_pattern_in_the_end(self, karelian_extractor):
        results, metadata = karelian_extractor.extract(
            {'text': LOCATION_HEURISTICS['long_name_with_mlk']['text']}, {}, {}
        )
        locations = results['karelianLocations']['karelianLocations']

        assert len(locations) == 1
        assert locations[0]['locationName'] == 'Kristiinankaupungin mlk'

    def should_remove_hyphens_from_beginning_of_the_place_name(
        self, karelian_extractor
    ):
        results, metadata = karelian_extractor.extract(
            {'text': LOCATION_HEURISTICS['name_with_extra_hyphens']['text']}, {}, {}
        )
        locations = results['karelianLocations']['karelianLocations']

        assert len(locations) == 1
        assert (
            locations[0]['locationName'] == 'Viipuri'
        )  # Hyphen from beginning removed


class TestMigrationRouteExtractor:
    @pytest.fixture(autouse=True)
    def migration_pipeline(self, th):
        return th.build_pipeline_from_yaml(MIGRATION_CONFIG)

    def should_run_post_process_to_mark_if_person_returned_to_karelia(
        self, migration_pipeline, th
    ):
        text = re.sub(r'\s', r' ', LOCATION_TEXTS[0])

        results, metadata = migration_pipeline.process({'text': text})
        th.omit_property(results, 'coordinates')
        assert results['migrationHistory']['returnedToKarelia'] is True

    @pytest.mark.skip
    def should_extract_location_list_with_missing_years_properly(
        self, migration_pipeline, th
    ):
        # TODO: Here both karelian and finnish location extraction breaks weirdly. Only Ypäjä is recognized as finnish location and
        # others will be classified as karelian locations. Something strange is going on.
        text = re.sub(r'\s', r' ', LOCATION_TEXTS[5])

        results, metadata = migration_pipeline.extract({'text': text}, {}, {})
        th.omit_property(results, 'coordinates')

    def should_fix_helsinkis_region_from_karelia_to_other(self, migration_pipeline, th):
        text = re.sub(r'\s', r' ', LOCATION_TEXTS_WITH_INCORRECT_REGION[0]['text'])

        results, metadata = migration_pipeline.process({'text': text})
        th.omit_property(results, 'coordinates')
        result_locations = results['migrationHistory']['locations']

        assert len(result_locations) == len(
            LOCATION_TEXTS_WITH_INCORRECT_REGION[0]['expected']
        )
        assert result_locations == LOCATION_TEXTS_WITH_INCORRECT_REGION[0]['expected']

    def should_fix_kanneljärvi_region_from_other_to_karelia(
        self, migration_pipeline, th
    ):
        text = re.sub(r'\s', r' ', LOCATION_TEXTS_WITH_INCORRECT_REGION[1]['text'])

        results, metadata = migration_pipeline.process({'text': text})
        th.omit_property(results, 'coordinates')
        result_locations = results['migrationHistory']['locations']

        assert len(result_locations) == len(
            LOCATION_TEXTS_WITH_INCORRECT_REGION[1]['expected']
        )
        assert result_locations == LOCATION_TEXTS_WITH_INCORRECT_REGION[1]['expected']

    def should_fix_incorrectly_listed_region_to_correct_one_from_geo_db(
        self, migration_pipeline, th, test_geo_db
    ):
        # Set up a case where place Mordor is listed in text as place in Karelia while in reality its region should
        # be "other". Region is fixed by retrieving it from geo db along with coordinates
        with test_geo_db.bind_ctx((Place, Location)):
            other_location = Location.get(Location.region == 'other')
            mock_other_place = Place(name='Mordor', location=other_location.id)
            mock_other_place.save()

            karelian_location = Location.get(Location.region == 'karelia')
            mock_karelia_place = Place(name='Lothlorien', location=karelian_location.id)
            mock_karelia_place.save()

            text = re.sub(r'\s', r' ', LOCATION_TEXTS_WITH_INCORRECT_REGION[2]['text'])

            results, metadata = migration_pipeline.process({'text': text})
            th.omit_property(results, 'coordinates')
            result_locations = results['migrationHistory']['locations']

            assert len(result_locations) == len(
                LOCATION_TEXTS_WITH_INCORRECT_REGION[2]['expected']
            )
            assert (
                result_locations == LOCATION_TEXTS_WITH_INCORRECT_REGION[2]['expected']
            )

    def should_leave_region_as_is_if_it_is_not_found_from_db(
        self, migration_pipeline, th
    ):
        text = re.sub(r'\s', r' ', LOCATION_TEXTS_WITH_INCORRECT_REGION[2]['text'])

        results, metadata = migration_pipeline.process({'text': text})
        th.omit_property(results, 'coordinates')
        result_locations = results['migrationHistory']['locations']

        assert len(result_locations) == len(
            LOCATION_TEXTS_WITH_INCORRECT_REGION[2]['expected']
        )
        # Assign regions based on the list in book when db does not have any overriding info
        assert result_locations[0]['region'] == 'karelia'
        assert result_locations[1]['region'] == 'other'

    class TestExcludingIncorrectWords:
        def extract_and_assert(self, person_data, migration_pipeline, th):
            text = re.sub(r'\s', r' ', person_data['text'])
            results, metadata = migration_pipeline.process({'text': text})
            th.omit_property(results, 'coordinates')
            th.omit_property(results, 'village')
            result_locations = results['migrationHistory']['locations']

            assert len(result_locations) == len(person_data['expected'])
            assert result_locations == person_data['expected']

        def should_not_contain_incorrect_word_rouva_as_location(
            self, migration_pipeline, th
        ):
            # Regression test to remove word Rouva from results
            self.extract_and_assert(
                LOCATION_TEXTS_WITH_ROUVA_WORD[0], migration_pipeline, th
            )
            self.extract_and_assert(
                LOCATION_TEXTS_WITH_ROUVA_WORD[1], migration_pipeline, th
            )
            self.extract_and_assert(
                LOCATION_TEXTS_WITH_ROUVA_WORD[2], migration_pipeline, th
            )
            self.extract_and_assert(
                LOCATION_TEXTS_WITH_ROUVA_WORD[3], migration_pipeline, th
            )


MIGRATION_CONFIG = """
pipeline:
  - !Extractor {
      module: "extractors.bookseries.karelians.extractors.migration_route_extractors",
      class_name: "MigrationRouteExtractor",
      pipeline: [
        !Extractor {
            module: "extractors.bookseries.karelians.extractors.migration_route_extractors",
            class_name: "KarelianLocationsExtractor"
        },
        !Extractor {
            module: "extractors.bookseries.karelians.extractors.migration_route_extractors",
            class_name: "FinnishLocationsExtractor"
        }
      ]
    }
"""

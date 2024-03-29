import pytest
from extractors.bookseries.karelians.extractors.farm_area_extractor import (
    FarmAreaExtractor,
)


class TestFarmExtraction:
    @pytest.fixture(autouse=True)
    def farm_extractor(self, th):
        return th.build_pipeline_from_yaml(FARM_EXTRACTOR_CONFIG)

    def verify_flags(self, expected_flags_and_texts, flag, farm_extractor):
        for e in expected_flags_and_texts:
            results, metadata = farm_extractor.process({'text': e[0]})
            assert results['farmDetails'][flag] is e[1]

    def verify_farm_details_were_found(self, expected, farm_extractor):
        for e in expected:
            results, metadata = farm_extractor.process({'text': e[0]})
            assert (results['farmDetails'] is not None) is e[1]

    def should_mark_animal_husbandry_true_if_it_is_mentioned_in_text(
        self, farm_extractor
    ):
        self.verify_flags(
            [
                ('Maanviljelyksen ohella Testikkäät harjoittavat karjanhoitoa.', True),
                ('Maanviljelyksen ohella Testikkäät harjoittavat karjataloutta.', True),
                ('Testikkäiden tila on karjatalous.', True),
            ],
            'animalHusbandry',
            farm_extractor,
        )

    def should_return_none_if_no_farm_properties_were_found(self, farm_extractor):
        self.verify_farm_details_were_found(
            [
                ('Testikkäillä on traktori.', False),
                ('Emäntä Testikäs on käynyt karjatalouskoulun.', False),
                ('Isäntä Testikäs on karjanhoitaja.', False),
            ],
            farm_extractor,
        )

    def should_mark_dairy_farm_true_if_it_is_mentioned_in_text_in_relevant_meaning(
        self, farm_extractor
    ):
        self.verify_flags(
            [
                ('Maanviljelyksen ohella Testikkäillä on lypsykarjaa.', True),
                ('Maanviljelyksen ohella Testikkäillä on lypsy- ja lihakarjaa.', True),
                (
                    'Emäntä on voittanut lypsykilpailun. Karjanhoitoa harjoitetaan.',
                    False,
                ),
                (
                    'Tilalla on siirrytty lypsykarjasta teuraskarjaan. Karjanhoitoa harjoitetaan.',
                    False,
                ),
            ],
            'dairyFarm',
            farm_extractor,
        )

    def should_mark_farm_as_asutustila_if_it_is_mentioned_in_the_text(
        self, farm_extractor
    ):
        self.verify_flags(
            [
                ('Testikkäillä on asutustila, jonka he saivat valtiolta.', True),
                ('Testikkäiden tila on pika-asutustila.', True),
                ('Testikkäiden tila on pika asutustila.', True),
                ('Testikkäillä on maatila jolla harjoitetaan karjanhoitoa.', False),
                (
                    'Testikkäiden tila on pisaka-asutudgstila, jolla harjoitetaan karjanhoitoa.',
                    False,
                ),
            ],
            'asutustila',
            farm_extractor,
        )

    def should_mark_maanhankintalaki_if_it_is_mentioned_in_the_text(
        self, farm_extractor
    ):
        self.verify_flags(
            [
                ('Testikkäiden tila perustettiin maanhankintalain nojalla.', True),
                (
                    'Testikkäiden tila perustettiin maanhangintalain nojalla. He harjoittavat karjanhoitoa.',
                    True,
                ),
                ('Testikkäillä on maanhankintatila.', True),
                (
                    'Testikkäillä on hieno maatila jossa harjoitetaan karjanhoitoa.',
                    False,
                ),
                (
                    'Testikkäillä on maanhaankrintatila. He harjoittavat karjanhoitoa.',
                    False,
                ),
            ],
            'maanhankintalaki',
            farm_extractor,
        )

    def should_mark_farm_as_cold_farm_if_it_is_mentioned_in_the_text(
        self, farm_extractor
    ):
        self.verify_flags(
            [
                ('Testikkäillä on kylmätila, jonka he saivat valtiolta.', True),
                (
                    'Testikkäiden tila on kylmätilana saatu, jonka he myöhemmin raivasivat isommaksi.',
                    True,
                ),
                (
                    'Testikkäiden tila kymätila, ja he harjoittavat karjanhoitoa',
                    False,
                ),  # No support for typos
                ('Testikkäillä on maatila jolla harjoitetaan karjanhoitoa.', False),
            ],
            'coldFarm',
            farm_extractor,
        )

    def should_extract_farm_area(self, farm_extractor):
        results, metadata = farm_extractor.process(
            {
                'text': 'Anonyymit asuvat maatilallaan, jonka pinta-ala on 35.20 ha ja siitä on viljeltyä 3.37 ha.'
            }
        )
        assert results['farmDetails']['farmTotalArea'] == 35.2


class TestFarmAreaExtraction:
    @pytest.fixture(autouse=True)
    def farm_area_extractor(self, th):
        return th.setup_extractor(FarmAreaExtractor(None, None))

    class TestFarmAreaIsPattern:
        def should_extract_hectares_correctly_as_float(self, farm_area_extractor):
            results, metadata = farm_area_extractor.extract(
                {
                    'text': 'Anonyymit asuvat maatilallaan, jonka pinta-ala on 35.20 ha ja siitä on viljeltyä 3.37 ha.'
                },
                {},
                {},
            )
            assert results['farmTotalArea'] == 35.2

            results, metadata = farm_area_extractor.extract(
                {
                    'text': 'Nimettömät asuvat tilalla, jonka pinta-ala on 21,61 ha ja viljelyksiä on 7,79 ha.'
                },
                {},
                {},
            )
            assert results['farmTotalArea'] == 21.61

        def should_extract_hectares_correctly_as_float_if_hectare_unit_contains_typo(
            self, farm_area_extractor
        ):
            results, metadata = farm_area_extractor.extract(
                {
                    'text': 'Perhe asuu tilalla, jonka pinta-ala on 28,5 haja viljelyksiä on 15 ha Heidän poikansa Taavi hoitaa tilaa.'
                },
                {},
                {},
            )
            assert results['farmTotalArea'] == 28.5

        def should_extract_hectares_correctly_as_float_if_area_is_in_ares(
            self, farm_area_extractor
        ):
            results, metadata = farm_area_extractor.extract(
                {
                    'text': 'Pa-lonkylä 44- Satunnaisella ihmisellä on oma talo. jonka tontin pinta ala on 10 aaria.'
                },
                {},
                {},
            )
            assert results['farmTotalArea'] == 10 / 100

        def should_extract_none_if_contains_whitespace_in_number(
            self, farm_area_extractor
        ):
            results, metadata = farm_area_extractor.extract(
                {
                    'text': 'Meikäläisillä on asutustila, jonka pinta-ala on 1 9 ha ja siitä on viljeltyä 4 ha.'
                },
                {},
                {},
            )
            assert results['farmTotalArea'] is None

        def should_extract_none_if_data_does_not_contain_total_area(
            self, farm_area_extractor
        ):
            results, metadata = farm_area_extractor.extract(
                {
                    'text': 'Jonkun perhe asuu maatilallaan. Pinta-alasta on viljeltyä 2,7 ha ja metsää 0,3 ha.'
                },
                {},
                {},
            )
            assert results['farmTotalArea'] is None

        def should_extract_none_if_area_is_in_square_meters(self, farm_area_extractor):
            results, metadata = farm_area_extractor.extract(
                {
                    'text': 'Nyymeillä on myös Helsingissä Tikkurilassa kaksikerroksinen asuintalo, jonka pinta-ala on 270 m'
                },
                {},
                {},
            )
            assert results['farmTotalArea'] is None

            results, metadata = farm_area_extractor.extract(
                {
                    'text': 'Testiperheellä on kesäasunto Ristiinkäytävän järven rannalla. Tontin pinta-ala on n. 2300 m'
                },
                {},
                {},
            )
            assert results['farmTotalArea'] is None

    class TestFarmAreaHaPattern:
        def should_extract_hectares_correctly_as_float_if_dot_in_unit_of_area(
            self, farm_area_extractor
        ):
            results, metadata = farm_area_extractor.extract(
                {
                    'text': 'Satunnaiset asuvat 20 ha.n suuruisella tilallaan, josta on viljeltyä 12.75 ha.'
                },
                {},
                {},
            )
            assert results['farmTotalArea'] == 20

        def should_extract_hectares_correctly_as_float_if_colon_in_unit_of_area(
            self, farm_area_extractor
        ):
            results, metadata = farm_area_extractor.extract(
                {
                    'text': 'Jotkut asuvat 133 ha:n suuruisella maatilallaan, jossa on 7 ha viljeltyä.'
                },
                {},
                {},
            )
            assert results['farmTotalArea'] == 133

        def should_extract_hectares_correctly_as_float_if_comma_in_value_of_area(
            self, farm_area_extractor
        ):
            results, metadata = farm_area_extractor.extract(
                {
                    'text': 'Anonyymit asuvat 112,23 ha:n suuruisella maatilalla, jossa on 12 ha viljeltyä.'
                },
                {},
                {},
            )
            assert results['farmTotalArea'] == 112.23

        def should_extract_hectares_correctly_as_float_if_dot_in_value_of_area(
            self, farm_area_extractor
        ):
            results, metadata = farm_area_extractor.extract(
                {
                    'text': 'Testiset asuvat 7.3 ha.n suuruisella asutustilallaan, jossa on 5 ha viljeltyä.'
                },
                {},
                {},
            )
            assert results['farmTotalArea'] == 7.3

        def should_extract_hectares_correctly_as_none_if_whitespace_in_value_of_area(
            self, farm_area_extractor
        ):
            results, metadata = farm_area_extractor.extract(
                {
                    'text': 'Testiset asuvat1 7 ha.n suuruisella asutustilallaan, jossa on 5 ha viljeltyä.'
                },
                {},
                {},
            )
            assert results['farmTotalArea'] is None


FARM_EXTRACTOR_CONFIG = """
pipeline:
  - !Extractor {
      module: "extractors.bookseries.karelians.extractors.farm_extractor",
      class_name: "FarmDetailsExtractor",
      pipeline: [
        !Extractor {
            module: "extractors.common.extractors.bool_extractor",
            class_name: "BoolExtractor",
            options: {
              patterns: {
                animalHusbandry: 'karjataloutta|karjanhoitoa?\\b|karjatalous\\b',
                dairyFarm: 'lypsy-|lypsy\\b|lypsykarja(?!sta)',
                asutustila: '(?:asutustila){s<=1,i<=1}|(?:pika-asutustila){s<=1,i<=1}',
                maanhankintalaki: '(?:maanhankinta){s<=1,i<=1}',
                coldFarm: 'kylmät'
              }
            }
        },
        !Extractor {
          module: "extractors.bookseries.karelians.extractors.farm_area_extractor",
          class_name: "FarmAreaExtractor"
        }
      ]
    }
"""

import pytest
from core.pipeline_construction.yaml_parser import YamlParser


class TestSpouseExtraction:

    @pytest.fixture(autouse=True)
    def spouse_extractor(self, result_map):
        parser = YamlParser(result_map)
        return parser.build_pipeline_from_yaml_string(SPOUSE_CONFIG)

    def should_extract_spouse_details_correctly(self, spouse_extractor, th, result_map):
        spouse_text = 'Puol. Maija Nyymi o.s. Testaaja, emäntä, synt. 30. 6. -19 Testilässä. Avioit. -44. Poika: Joku Jälkeäinen -46 Nyymilä.'

        # Add mocked dependency result to the result map, so that when pipeline is ran,
        # the spouse's extractors will pick these results
        result_map.add_results('mockPrimaryPerson', {'name': {'gender': 'Male'}})

        result, metadata = spouse_extractor.process({'text': spouse_text})
        spouse_details = result['spouse']

        th.omit_property(spouse_details, 'kairaId')

        assert spouse_details == {
            'formerSurname': 'Testaaja',
            'firstNames': 'Maija Nyymi',
            'hasSpouse': True,
            'deathYear': None,
            'weddingYear': 1944,
            'birthData': {
                'birthDay': 30,
                'birthMonth': 6,
                'birthYear': 1919,
                'birthLocation': {
                    'locationName': 'Testilässä',
                    'region': None,
                    'latitude': None,
                    'longitude': None
                }
            },
            'profession': {
                'professionName': 'emäntä',
                'extraInfo': {
                    'SESgroup1989': 1,
                    'agricultureOrForestryRelated': True,
                    'education': True,
                    'englishName': 'Farm housewife',
                    'manualLabor': True,
                    'occupationCategory': 3,
                    'socialClassRank': 5
                }
            },
            'warData': {
                'injuredInWarFlag': None,
                'servedDuringWarFlag': None,
                'lottaActivityFlags': {'lotta': False,
                                       'foodLotta': False,
                                       'officeLotta': False,
                                       'nurseLotta': False,
                                       'antiairLotta': False,
                                       'pikkulotta': False,
                                       'organizationLotta': False}
            },
            'marttaActivityFlag': False
        }

        assert metadata == {
            'spouse': {
                'cursorLocation': 79,
                'errors': {}
            }
        }

    def should_return_none_if_spouse_not_available(self, spouse_extractor, result_map):
        spouse_text = 'om. Testi Testisen perikunta. Viljelijä Mies Testinen. Tila sijaitsee Antooran kylässä. Kokonaispinta-ala on 80,67 ha.'
        # Add mocked dependency result to the result map, so that when pipeline is ran,
        # the spouse's extractors will pick these results
        result_map.add_results('mockPrimaryPerson', {'name': {'gender': 'Male'}})

        result, metadata = spouse_extractor.process({'text': spouse_text})
        spouse_details = result['spouse']

        assert spouse_details is None


# NOTE: In tests replace dependencies which you want to mock with string instead of anchor and mock the results
# to the result map.
SPOUSE_CONFIG = """
pipeline:
  - !Extractor {
      module: "book_extractors.karelians.extractors.spouse_extractor",
      class_name: "SpouseExtractor",
      pipeline: [
        !Extractor &SpouseFormerSurname {
          module: "book_extractors.karelians.extractors.original_family_extractor",
          class_name: "FormerSurnameExtractor",
          options: {
            output_path: "spouse"
          }
        },
        !Extractor {
          module: "book_extractors.karelians.extractors.profession_extractor",
          class_name: "ProfessionExtractor",
          cursor_location_depend_on: *SpouseFormerSurname,
          options: {
            output_path: "spouse"
          }
        },
        !Extractor &SpouseBirthday {
          module: "book_extractors.karelians.extractors.birthday_extractor",
          class_name: "BirthdayExtractor",
          cursor_location_depend_on: *SpouseFormerSurname,
          options: {
            output_path: "spouse"
          }
        },
        !Extractor &SpouseBirthLocation {
          module: "book_extractors.karelians.extractors.location_extractor",
          class_name: "BirthdayLocationExtractor",
          cursor_location_depend_on: *SpouseBirthday,
          options: {
            output_path: "spouse"
          }
        },
        !Extractor {
          module: "book_extractors.karelians.extractors.death_extractor",
          class_name: "DeathExtractor",
          cursor_location_depend_on: *SpouseBirthLocation,
          options: {
            output_path: "spouse"
          }
        },
        !Extractor {
          module: "book_extractors.karelians.extractors.wedding_extractor",
          class_name: "WeddingExtractor",
          cursor_location_depend_on: *SpouseBirthLocation,
          options: {
            output_path: "spouse"
          }
        },
        !Extractor {
          module: "book_extractors.karelians.extractors.martta_activity_flag_extractor",
          class_name: "MarttaActivityFlagExtractor",
          depends_on: [ "mockPrimaryPerson" ],
          options: {
            in_spouse_extractor: true,
            output_path: "spouse"
          }
        },
        !Extractor {
          module: "book_extractors.karelians.extractors.war_data_extractor",
          class_name: "WarDataExtractor",
          options: {
            output_path: "spouse"
          },
          pipeline: [
            !Extractor {
              module: "book_extractors.karelians.extractors.injured_in_war_flag_extractor",
              class_name: "InjuredInWarFlagExtractor",
              depends_on: [ "mockPrimaryPerson" ],
              options: {
                in_spouse_extractor: true
              }
            },
            !Extractor {
              module: "book_extractors.karelians.extractors.served_during_war_flag_extractor",
              class_name: "ServedDuringWarFlagExtractor",
              depends_on: [ "mockPrimaryPerson" ],
              options: {
                in_spouse_extractor: true
              }
            },
            !Extractor {
              module: "book_extractors.karelians.extractors.lotta_activity_flag_extractor",
              class_name: "LottaActivityFlagExtractor",
              depends_on: [ "mockPrimaryPerson" ],
              options: {
                in_spouse_extractor: true
              }
            }
          ]
        }
      ]
    }
"""

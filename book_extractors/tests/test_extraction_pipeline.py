import pytest
from book_extractors.common.extractors.base_extractor import BaseExtractor
from book_extractors.extraction_pipeline import ExtractionPipeline, configure_extractor


class TestExtractionPipeline:
    class TestDependencySystemOverallFunction:
        def should_successfully_resolve_deps_with_multiple_parent_pipeline_context_setting(self):
            parent_data = {
                'extraction_results': {},
                'parent_data': {
                    'parent_data': {
                        'extraction_results': {
                            'personState': 'awoooo'
                        }
                    }
                }
            }

            test_pipeline = ExtractionPipeline([
                configure_extractor(PreferredDrinkExtractor, dependencies_contexts=['parent.parent.parent'])
            ])

            results, metadata = test_pipeline.process({'text': 'awoo am a wolf'}, parent_pipeline_data=parent_data)
            assert results['preferredDrink'] == 'water'

        def should_successfully_resolve_deps_with_main_pipeline_context(self):
            parent_data = {
                'extraction_results': {},
                'parent_data': {
                    'parent_data': {
                        'parent_data': {
                            'extraction_results': {
                                'personState': 'awoooo'
                            },
                            'parent_data': None
                        }
                    }
                }
            }

            test_pipeline = ExtractionPipeline([
                configure_extractor(PreferredDrinkExtractor, dependencies_contexts=['main'])
            ])

            results, metadata = test_pipeline.process({'text': 'awoo am a wolf'}, parent_pipeline_data=parent_data)
            assert results['preferredDrink'] == 'water'

        def should_successfully_resolve_deps_with_current_pipeline_context(self):
            test_pipeline = ExtractionPipeline([
                configure_extractor(PersonStateExtractor),
                configure_extractor(PreferredDrinkExtractor, dependencies_contexts=['current'])
            ])

            results, metadata = test_pipeline.process({'text': 'awoo am a wolf'})
            assert results['preferredDrink'] == 'water'

        def should_set_dependencies_and_contexts_correctly_when_extractor_has_own_and_inherited_dependencies(self):
            # Own dep: HotDayFlagExtractor (from PreferredCoffeeDrinkExtractor)
            # Inherited dep: PersonState (from PreferredDrinkExtractor)
            parent_data = {'extraction_results': {'hotDay': True}}

            test_pipeline = ExtractionPipeline([
                configure_extractor(PersonStateExtractor),
                configure_extractor(PreferredCoffeeDrinkExtractor, dependencies_contexts=['parent', 'current'])
            ])

            results, metadata = test_pipeline.process({'text': 'wolfy'}, parent_pipeline_data=parent_data)
            assert results == {'preferredCoffeeDrink': 'ice coffee',
                               'personState': 'wolfy'}

        def should_set_dependencies_and_contexts_correctly_when_extractor_has_multiple_own_and_inherited_deps(self):
            # Own deps: PreferredCoffeeDrinkExtractor, PersonStateExtractor (from SubExtractorWithMultipleDeps)
            # Inherited deps: PreferredDrinkExtractor, HotDayFlagExtractor (from ExtractorWithMultipleDeps)
            parent_data = {
                'extraction_results': {'preferredDrink': 'coffee'},
                'parent_data': {
                    'extraction_results': {'personState': 'awoo'},
                    'parent_data': {
                        'extraction_results': {'preferredCoffeeDrink': 'ice coffee',
                                               'hotDay': True},
                        'parent_data': None
                    }
                }
            }

            test_pipeline = ExtractionPipeline([
                configure_extractor(SubExtractorWithMultipleDependencies,
                                    dependencies_contexts=['main', 'parent.parent', 'parent', 'parent.parent.parent'])
            ])

            results, metadata = test_pipeline.process({'text': 'awoo am a wolf'}, parent_pipeline_data=parent_data)
            assert results['subMultiDeps'] == 'TrueTrue'

        def should_correctly_set_everything_up_if_same_dep_is_present_multiple_times_on_different_pipelines(self):
            parent_data = {
                'extraction_results': {
                    'hotDay': False},
                'parent_data': {
                    'extraction_results': {'hotDay': True},
                    'parent_data': None
                }
            }

            test_pipeline = ExtractionPipeline([
                configure_extractor(ExtractorWithSameDepMultipleTimes, dependencies_contexts=['parent', 'main'])
            ])

            results, metadata = test_pipeline.process({'text': 'awoo am a wolf'}, parent_pipeline_data=parent_data)
            assert results['sameMultipleTimes'] == {'main.hotDay': True, 'parent.hotDay': False}

        def should_successfully_extract_expected_data_based_on_all_the_dependencies_and_their_contexts(self):
            parent_data = {
                'extraction_results': {
                    'result': 'test'
                },
                'metadata': {
                    'identity': 'i hate meta'
                },
                'parent_data': {
                    'extraction_results': {'hotDay': True},
                    'metadata': {'identity': 'who am i'},
                    'parent_data': None
                }
            }

            test_pipeline = ExtractionPipeline([
                configure_extractor(PersonStateExtractor),
                configure_extractor(PreferredDrinkExtractor, dependencies_contexts=['current']),
                configure_extractor(GroceryListExtractor)
            ])

            results, metadata = test_pipeline.process({'text': 'drowsy'}, parent_pipeline_data=parent_data)

            expected_results = {'groceryList': {'buyCoffee': True,
                                                'preferredCoffeeDrink': 'ice coffee'},
                                'personState': 'drowsy',
                                'preferredDrink': 'coffee'}

            assert results == expected_results

            parent_data['parent_data']['extraction_results']['hotDay'] = False
            results, metadata = test_pipeline.process({'text': 'happy'}, parent_pipeline_data=parent_data)

            expected_results = {'groceryList': {'buyCoffee': False,
                                                'preferredCoffeeDrink': 'hot coffee'},
                                'personState': 'happy',
                                'preferredDrink': 'water'}

            assert results == expected_results


class MockExtractor(BaseExtractor):
    extraction_key = 'mock'

    def __init__(self, key_of_cursor_location_dependent=None, options=None, dependencies_contexts=None):
        super(MockExtractor, self).__init__(key_of_cursor_location_dependent, options)

    def _extract(self, entry, extraction_results, extraction_metadata):
        return self._add_to_extraction_results('mock result', extraction_results, extraction_metadata)


class PersonStateExtractor(BaseExtractor):
    extraction_key = 'personState'

    def __init__(self, key_of_cursor_location_dependent=None, options=None, dependencies_contexts=None):
        super(PersonStateExtractor, self).__init__()

    def _extract(self, entry, extraction_results, extraction_metadata):
        return self._add_to_extraction_results(entry['text'], extraction_results, extraction_metadata)


class PreferredDrinkExtractor(BaseExtractor):
    extraction_key = 'preferredDrink'

    def __init__(self, key_of_cursor_location_dependent=None, options=None, dependencies_contexts=None):
        super(PreferredDrinkExtractor, self).__init__()

        self._set_dependencies([PersonStateExtractor], dependencies_contexts)

    def _extract(self, entry, extraction_results, extraction_metadata):
        result = 'water'

        if self._deps[PersonStateExtractor.extraction_key] == 'drowsy':
            result = 'coffee'

        return self._add_to_extraction_results(result, extraction_results, extraction_metadata)


class GroceryListExtractor(BaseExtractor):
    extraction_key = 'groceryList'

    def __init__(self, key_of_cursor_location_dependent=None, options=None, dependencies_contexts=None):
        super(GroceryListExtractor, self).__init__()

        self._test_sub_pipeline = ExtractionPipeline([
            configure_extractor(BuyCoffeeExtractor, dependencies_contexts=['parent']),
            configure_extractor(PreferredCoffeeDrinkExtractor, dependencies_contexts=['main', 'parent'])
        ])

    def _extract(self, entry, extraction_results, extraction_metadata):
        parent_data = {'extraction_results': extraction_results,
                       'metadata': extraction_metadata,
                       'parent_data': self._parent_pipeline_data}
        results, metadata = self._test_sub_pipeline.process({'text': 'drowsy'}, parent_pipeline_data=parent_data)

        return self._add_to_extraction_results(results, extraction_results, extraction_metadata)


class BuyCoffeeExtractor(BaseExtractor):
    extraction_key = 'buyCoffee'

    def __init__(self, key_of_cursor_location_dependent=None, options=None, dependencies_contexts=None):
        super(BuyCoffeeExtractor, self).__init__()

        self._set_dependencies([PreferredDrinkExtractor], dependencies_contexts)

    def _extract(self, entry, extraction_results, extraction_metadata):
        result = 'coffee' in self._deps[PreferredDrinkExtractor.extraction_key]
        return self._add_to_extraction_results(result, extraction_results, extraction_metadata)


class PreferredCoffeeDrinkExtractor(PreferredDrinkExtractor):
    extraction_key = 'preferredCoffeeDrink'

    def __init__(self, key_of_cursor_location_dependent=None, options=None, dependencies_contexts=None):
        super(PreferredCoffeeDrinkExtractor, self).__init__()
        self._set_dependencies([HotDayFlagExtractor], dependencies_contexts=dependencies_contexts)

    def _extract(self, entry, extraction_results, extraction_metadata):
        result = 'ice coffee' if self._deps[HotDayFlagExtractor.extraction_key] else 'hot coffee'
        return self._add_to_extraction_results(result, extraction_results, extraction_metadata)


class HotDayFlagExtractor:
    extraction_key = 'hotDay'


class ExtractorWithMultipleDependencies(BaseExtractor):
    extraction_key = 'superMultiDeps'

    def __init__(self, key_of_cursor_location_dependent=None, options=None, dependencies_contexts=None):
        super(ExtractorWithMultipleDependencies, self).__init__()

        self._set_dependencies([PreferredDrinkExtractor, HotDayFlagExtractor], dependencies_contexts)

    def _extract(self, entry, extraction_results, extraction_metadata):
        result = ('coffee' in self._deps[PreferredDrinkExtractor.extraction_key]).__str__()
        result += self._deps[HotDayFlagExtractor.extraction_key].__str__()
        return self._add_to_extraction_results(result, extraction_results, extraction_metadata)


class SubExtractorWithMultipleDependencies(ExtractorWithMultipleDependencies):
    extraction_key = 'subMultiDeps'

    def __init__(self, key_of_cursor_location_dependent=None, options=None, dependencies_contexts=None):
        super(SubExtractorWithMultipleDependencies, self).__init__()

        self._set_dependencies([PreferredCoffeeDrinkExtractor, PersonStateExtractor], dependencies_contexts)

    def _extract(self, entry, extraction_results, extraction_metadata):
        result = ('ice coffee' in self._deps[PreferredCoffeeDrinkExtractor.extraction_key]).__str__()
        result += ('awoo' in self._deps[PersonStateExtractor.extraction_key]).__str__()
        return self._add_to_extraction_results(result, extraction_results, extraction_metadata)


class ExtractorWithSameDepMultipleTimes(BaseExtractor):
    extraction_key = 'sameMultipleTimes'

    def __init__(self, key_of_cursor_location_dependent=None, options=None, dependencies_contexts=None):
        super(ExtractorWithSameDepMultipleTimes, self).__init__()

        self._set_dependencies([HotDayFlagExtractor, HotDayFlagExtractor], dependencies_contexts)

    def _extract(self, entry, extraction_results, extraction_metadata):
        return self._add_to_extraction_results(self._deps, extraction_results, extraction_metadata)
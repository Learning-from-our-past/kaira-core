import pytest


def pytest_collection_modifyitems(session, config, items):
    """
    Called after collection has been performed, may filter or re-order
    the items in-place. Use with decorator:
    @pytest.mark.only
    """
    found_only_marker = False
    for item in items.copy():
        if item.get_marker('only'):
            if not found_only_marker:
                items.clear()
                found_only_marker = True
            items.append(item)


class Th:
    """
    Test helper class which is importable as fixture to all tests.
    """
    @staticmethod
    def omit_property(target, property_name):
        if type(target) is list:
            for item in target:
                Th.omit_property(item, property_name)
        elif type(target) is dict and property_name in target:
            del target[property_name]

        if type(target) is dict:
            for key, item in target.items():
                Th.omit_property(item, property_name)

@pytest.fixture
def th():
    return Th

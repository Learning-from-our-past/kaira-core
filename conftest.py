import pytest
from peewee import *
import shutil
import os

from core import extraction_constants
from extractors.common.extractors.kaira_id_extractor import KairaIdProvider
from core.pipeline_construction.dependency_resolver import ExtractorResultsMap
from core.pipeline_construction.yaml_parser import YamlParser


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

    @staticmethod
    def setup_extractor(extractor):
        extractor.set_extraction_results_map(ExtractorResultsMap())
        return extractor

    @staticmethod
    def build_pipeline_from_yaml(config):
        parser = YamlParser(ExtractorResultsMap())
        return parser.build_pipeline_from_yaml_string(config)


@pytest.fixture
def th():
    return Th


@pytest.fixture()
def result_map():
    return ExtractorResultsMap()


@pytest.fixture(scope='session', autouse=True)
def constants():
    extraction_constants.BOOK_NUMBER = '1'
    extraction_constants.BOOK_SERIES = 'testbook'


@pytest.fixture(scope='function', autouse=True)
def reset_kaira_id():
    p = KairaIdProvider()
    p.reset()


@pytest.fixture(scope='session', autouse=True)
def test_geo_db():
    """
    Creates a test database which is copy of the normal geo database. Should be used with Peewee's test_database
    functionality: http://docs.peewee-orm.com/en/latest/peewee/playhouse.html#test-utils

    Example:
     with test_database(test_geo_db, (Place, Location), create_tables=False):
        # tests here...

    Note that this database is created once per session, so changes to it will be in effect in other tests which
    use the test db. If you need a clean test db, improve this fixture but take care to make it efficient by only restoring
    the db on tests that need it (set autouse=False) or modifying this to use in-memory db.
    """
    path = './temp'
    if not os.path.exists(path):
        os.makedirs(path)

    # Copy the db to temp location in favor of using in-memory copy. While in-memory would be likely faster,
    # the copying process seems slightly more complex and perhaps prone to errors. Look this SO-post and comments to
    # solution for possible complications:
    # https://stackoverflow.com/questions/4019081/how-to-copy-a-sqlite-table-from-a-disk-database-to-a-memory-database-in-python
    shutil.copyfile('support_datasheets/location.db', 'temp/location.db')
    test_db = SqliteDatabase('temp/location.db')

    yield test_db

    shutil.rmtree(path)

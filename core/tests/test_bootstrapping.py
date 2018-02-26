import pytest
import core.bootstrap as bootstrapper


def should_find_available_manifest_files_from_directory():
    available_bookseries = bootstrapper.find_available_bookseries_from_directory('core/tests/mock_data/manifest_mock_directories')
    assert len(available_bookseries) == 2


class TestBookseriesSetup:

    def should_raise_error_if_given_book_series_is_not_supported(self):
        with pytest.raises(bootstrapper.BookSeriesNotSupportedException):
            bootstrapper.setup_extraction_framework_for_bookseries('suomen-cs-pelaajat',
                                                                   'core/tests/mock_data/manifest_mock_directories')

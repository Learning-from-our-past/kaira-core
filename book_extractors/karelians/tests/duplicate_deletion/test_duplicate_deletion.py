import pytest
from lxml import etree
from book_extractors.karelians.duplicate_deleter import DuplicateDeleter
from book_extractors.karelians.tests.duplicate_deletion import mock_xml_data


class TestDuplicateDeletion:
    @pytest.fixture(autouse=True)
    def duplicate_deleter(self):
        return DuplicateDeleter()

    def should_correctly_delete_exact_duplicate_and_only_return_one_entry(self, duplicate_deleter):
        book = [etree.fromstring(mock_xml_data.DUPLICATED_PERSON)]
        dupes_deleted = duplicate_deleter.delete_duplicate_persons(book)
        assert len(dupes_deleted[0]) == 1

    def should_correctly_delete_nearly_exact_duplicate_when_birthdate_is_missing(self, duplicate_deleter):
        book = [etree.fromstring(mock_xml_data.DUPLICATED_PERSON_BAD_DOB)]
        dupes_deleted = duplicate_deleter.delete_duplicate_persons(book)
        assert len(dupes_deleted[0]) == 1

    def should_correctly_delete_very_similar_duplicate_when_name_and_birthdate_fail_to_match_identify_duplicate(self, duplicate_deleter):
        book = [etree.fromstring(mock_xml_data.DUPLICATED_PERSON_BAD_DOB_AND_NAME)]
        dupes_deleted = duplicate_deleter.delete_duplicate_persons(book)
        assert len(dupes_deleted[0]) == 1

    def should_correctly_delete_duplicate_but_keep_longer_text_from_duplicate_entry(self, duplicate_deleter):
        book = [etree.fromstring(mock_xml_data.DUPLICATED_PERSON_BAD_DOB_AND_NAME)]
        dupes_deleted = duplicate_deleter.delete_duplicate_persons(book)
        assert len(dupes_deleted[0][0].text) == 433

    def should_correctly_delete_duplicate_with_bad_birthdate_but_very_similar_name(self, duplicate_deleter):
        book = [etree.fromstring(mock_xml_data.DUPLICATED_PERSON_NO_DOB_SIMILAR_NAME)]
        dupes_deleted = duplicate_deleter.delete_duplicate_persons(book)
        assert len(dupes_deleted[0]) == 1

    def should_correctly_delete_duplicates_across_multiple_books_and_not_touch_nonduplicates(self, duplicate_deleter):
        books = [
            etree.fromstring(mock_xml_data.NO_DUPLICATES),
            etree.fromstring(mock_xml_data.NO_DUPLICATES_TWO),
            etree.fromstring(mock_xml_data.SHARES_ONE_ENTRY_WITH_EACH_NO_DUPLICATES)
        ]

        dupes_deleted = duplicate_deleter.delete_duplicate_persons(books)
        entries = {}
        for book in dupes_deleted:
            for entry in book:
                entries[entry.attrib['name']] = entry.text

        assert len(entries) == 4
        assert ('JOKUMIES, HERRA' in entries and 'VELHO, NOITA' in entries) is True

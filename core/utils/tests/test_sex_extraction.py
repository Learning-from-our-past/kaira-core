import pytest
from core.utils.sex_extract import Sex
from core.utils.sex_extract import SexException


class TestSexExtraction:
    @pytest.fixture(autouse=True, scope='class')
    def sex(self):
        return Sex()

    def should_extract_male_from_multiple_male_names(self, sex):
        name_string = 'Tuomas Juuso Joonas'
        assert sex.find_sex(name_string) == 'Male'

    def should_extract_female_from_multiple_female_names(self, sex):
        name_string = 'Virpi Maria Johanna'
        assert sex.find_sex(name_string) == 'Female'

    def should_extract_male_when_most_names_are_male_names_but_there_is_a_female_name(
        self, sex
    ):
        name_string = 'Tuomas Juuso Maria'
        assert sex.find_sex(name_string) == 'Male'

    def should_extract_female_when_most_names_are_female_names_but_there_is_a_male_name(
        self, sex
    ):
        name_string = 'Joonas Virpi Maria'
        assert sex.find_sex(name_string) == 'Female'

    def should_extract_none_when_there_are_equal_numbers_of_male_and_female_names(
        self, sex
    ):
        name_string = 'Maria Tuomas'
        assert sex.find_sex(name_string) is None

    def should_raise_exception_when_person_has_name_but_no_female_or_male_names_can_be_determined(
        self, sex
    ):
        name_string = 'Sherlock'
        with pytest.raises(SexException):
            sex.find_sex(name_string)

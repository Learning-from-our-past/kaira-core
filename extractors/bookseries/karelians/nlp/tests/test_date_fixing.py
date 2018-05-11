from extractors.bookseries.karelians.nlp.date_fixer import fix_dates


class TestDateFixer:
    def _verify_date(self, date, expected_date):
        assert fix_dates(date).strip() == expected_date

    def should_fix_common_incorrectly_formatted_siirtokarjalaisten_tie_dates(self):
        self._verify_date(' 12. 7. -14 ', '12.7.1914')
        self._verify_date(' 22. 2.-14 ', '22.2.1914')
        self._verify_date(' 13. 3.   16 ', '13.3.1916')
        self._verify_date(' 14. 11    35 ', '14.11.1935')
        self._verify_date(' 13. 5 -28 ', '13.5.1928')
        self._verify_date(' 20. 1 1. 39 ', '20.11.1939')
        self._verify_date(' 24. 5 04 ', '24.5.1904')
        self._verify_date(' 25, 9 -71 ', '25.9.1871')
        self._verify_date(' 12.   3,  1901 ', '12.3.1901')
        self._verify_date(' 15,  1,  1889', '15.1.1889')

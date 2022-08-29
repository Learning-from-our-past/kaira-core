from extractors.bookseries.karelians.nlp.clean_up_replacer import (
    get_siirtokarjalaisten_tie_cleaner,
)
from extractors.bookseries.karelians.nlp.date_fixer import fix_dates

replacer = get_siirtokarjalaisten_tie_cleaner()


def clean_up_entry(entry):
    """
    Runs all the preprocessing steps on a Siirtokarjalaisten tie person entry.

    While the quality of the Siirtokarjalaisten tie person entries is
    relatively good, some simple preprocessing can improve it
    considerably so it does not trip up the NLP parser.
    :param entry: A string entry from one of the Siirtokarjalaisten tie books
    :return String with clean-up procedures performed
    """
    preprocessed = replacer.run_replacements(entry.text)
    preprocessed = fix_dates(preprocessed)
    return preprocessed

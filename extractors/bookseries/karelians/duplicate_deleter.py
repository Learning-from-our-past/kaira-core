import datetime
import regex
from importlib import util as import_util
from jellyfish import levenshtein_distance as distance
if import_util.find_spec('ssdeep'):
    # This package is difficult to install on MacOS so to keep tests etc. from breaking, import it conditionally
    import ssdeep

"""
This file contains the code needed to filter duplicates out of the entries in
the 'Siirtokarjalaisten tie' books. The books contain duplicates, simply
because the authors of the books included the same person multiple times in
the books, sometimes with different texts. So there is also a need to decide
which text entry to keep - preferably there would be some way to objectively
evaluate which text entry is more information rich, but for now we simply take
the longer text entry and keep that. Some of the duplicates in the books are
also presumably as result of the same pages being carelessly scanned multiple
times.
"""


class DuplicateDeleter:
    def __init__(self, duplicate_match_threshold=80, potential_match_threshold=30,
                 minimum_str_length_for_potential_matches=400,
                 potential_bday_match_name_distance_threshold=4,
                 potential_typo_in_name_match_distance_threshold=1,
                 update_callback=None):
        """
        Configure the DuplicateDeleter using the arguments of this constructor.

        :param duplicate_match_threshold: The threshold of similarity required
        between two entries for them to be considered duplicates. This is
        measured in percentages. Default is 80% similar.
        :param potential_match_threshold: The threshold of similarity required
        between two entries for the entries to be potentially considered to be
        duplicates. This is measured in percentages. Default is 30% similar.
        :param minimum_str_length_for_potential_matches: The minimum length of
        the two entries' strings that are being compared. Default is 400
        characters. The shorter a string is, the poorer the comparison results
        are with fuzzy hashing. A minimum length of 400 characters means 200
        characters per entry.
        :param potential_bday_match_name_distance_threshold: The maximum
        Levenshtein distance between names when trying to match potential
        matches with date of birth.
        :param potential_typo_in_name_match_distance_threshold: The maximum
        Levenshtein distance between names when trying to match potential
        matches with name alone.
        """
        self._duplicate_match_threshold = duplicate_match_threshold
        self._potential_match_threshold = potential_match_threshold
        self._min_str_for_potential = minimum_str_length_for_potential_matches
        self._potential_bday_match_name_distance_threshold = potential_bday_match_name_distance_threshold
        self._potential_typo_in_name_match_distance_threshold = potential_typo_in_name_match_distance_threshold
        self._unique_entries = {}
        self._potential_matches = []
        self._update_callback_function = update_callback

        birthday_regex_pattern = r'(?:synt)\.?,?(?:\s+)?(?:(?:(?P<day>\d{1,2})(?:\.|,|:|\s+|s)\s?(?P<month>\d{1,2})(?:\.|,|:|\s+|s)?(?:\s+)?-?(?P<year>\d{2,4}))|\s?-(?P<yearOnly>\d{2,4})(?!\.|,|\s|\d)(?=\D\D\D\D\D))'
        self._BIRTHDAY_REGEX = regex.compile(birthday_regex_pattern, regex.UNICODE | regex.IGNORECASE)

    def delete_duplicate_persons(self, xml_books):
        """
        This function begins the duplicate deletion process. To filter duplicates,
        various methods are used, from simply matching the names and the dates of
        birth, to comparing how similar entries are through fuzzy hashing. To
        properly perform this filtering, all books within a bookseries should be
        included in one go.

        :param xml_books: a list of lxml ElementTree objects in Kaira's format.
        <PERSON> tags inside <DATA> tags.
        :return:
        """
        duplicates_count = 0
        start_time = datetime.datetime.now()

        files_without_duplicates = []

        for book_id, book in enumerate(xml_books):
            print('Filtering duplicates in file number {}.'.format(book_id+1))
            unique_entry_id = 0
            files_without_duplicates.append(book)

            for entry_id, child in enumerate(files_without_duplicates[book_id]):
                if self._update_callback_function is not None:
                    self._update_callback_function(entry_id)

                current_entry = self._get_current_entry(child, unique_entry_id, book_id)
                unique_entry_match = self._try_to_find_matching_entry(current_entry)

                if unique_entry_match:
                    duplicates_count += 1
                    raw = child.find('RAW')

                    if len(unique_entry_match['text']) < len(raw.text):
                        book_of_unique_entry = files_without_duplicates[unique_entry_match['book']]
                        book_of_unique_entry[unique_entry_match['entry_index']].text = raw.text

                    files_without_duplicates[book_id].remove(child)
                else:
                    self._unique_entries[current_entry['unique_key']] = current_entry
                    unique_entry_id += 1

            print('File number {} filtering done.'.format(book_id+1))

        elapsed = datetime.datetime.now() - start_time
        results_string = '--------------\nFILTERING DONE\n--------------' \
                         '\nElapsed time: {} s\nDuplicates found: {}'.format(elapsed.seconds,
                                                                             duplicates_count)
        print(results_string)
        return files_without_duplicates

    def _get_date_of_birth(self, entry):
        bday_matches = self._BIRTHDAY_REGEX.search(entry)
        birthday = (None, None, None)
        if bday_matches:
            if bday_matches.group('yearOnly'):
                birthday = (None, None, bday_matches.group('yearOnly'))
            else:
                birthday = (bday_matches.group('day'), bday_matches.group('month'), bday_matches.group('year'))

        return birthday

    def _match_by_birthday_and_name(self, unique_key):
        """
        Simply try to match the current entry we are processing to any entry
        we have already encountered by date of birth and name. _unique_entries
        is a dict whose keys contain both the names and birth dates of each
        unique entry found so far, so we check if the current entry's key is
        in the dict's keys.

        :param unique_key: The unique key of the current entry, in the format
        '{name_of_person}{date_of_birth_of_person}'
        :return: None if there is no match, otherwise the match itself.
        """
        match = None
        if unique_key in self._unique_entries:
            match = self._unique_entries[unique_key]

        return match

    def _find_fuzzy_match_or_potential_matches(self, entry_hash):
        """
        Try to match the current entry to a previously encountered unique entry
        by comparing fuzzy hashes. The thresholds for whether to consider
        entries duplicates or not are set in the constructor of the class.
        While trying to find a fuzzy match, we also compile a list of potential
        matches. If there is no fuzzy hash comparison exceeding the duplicate
        match threshold, the potential matches are used later in another effort
        to figure out whether the current entry is a duplicate or not.

        :param entry_hash: The fuzzy hash of the current entry.
        :return: None if there is no match, otherwise the match itself.
        """
        match = None
        for key, unique_entry in self._unique_entries.items():
            comparison = ssdeep.compare(unique_entry['hash'], entry_hash)
            if comparison > self._duplicate_match_threshold:
                match = unique_entry
                break

            if comparison > self._potential_match_threshold:
                self._potential_matches.append(unique_entry)

        return match

    def _match_by_bday_and_dist_in_potential_matches(self, name, birthday, text):
        """
        If we fail to confirm that the current entry is a duplicate with the
        other matching methods, this is the final attempt to do so. Using
        the potential matches gathered during fuzzy hash comparisons, we try
        to find an entry whose date of birth is the same, and its name is
        fairly similar. If that fails, we still look for people whose names
        are very similar, essentially we are looking through potential matches
        for people who are likely to be duplicates but there is a typo in the
        name. The name comparison is done using Levenshtein distance.

        :param name: Name of current person entry, to be compared to entries
        in potential matches.
        :param birthday: Date of birth of current person entry, to be compared
        to entries in potential matches.
        :param text: The text of the current person entry, used to make sure
        the entry's text is long enough for fuzzy hash comparison to be
        reliable.
        :return: None if there is no match, otherwise the match itself.
        """
        match = None
        for unique_entry in self._potential_matches:
            name_dist = distance(name, unique_entry['name'])
            if (birthday == unique_entry['birthday'] and
                    len('{}{}'.format(unique_entry['text'], text)) > 400 and
                    name_dist <= self._potential_bday_match_name_distance_threshold):
                match = unique_entry
            elif name_dist <= self._potential_typo_in_name_match_distance_threshold:
                match = unique_entry

        return match

    def _try_to_find_matching_entry(self, current_entry):
        """
        Tries to find an entry in the already-processed entriess that is likely
        to be the same person as this is. Check the docstrings for the matching
        functions themselves for details on how this works.

        :param current_entry: The current entry that is to be compared against
        all previous entries.
        :return: None if there is no match, otherwise the match itself.
        """
        matching_entry = self._match_by_birthday_and_name(current_entry['unique_key'])

        if not matching_entry:
            matching_entry = self._find_fuzzy_match_or_potential_matches(current_entry['hash'])

        if not matching_entry:
            matching_entry = self._match_by_bday_and_dist_in_potential_matches(
                current_entry['name'],
                current_entry['birthday'],
                current_entry['text']
            )
            self._potential_matches.clear()

        return matching_entry

    def _get_current_entry(self, child, entry_id, book_number):
        """
        Compiles all of the various data about the current entry into a single
        dict object.
        :param child: The XML Element object of the current <PERSON> entry.
        :param entry_id: The index of the current entry.
        :param book_number: The number of the book this entry is in.
        :return: A dict with all of the relevant data about the person for
        duplicate matching. Keys: 'name', 'birthday', 'text', 'hash',
        'unique_key', 'entry_index', 'book'.
        """
        name_processed = child.attrib['name'].replace('.', ',')
        raw = child.find('RAW')
        birthday = self._get_date_of_birth(raw.text)
        current_entry = {
            'name': name_processed,
            'birthday': birthday,
            'text': raw.text,
            'hash': ssdeep.hash(raw.text),
            'unique_key': '{}{}'.format(name_processed, birthday),
            'entry_index': entry_id,
            'book': book_number
        }

        return current_entry

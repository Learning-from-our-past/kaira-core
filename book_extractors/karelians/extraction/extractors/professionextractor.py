from book_extractors.common.base_extractor import BaseExtractor
from book_extractors.common.extraction_keys import KEYS
import shared.textUtils as textUtils
import shared.regexUtils as regexUtils
import re


class ProfessionExtractor(BaseExtractor):
    SEARCH_SPACE = 60

    def __init__(self, options):
        super(ProfessionExtractor, self).__init__(options)
        self.PROFESSION_PATTERN = r"(?<profession>[a-zä-ö,\. ]*) synt"
        self.PROFESSION_OPTIONS = (re.UNICODE | re.IGNORECASE)

    def extract(self, entry, start_position=0):
        profession_results = self._find_profession(entry['text'], start_position)

        return self._constructReturnDict({
            KEYS["profession"]: profession_results[0]
        }, profession_results[1])


    def _find_profession(self, text, start_position):
        text = textUtils.takeSubStrBasedOnRange(text, start_position, self.SEARCH_SPACE)
        cursor_location = 0
        profession = ''

        try:
            #limit the search range if there is spouse keyword:
            try:
                found_spouse_word = regexUtils.safeSearch(r"Puol", text, self.PROFESSION_OPTIONS)
                text = textUtils.takeSubStrBasedOnRange(text, 0, found_spouse_word.start())
            except regexUtils.RegexNoneMatchException as e:
                pass

            found_profession_match = regexUtils.safeSearch(self.PROFESSION_PATTERN, text, self.PROFESSION_OPTIONS)

            cursor_location = found_profession_match.end()
            profession = found_profession_match.group("profession")
        except regexUtils.RegexNoneMatchException as e:
            pass

        result_profession = self._clean_professions(profession)

        return result_profession, cursor_location

    def _clean_professions(self, profession):
        profession = profession.strip(",")
        profession = profession.strip()
        profession = profession.lstrip()

        uppercase = re.match(r"[A-ZÄ-Ö]", profession)
        if uppercase is not None:
            comma = profession.find(",")
            if comma != -1:
                profession = profession[comma:]

        profession = profession.strip(",")
        profession = profession.strip(".")
        profession = profession.strip()
        profession = profession.lstrip()
        profession = re.sub(r"[a-zä-ö]{1,3}(?:,|\.)\s", "", profession, self.PROFESSION_OPTIONS)

        if len(profession) < 3:
            profession = ""

        if profession == "":
            # TODO: Metadata logging here  self.errorLogger.logError(ProfessionException.eType, self.currentChild)
            pass

        return profession

"""
This class defines the progress and order of the extraction process by initializing and calling
required extractors.
"""
from book_extractors.karelians.extraction.extractors.nameextractor import NameExtractor
from book_extractors.karelians.extraction.extractors.origfamilyextractor import OrigFamilyExtractor
from book_extractors.karelians.extraction.extractors.professionextractor import ProfessionExtractor
from book_extractors.karelians.extraction.extractors.imageextractor import ImageExtractor
from book_extractors.karelians.extraction.extractors.omakotitaloextractor import OmakotitaloExtractor
from book_extractors.karelians.extraction.extractors.birthdayExtractor import BirthdayExtractor
from book_extractors.karelians.extraction.extractors.locationExtractor import BirthdayLocationExtractor
from book_extractors.karelians.extraction.extractors.migration_route_extractors import FinnishLocationsExtractor, KarelianLocationsExtractor
from book_extractors.karelians.extraction.extractors.spouseextractor import SpouseExtractor
from book_extractors.karelians.extraction.extractors.childextractor import ChildExtractor
from shared.genderExtract import Gender
import re


class ExtractionPipeline:

    def __init__(self, person_data_input):
        self.person_data = person_data_input
        Gender.load_names()

    def process(self, person, eLogger):
        # Replace all weird invisible white space characters with regular space
        text = person['text'] = re.sub(r"\s", r" ", person['text'])

        name_ext = NameExtractor(person, eLogger)
        names = name_ext.extract(text, person)

        image_ext = ImageExtractor(person, eLogger)
        image = image_ext.extract(text, person)

        orig_family_ext = OrigFamilyExtractor(person, eLogger)
        orig_family_ext.setDependencyMatchPositionToZero()
        orig_family = orig_family_ext.extract(text, person)

        profession_ext = ProfessionExtractor(person, eLogger)
        profession_ext.dependsOnMatchPositionOf(orig_family_ext)
        profession = profession_ext.extract(text, person)

        birthday_ext = BirthdayExtractor(person, eLogger)
        birthday_ext.dependsOnMatchPositionOf(orig_family_ext)
        birthday = birthday_ext.extract(text, person)

        birth_loc_ext = BirthdayLocationExtractor(person, eLogger)
        birth_loc_ext.dependsOnMatchPositionOf(birthday_ext)
        birthday_location = birth_loc_ext.extract(text, person)

        karelian_loc_ext = KarelianLocationsExtractor(person, eLogger)
        karelian_locations = karelian_loc_ext.extract(text, person)

        finnish_loc_ext = FinnishLocationsExtractor(person, eLogger)
        finnish_locations = finnish_loc_ext.extract(text, person)

        omakotitalo_ext = OmakotitaloExtractor(person, eLogger)
        omakotitalo = omakotitalo_ext.extract(text, person)

        spouse_ext = SpouseExtractor(person, eLogger)
        spouse = spouse_ext.extract(text, person)

        child_ext = ChildExtractor(person, eLogger)
        children = child_ext.extract(text, person)

        d = names.copy()
        d.update(image)
        d.update(orig_family)
        d.update(profession)
        d.update(omakotitalo)
        d.update(birthday)
        d.update(birthday_location)
        d.update(karelian_locations)
        d.update(finnish_locations)
        d.update(spouse)
        d.update(children)
        d["originalText"] = text
        return d

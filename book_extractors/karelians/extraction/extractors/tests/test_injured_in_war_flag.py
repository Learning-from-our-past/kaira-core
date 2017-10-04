import pytest
from book_extractors.karelians.extraction.extractors.injured_in_war_flag_extractor import InjuredInWarFlagExtractor

class TestInjuredInWarFlag:

    @pytest.yield_fixture(autouse=True)
    def extractor(self):
        return InjuredInWarFlagExtractor(None, None)

    def _verify_flags(self, expected_flags_and_texts, extractor, gender = 'Male'):
        extraction_results = {'primaryPerson': {'name': {'gender': gender}}}
        flag = 'injuredInWarFlag'

        for e in expected_flags_and_texts:
            results, metadata = extractor.extract({'text': e[0]}, extraction_results, {})
            assert results[flag] is e[1]

    def should_return_true_if_text_contains_mentions_of_being_injured(self, extractor):
        self._verify_flags([
            ('Nyymi on sotamies, ja hän palveli JP 1;ssä. Hän haavoittui v. -44 ja on 30 %;n sotainvalidi.', True),
            ('Sodassa haavoittumisen vuoksi hän on 30 % invaliidi.', True)
        ], extractor)

    def should_return_true_if_text_contains_mentions_of_being_injured_and_a_hyphen(self, extractor):
        self._verify_flags([
            ('Nyymi on sotamies, ja hän palveli JP 1;ssä. Hän haavoit-tui v. -44 ja on 30 %;n sotainvalidi.', True)
        ], extractor)

    def should_return_true_if_text_contains_mentions_of_being_injured_and_a_typo(self, extractor):
        self._verify_flags([
            ('Joku on sotamies ja palvellut jatkosodassa JvKoulK 2:ssa ja 4./JR 6:ssa. Hän haavoi7tui kaksi kertaa.', True)
        ], extractor)

    def should_return_true_if_text_contains_mentions_of_being_warhandicapped(self, extractor):
        self._verify_flags([
            ('asuvat osakehuoneistossa. Rakennusmestari Joku on 20 %:n sotainvalidi. Hänelle on myönnetty', True)
        ], extractor)

    def should_return_true_if_text_contains_mentions_of_being_warhandicapped_and_a_hyphen(self, extractor):
        self._verify_flags([
            ('asuvat osakehuoneistossa. Rakennusmestari Joku on 20 %:n sota-invalidi. Hänelle on myönnetty', True)
        ], extractor)

    def should_return_true_if_text_contains_mentions_of_being_warhandicapped_and_a_typo(self, extractor):
        self._verify_flags([
            ('Hän on sotamies ja palvellut jatkosodassa JR 6:ssa. Hän on 60 %:n sotainvalibi.', True)
        ], extractor)

    def should_return_false_if_text_does_not_mention_injury_or_being_warhandicapped(self, extractor):
        self._verify_flags([
            ('Joku Meikäläinen on kersantti ja palveli talvisodassa 1./VKK:ssa, 2./VP 19:ssä ja '
             '2./VP 1 :ssä sekä jatkosodassa 1./RaskPsto 14:s sä. Hänelle on myönnetty Vm 2, Ts '
             'mm sekä Js mm. Hän on Lauritsalan Kisan jäsen. Hän kuuluu Paperityöväenliittoon Ul'
             'koilu ja pihanhoito sekä hiihto ovat hänen mieliharrastuksiaan. Rouva Ni-me-tön ku'
             'uluu Liiketyöntekijöihin. Käsityöt ovat hänen harrastuksiaan.', False)
        ], extractor)

    def should_return_false_if_text_mentions_warhandicapped_in_wrong_context(self, extractor):
        self._verify_flags([
            ('Satunnainen heppuu asuu yhdessä äitinsä, Satunnaisen Äidin kanssa sotainvalidien talossa.', False),
            ('Hän kuuluu Karjalaseuraan, Rakennustyöväen liittoon ja Sotainvalidien Veljesliittoon.', False)
        ], extractor)

    def should_return_none_if_primaryperson_gender_is_female(self, extractor):
        self._verify_flags([
            ('Hän on sotamies ja palvellut jatkosodassa JR 6:ssa. Hän on 60 %:n sotainvalidi.', None)
        ], extractor, gender='Female')

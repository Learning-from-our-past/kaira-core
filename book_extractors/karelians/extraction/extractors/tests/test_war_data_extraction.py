import pytest
from book_extractors.karelians.extraction.extractors.war_data_extractor import WarDataExtractor
from book_extractors.karelians.extraction.extractors.injured_in_war_flag_extractor import InjuredInWarFlagExtractor
from book_extractors.karelians.extraction.extractors.served_during_war_flag_extractor import ServedDuringWarFlagExtractor
from book_extractors.karelians.extraction.extractors.lotta_activity_flag_extractor import LottaActivityFlagExtractor


class TestWarDataExtraction:
    @pytest.yield_fixture(autouse=True)
    def extractor(self):
        return WarDataExtractor(None, None)

    def _verify_flags(self, expected_flags_and_texts, extractor, subflag, gender):
        extractor_prerequisite_results = {'primaryPerson': {'name': {'gender': gender}}}
        flag = 'warData'

        for e in expected_flags_and_texts:
            results, metadata = extractor.extract({'text': e[0]}, extractor_prerequisite_results, {})
            assert results[flag][subflag] is e[1]

    def _verify_lotta_flag(self, expected_flags_and_texts, extractor, gender):
        extractor_prerequisite_results = {'primaryPerson': {'name': {'gender': gender}}, 'spouse': {}}
        flag = 'warData'
        subflag = 'lottaActivityFlag'

        for e in expected_flags_and_texts:
            results, metadata = extractor.extract({'text': e[0]}, extractor_prerequisite_results, {})
            if gender == 'Male':
                assert results[flag][subflag] is None
                assert results['spouse'][subflag] is e[1]
            else:
                assert results[flag][subflag] is e[1]

    def should_extract_injured_in_war_flag_correctly_as_true_if_primary_person_is_male(self, extractor):
        self._verify_flags([
            ('Nyymi on sotamies, ja hän palveli JP 1;ssä. Hän haavoittui v. -44 ja on 30 %;n sotainvalidi.', True)
        ], extractor, 'injuredInWarFlag', 'Male')

    def should_extract_injured_in_war_flag_correctly_as_none_if_primary_person_is_female(self, extractor):
        self._verify_flags([
            ('Hän on sotamies ja palvellut jatkosodassa JR 6:ssa. Hän on 60 %:n sotainvalidi.', None)
        ], extractor, 'injuredInWarFlag', 'Female')

    def should_extract_served_during_war_flag_correctly_as_true_if_primary_person_is_male(self, extractor):
        self._verify_flags([
            ('Herra Testilä oli molemmissa sodissa mukana palvellen tykkimiehenä.', True)
        ], extractor, 'servedDuringWarFlag', 'Male')

    def should_extract_served_during_war_flag_correctly_as_none_if_primary_person_is_female(self, extractor):
        self._verify_flags([
            ('Rouva Testilä oli molemmissa sodissa mukana palvellen ironmanina.', None)
        ], extractor, 'servedDuringWarFlag', 'Female')

    def should_extract_lotta_activity_flag_correctly_as_true_if_female(self, extractor):
        self._verify_lotta_flag([
            ('Emäntä oli sota-aikana mukana lottatoiminnas-sa ja hän on saanut talvisodan muistomitalin.', True)
        ], extractor, "Female")

    def should_extract_lotta_activity_flag_correctly_as_true_for_spouse_if_male_and_none_for_person(self, extractor):
        self._verify_lotta_flag([
            ('Emäntä oli sota-aikana mukana lottatoiminnas-sa ja hän on saanut talvisodan muistomitalin.', True)
        ], extractor, "Male")


class TestInjuredInWarFlag:
    @pytest.yield_fixture(autouse=True)
    def extractor(self):
        return InjuredInWarFlagExtractor(None, None)

    def _verify_flags(self, expected_flags_and_texts, extractor):
        flag = 'injuredInWarFlag'

        for e in expected_flags_and_texts:
            results, metadata = extractor.extract({'text': e[0]}, {}, {})
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


class TestServedDuringWarFlagExtraction:
    @pytest.yield_fixture(autouse=True)
    def extractor(self):
        return ServedDuringWarFlagExtractor(None, None)

    def _verify_flags(self, expected_flags_and_texts, extractor):
        flag = 'servedDuringWarFlag'

        for e in expected_flags_and_texts:
            results, metadata = extractor.extract({'text': e[0]}, {}, {})
            assert results[flag] is e[1]

    def should_return_true_if_text_contains_mention_of_having_served_with_lut_suffix(self, extractor):
        self._verify_flags([
            ('Herra Alikersantti on sotilasarvoltaan alikersantti ja palvellut jatkosodassa ETp/VAK:ssa '
             'sekä ErP 21:ssa.', True)
        ], extractor)

    def should_return_true_if_text_contains_mention_of_having_served_with_li_suffix(self, extractor):
        self._verify_flags([
            ('Muut asuinp.: Kuhmoinen, Orimattila, Perniö 44—, Paimio. Sota Mies palveli sotamiehen'
             'ä jatkosodassa JR 20:ssa, Vapaa-aikansa hän viettää lueskellen.', True)
        ], extractor)

    def should_return_true_if_text_contains_mention_of_having_served_with_len_suffix(self, extractor):
        self._verify_flags([
            ('Herra Testilä oli molemmissa sodissa mukana palvellen tykkimiehenä.', True)
        ], extractor)

    def should_return_true_if_text_contains_mention_of_having_served_with_substitutions_and_or_hyphen(self, extractor):
        self._verify_flags([
            ('Herra Alikersantti on sotilasarvoltaan alikersantti ja pa1-vellut jatkosodassa ETp/VAK:ssa '
             'sekä ErP 21:ssa.', True)
        ], extractor)

    def should_return_false_if_text_contains_no_mention_of_having_served(self, extractor):
        self._verify_flags([
            ('Nimettömät asuvat rakentamassaan omakotitalossa. Nyrkkeilijä Nimetön on ammattiosaston jäsen '
             'ja kuuluu nuorisojaostoon. Hän harrastaa yleisurheilua, nyrkkeilyä ja hiihtoa. Nimetön on voi'
             'ttanut seiväshypyssä piirin mestaruuksia. Hän lukee ammattikirjallisuutta. Rouva Nimetön on o'
             'piskellut työväenopistossa. Rouva harrastaa puutarhanhoitoa, käsitöitä ja kirjallisuutta. Hän'
             'on ottanut osaa kirkollisiin toimiin. Herran äiti, Äiti Nimetön o.s. Epänimetön, asuu Kaarlel'
             'assa omakotitalossa.', False)
        ], extractor)

    def should_return_false_if_text_contains_mention_of_having_served_with_luksessa_suffix(self, extractor):
        self._verify_flags([
            ('Rautateiden Partaveitsi on ollut vuodesta -48 lähtien valtion rautateiden palveluksessa.', False)
        ], extractor)


class TestLottaActivityFlagExtraction:
    @pytest.yield_fixture(autouse=True)
    def extractor(self):
        return LottaActivityFlagExtractor(None, None)

    def _verify_flags(self, expected_flags_and_texts, extractor):
        flag = 'lottaActivityFlag'

        for e in expected_flags_and_texts:
            results, metadata = extractor.extract({'text': e[0]}, {}, {})
            assert results[flag] is e[1]

    def should_return_true_if_text_contains_mention_of_lotta_activity(self, extractor):
        self._verify_flags([
            ('Emäntä oli sota-aikana mukana lottatoiminnas-sa ja hän on saanut talvisodan muistomitalin.', True)
        ], extractor)

    def should_return_true_if_text_contains_mention_of_lotta_activity_with_typo(self, extractor):
        self._verify_flags([
            ('Emäntä oli sota-aikana mukana lot7atoiminnas-sa ja hän on saanut talvisodan muistomitalin.', True)
        ], extractor)

    def should_return_true_if_text_contains_mention_of_lotta_activity_with_hyphen(self, extractor):
        self._verify_flags([
            ('Emäntä oli sota-aikana mukana lot-tatoiminnas-sa ja hän on saanut talvisodan muistomitalin.', True)
        ], extractor)

    def should_return_true_if_text_contains_mention_of_lotta_activity_with_typo_and_hyphen(self, extractor):
        self._verify_flags([
            ('Emäntä oli sota-aikana mukana l0t-tatoiminnas-sa ja hän on saanut talvisodan muistomitalin.', True)
        ], extractor)

    def should_return_false_if_text_does_not_contain_mention_of_lotta_activity(self, extractor):
        self._verify_flags([
            ('Emäntä oli sota-aikana tanssilattioiden partaveitsi eikä piitannut sotatoiminnasta.', False)
        ], extractor)
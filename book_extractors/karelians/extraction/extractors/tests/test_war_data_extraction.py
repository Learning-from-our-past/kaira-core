import pytest
from book_extractors.karelians.extraction.extractors.war_data_extractor import WarDataExtractor
from book_extractors.karelians.extraction.extractors.injured_in_war_flag_extractor import InjuredInWarFlagExtractor
from book_extractors.karelians.extraction.extractors.served_during_war_flag_extractor import ServedDuringWarFlagExtractor
from book_extractors.extraction_pipeline import ExtractionPipeline, configure_extractor
from book_extractors.karelians.extraction.extractors.lotta_activity_flag_extractor import LottaActivityFlagExtractor


class TestWarDataExtraction:
    @pytest.yield_fixture(autouse=True)
    def extractor(self):
        return WarDataExtractor(None, {'in_spouse_extractor': False})

    def _verify_flags(self, expected_flags_and_texts, extractor, subflag, gender):
        flag = 'warData'
        parent_data = {'extraction_results': {'primaryPerson': {'name': {'gender': gender}}},
                       'parent_data': None}

        for e in expected_flags_and_texts:
            results, metadata = extractor.extract({'text': e[0]}, {}, {},
                                                  parent_pipeline_data=parent_data)
            assert results[flag][subflag] == e[1]

    def should_extract_injured_in_war_flag_correctly_as_true_if_primary_person_is_male(self, extractor):
        self._verify_flags([
            ('Nyymi on sotamies, ja hän palveli JP 1;ssä. Hän haavoittui v. -44 ja on 30 %;n sotainvalidi.', True)
        ], extractor, 'injuredInWarFlag', 'Male')

    def should_extract_served_during_war_flag_correctly_as_true_if_primary_person_is_male(self, extractor):
        self._verify_flags([
            ('Herra Testilä oli molemmissa sodissa mukana palvellen tykkimiehenä.', True)
        ], extractor, 'servedDuringWarFlag', 'Male')

    def should_extract_lotta_activity_flag_correctly_as_true_if_primary_person_is_female(self, extractor):
        expected_result = {'lotta': True,
                           'foodLotta': False}
        self._verify_flags([
            ('Emäntä oli sota-aikana mukana lottatoiminnas-sa ja hän on saanut talvisodan muistomitalin.', expected_result)
        ], extractor, LottaActivityFlagExtractor.extraction_key, 'Female')


class TestInjuredInWarFlag:
    def _verify_flags(self, expected_flags_and_texts, in_spouse=False, sex='Male'):
        flag = 'injuredInWarFlag'
        parent_data = {'extraction_results': {'name': {'gender': sex}},
                       'parent_data': None}

        pipeline = ExtractionPipeline([
            configure_extractor(InjuredInWarFlagExtractor, extractor_options={'in_spouse_extractor': in_spouse},
                                dependencies_contexts=['main'])
        ])

        for e in expected_flags_and_texts:
            results, metadata = pipeline.process({'text': e[0]}, parent_pipeline_data=parent_data)
            assert results[flag] is e[1]

    def should_return_true_if_text_contains_mentions_of_being_injured(self):
        self._verify_flags([
            ('Nyymi on sotamies, ja hän palveli JP 1;ssä. Hän haavoittui v. -44 ja on 30 %;n sotainvalidi.', True),
            ('Sodassa haavoittumisen vuoksi hän on 30 % invaliidi.', True)
        ])

    def should_return_true_if_text_contains_mentions_of_being_injured_and_a_hyphen(self):
        self._verify_flags([
            ('Nyymi on sotamies, ja hän palveli JP 1;ssä. Hän haavoit-tui v. -44 ja on 30 %;n sotainvalidi.', True)
        ])

    def should_return_true_if_text_contains_mentions_of_being_injured_and_a_typo(self):
        self._verify_flags([
            ('Joku on sotamies ja palvellut jatkosodassa JvKoulK 2:ssa ja 4./JR 6:ssa. Hän haavoi7tui kaksi kertaa.', True)
        ])

    def should_return_true_if_text_contains_mentions_of_being_warhandicapped(self):
        self._verify_flags([
            ('asuvat osakehuoneistossa. Rakennusmestari Joku on 20 %:n sotainvalidi. Hänelle on myönnetty', True)
        ])

    def should_return_true_if_text_contains_mentions_of_being_warhandicapped_and_a_hyphen(self):
        self._verify_flags([
            ('asuvat osakehuoneistossa. Rakennusmestari Joku on 20 %:n sota-invalidi. Hänelle on myönnetty', True)
        ])

    def should_return_true_if_text_contains_mentions_of_being_warhandicapped_and_a_typo(self):
        self._verify_flags([
            ('Hän on sotamies ja palvellut jatkosodassa JR 6:ssa. Hän on 60 %:n sotainvalibi.', True)
        ])

    def should_return_false_if_text_does_not_mention_injury_or_being_warhandicapped(self):
        self._verify_flags([
            ('Joku Meikäläinen on kersantti ja palveli talvisodassa 1./VKK:ssa, 2./VP 19:ssä ja '
             '2./VP 1 :ssä sekä jatkosodassa 1./RaskPsto 14:s sä. Hänelle on myönnetty Vm 2, Ts '
             'mm sekä Js mm. Hän on Lauritsalan Kisan jäsen. Hän kuuluu Paperityöväenliittoon Ul'
             'koilu ja pihanhoito sekä hiihto ovat hänen mieliharrastuksiaan. Rouva Ni-me-tön ku'
             'uluu Liiketyöntekijöihin. Käsityöt ovat hänen harrastuksiaan.', False)
        ])

    def should_return_false_if_text_mentions_warhandicapped_in_wrong_context(self):
        self._verify_flags([
            ('Satunnainen heppuu asuu yhdessä äitinsä, Satunnaisen Äidin kanssa sotainvalidien talossa.', False),
            ('Hän kuuluu Karjalaseuraan, Rakennustyöväen liittoon ja Sotainvalidien Veljesliittoon.', False)
        ])

    def should_return_true_if_text_mentions_being_warhandicapped_and_primary_person_sex_is_female_and_we_are_in_spouse_extractor(self):
        self._verify_flags([
            ('asuvat osakehuoneistossa. Rakennusmestari Joku on 20 %:n sotainvalidi. Hänelle on myönnetty', True)
        ], in_spouse=True, sex='Female')

    def should_return_none_if_primary_person_sex_is_female_and_we_are_not_in_spouse_extractor(self):
        self._verify_flags([
            ('asuvat osakehuoneistossa. Rakennusmestari Joku on 20 %:n sotainvalidi. Hänelle on myönnetty', None)
        ], in_spouse=False, sex='Female')

    def should_return_none_if_primary_person_sex_is_male_and_we_are_in_spouse_extractor(self):
        self._verify_flags([
            ('asuvat osakehuoneistossa. Rakennusmestari Joku on 20 %:n sotainvalidi. Hänelle on myönnetty', None)
        ], in_spouse=True, sex='Male')

    def should_return_false_if_text_does_not_mention_being_warhandicapped_or_wounded_and_primary_person_sex_is_female_and_we_are_in_spouse_extractor(self):
        self._verify_flags([
            ('Joku Meikäläinen on kersantti ja palveli talvisodassa 1./VKK:ssa, 2./VP 19:ssä ja '
             '2./VP 1 :ssä sekä jatkosodassa 1./RaskPsto 14:s sä. Hänelle on myönnetty Vm 2, Ts '
             'mm sekä Js mm. Hän on Lauritsalan Kisan jäsen. Hän kuuluu Paperityöväenliittoon Ul'
             'koilu ja pihanhoito sekä hiihto ovat hänen mieliharrastuksiaan. Rouva Ni-me-tön ku'
             'uluu Liiketyöntekijöihin. Käsityöt ovat hänen harrastuksiaan.', False)
        ], in_spouse=True, sex='Female')


class TestServedDuringWarFlagExtraction:
    def _verify_flags(self, expected_flags_and_texts, in_spouse=False, sex='Male'):
        flag = ServedDuringWarFlagExtractor.extraction_key
        parent_data = {'extraction_results': {'name': {'gender': sex}},
                       'parent_data': None}

        pipeline = ExtractionPipeline([
            configure_extractor(ServedDuringWarFlagExtractor, extractor_options={'in_spouse_extractor': in_spouse},
                                dependencies_contexts=['main'])
        ])

        for e in expected_flags_and_texts:
            results, metadata = pipeline.process({'text': e[0]}, parent_pipeline_data=parent_data)
            assert results[flag] is e[1]

    def should_return_true_if_text_contains_mention_of_having_served_with_lut_suffix(self):
        self._verify_flags([
            ('Herra Alikersantti on sotilasarvoltaan alikersantti ja palvellut jatkosodassa ETp/VAK:ssa '
             'sekä ErP 21:ssa.', True)
        ])

    def should_return_true_if_text_contains_mention_of_having_served_with_li_suffix(self):
        self._verify_flags([
            ('Muut asuinp.: Kuhmoinen, Orimattila, Perniö 44—, Paimio. Sota Mies palveli sotamiehen'
             'ä jatkosodassa JR 20:ssa, Vapaa-aikansa hän viettää lueskellen.', True)
        ])

    def should_return_true_if_text_contains_mention_of_having_served_with_len_suffix(self):
        self._verify_flags([
            ('Herra Testilä oli molemmissa sodissa mukana palvellen tykkimiehenä.', True)
        ])

    def should_return_true_if_text_contains_mention_of_having_served_with_substitutions_and_or_hyphen(self):
        self._verify_flags([
            ('Herra Alikersantti on sotilasarvoltaan alikersantti ja pa1-vellut jatkosodassa ETp/VAK:ssa '
             'sekä ErP 21:ssa.', True)
        ])

    def should_return_false_if_text_contains_no_mention_of_having_served(self):
        self._verify_flags([
            ('Nimettömät asuvat rakentamassaan omakotitalossa. Nyrkkeilijä Nimetön on ammattiosaston jäsen '
             'ja kuuluu nuorisojaostoon. Hän harrastaa yleisurheilua, nyrkkeilyä ja hiihtoa. Nimetön on voi'
             'ttanut seiväshypyssä piirin mestaruuksia. Hän lukee ammattikirjallisuutta. Rouva Nimetön on o'
             'piskellut työväenopistossa. Rouva harrastaa puutarhanhoitoa, käsitöitä ja kirjallisuutta. Hän'
             'on ottanut osaa kirkollisiin toimiin. Herran äiti, Äiti Nimetön o.s. Epänimetön, asuu Kaarlel'
             'assa omakotitalossa.', False)
        ])

    def should_return_false_if_text_contains_mention_of_having_served_with_luksessa_suffix(self):
        self._verify_flags([
            ('Rautateiden Partaveitsi on ollut vuodesta -48 lähtien valtion rautateiden palveluksessa.', False)
        ])

    def should_return_true_if_text_mentions_having_served_and_primary_person_sex_is_female_and_we_are_in_spouse_extractor(self):
        self._verify_flags([
            ('Herra Alikersantti on sotilasarvoltaan alikersantti ja palvellut jatkosodassa ETp/VAK:ssa '
             'sekä ErP 21:ssa.', True)
        ], in_spouse=True, sex='Female')

    def should_return_none_if_primary_person_sex_is_female_and_we_are_not_in_spouse_extractor(self):
        self._verify_flags([
            ('Herra Alikersantti on sotilasarvoltaan alikersantti ja palvellut jatkosodassa ETp/VAK:ssa '
             'sekä ErP 21:ssa.', None)
        ], in_spouse=False, sex='Female')

    def should_return_none_if_primary_person_sex_is_male_and_we_are_in_spouse_extractor(self):
        self._verify_flags([
            ('Herra Alikersantti on sotilasarvoltaan alikersantti ja palvellut jatkosodassa ETp/VAK:ssa '
             'sekä ErP 21:ssa.', None)
        ], in_spouse=True, sex='Male')

    def should_return_false_if_text_does_not_mention_having_served_and_primary_person_sex_is_female_and_we_are_in_spouse_extractor(self):
        self._verify_flags([
            ('Nimettömät asuvat rakentamassaan omakotitalossa. Nyrkkeilijä Nimetön on ammattiosaston jäsen '
             'ja kuuluu nuorisojaostoon. Hän harrastaa yleisurheilua, nyrkkeilyä ja hiihtoa. Nimetön on voi'
             'ttanut seiväshypyssä piirin mestaruuksia. Hän lukee ammattikirjallisuutta. Rouva Nimetön on o'
             'piskellut työväenopistossa. Rouva harrastaa puutarhanhoitoa, käsitöitä ja kirjallisuutta. Hän'
             'on ottanut osaa kirkollisiin toimiin. Herran äiti, Äiti Nimetön o.s. Epänimetön, asuu Kaarlel'
             'assa omakotitalossa.', False)
        ], in_spouse=True, sex='Female')


def verify_flags(expected_flags_and_texts, in_spouse=False, sex='Female', subflag='lotta'):
    flag = LottaActivityFlagExtractor.extraction_key
    parent_data = {'extraction_results': {'name': {'gender': sex}},
                   'parent_data': None}

    pipeline = ExtractionPipeline([
        configure_extractor(LottaActivityFlagExtractor, extractor_options={'in_spouse_extractor': in_spouse},
                            dependencies_contexts=['main'])
    ])

    for e in expected_flags_and_texts:
        results, metadata = pipeline.process({'text': e[0]}, parent_pipeline_data=parent_data)
        assert results[flag][subflag] is e[1]


class TestLottaActivityFlagsExtraction:
    def should_return_true_if_text_contains_mention_of_lotta_activity(self):
        verify_flags([
            ('Emäntä oli sota-aikana mukana lottatoiminnas-sa ja hän on saanut talvisodan muistomitalin.', True)
        ])

    def should_return_true_if_text_contains_mention_of_lotta_activity(self):
        verify_flags([
            ('Emäntä oli sota-aikana mukana lottatoiminnas-sa ja hän on saanut talvisodan muistomitalin.', True)
        ], in_spouse=True, sex='Male')

    def should_return_true_if_text_contains_mention_of_lotta_activity_with_typo_and_hyphen(self):
        verify_flags([
            ('Emäntä oli sota-aikana mukana l0t-tatoiminnas-sa ja hän on saanut talvisodan muistomitalin.', True)
        ])

    def should_return_false_if_text_does_not_contain_mention_of_lotta_activity(self):
        verify_flags([
            ('Emäntä oli sota-aikana tanssilattioiden partaveitsi eikä piitannut sotatoiminnasta.', False)
        ], in_spouse=False, sex='Female')

    def should_return_false_if_text_does_not_contain_mention_of_lotta_activity(self):
        verify_flags([
            ('Emäntä oli sota-aikana tanssilattioiden partaveitsi eikä piitannut sotatoiminnasta.', False)
        ], in_spouse=True, sex='Male')

    def should_return_false_if_text_contains_lotta_name(self):
        verify_flags([
            ('Emännän nimi oli Lotta ja hän', False)
        ], in_spouse=False, sex='Female')

    def should_return_false_if_text_contains_word_vuotta(self):
        verify_flags([
            ('Emäntä asui kymmenen vuotta Vitsauskylässä.', False)
        ], in_spouse=False, sex='Female')

    def should_return_false_if_text_contains_lotta_like_word_with_wrong_suffix(self):
        verify_flags([
            ('Emäntä tuli ulos omakotitalosta ja kirkui.', False),
            ('Emäntä oli luullut olevansa kiillottaja koko elämänsä ajan.', False)
        ], in_spouse=False, sex='Female')

    def should_return_none_if_primary_person_is_male_and_we_are_not_in_spouse_extractor(self):
        verify_flags([('foo', None)], in_spouse=False, sex='Male')

    def should_return_none_if_primary_person_is_female_and_we_are_in_spouse_extractor(self):
        verify_flags([('bar', None)], in_spouse=True, sex='Female')

    class TestFoodLottaFlag:
        def should_extract_foodlotta_true_if_text_contains_mention_of_lotta_working_in_a_food_role(self):
            verify_flags([
                ('Rouva toimi sota-aikana muonituslottana.', True),
                ('Sodan aikana hän oli kanttiinilottana.', True),
            ], in_spouse=False, sex='Female', subflag='foodLotta')

        def should_extract_foodlotta_true_if_text_contains_mention_of_lotta_working_in_a_food_role_with_typos(self):
            verify_flags([
                ('Rouva toimi sota-aikana muoni-tuslot-tana.', True),
                ('Sodan aikana hän oli kantt11nilottana.', True),
            ], in_spouse=False, sex='Female', subflag='foodLotta')

        def should_not_extract_foodlotta_when_there_is_no_mention_of_foodlotta_work(self):
            verify_flags([
                ('Rouva toimi sota-aikana kodinhoitajana.', False)
            ], in_spouse=False, sex='Female', subflag='foodLotta')

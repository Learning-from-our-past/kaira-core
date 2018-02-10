import pytest
from book_extractors.karelians.extraction.extractors.injured_in_war_flag_extractor import InjuredInWarFlagExtractor
from book_extractors.karelians.extraction.extractors.served_during_war_flag_extractor import ServedDuringWarFlagExtractor
from book_extractors.karelians.extraction.extractors.lotta_activity_flag_extractor import LottaActivityFlagExtractor


class TestInjuredInWarFlag:
    def _verify_flags(self, expected_flags_and_texts, result_map, in_spouse=False, sex='Male'):
        flag = 'injuredInWarFlag'

        result_map.add_results('mockPrimaryPerson', {'name': {'gender': sex}})

        # Wire the dependencies and mock result map directly to the extractor
        extractor = InjuredInWarFlagExtractor(None, {'in_spouse_extractor': in_spouse})
        extractor.set_extraction_results_map(result_map)
        extractor.set_required_dependencies(['mockPrimaryPerson'])

        for e in expected_flags_and_texts:
            shortened_text = e[0][0:15] # Make sure the extractor uses full_text, not this substring
            results, metadata = extractor.extract({'text': shortened_text, 'full_text': e[0]}, {}, {})
            assert results[flag] is e[1]

    def should_return_true_if_text_contains_mentions_of_being_injured(self, result_map):
        self._verify_flags([
            ('Nyymi on sotamies, ja hän palveli JP 1;ssä. Hän haavoittui v. -44 ja on 30 %;n sotainvalidi.', True),
            ('Sodassa haavoittumisen vuoksi hän on 30 % invaliidi.', True)
        ], result_map)

    def should_return_true_if_text_contains_mentions_of_being_injured_and_a_hyphen(self, result_map):
        self._verify_flags([
            ('Nyymi on sotamies, ja hän palveli JP 1;ssä. Hän haavoit-tui v. -44 ja on 30 %;n sotainvalidi.', True)
        ], result_map)

    def should_return_true_if_text_contains_mentions_of_being_injured_and_a_typo(self, result_map):
        self._verify_flags([
            ('Joku on sotamies ja palvellut jatkosodassa JvKoulK 2:ssa ja 4./JR 6:ssa. Hän haavoi7tui kaksi kertaa.', True)
        ], result_map)

    def should_return_true_if_text_contains_mentions_of_being_warhandicapped(self, result_map):
        self._verify_flags([
            ('asuvat osakehuoneistossa. Rakennusmestari Joku on 20 %:n sotainvalidi. Hänelle on myönnetty', True)
        ], result_map)

    def should_return_true_if_text_contains_mentions_of_being_warhandicapped_and_a_hyphen(self, result_map):
        self._verify_flags([
            ('asuvat osakehuoneistossa. Rakennusmestari Joku on 20 %:n sota-invalidi. Hänelle on myönnetty', True)
        ], result_map)

    def should_return_true_if_text_contains_mentions_of_being_warhandicapped_and_a_typo(self, result_map):
        self._verify_flags([
            ('Hän on sotamies ja palvellut jatkosodassa JR 6:ssa. Hän on 60 %:n sotainvalibi.', True)
        ], result_map)

    def should_return_false_if_text_does_not_mention_injury_or_being_warhandicapped(self, result_map):
        self._verify_flags([
            ('Joku Meikäläinen on kersantti ja palveli talvisodassa 1./VKK:ssa, 2./VP 19:ssä ja '
             '2./VP 1 :ssä sekä jatkosodassa 1./RaskPsto 14:s sä. Hänelle on myönnetty Vm 2, Ts '
             'mm sekä Js mm. Hän on Lauritsalan Kisan jäsen. Hän kuuluu Paperityöväenliittoon Ul'
             'koilu ja pihanhoito sekä hiihto ovat hänen mieliharrastuksiaan. Rouva Ni-me-tön ku'
             'uluu Liiketyöntekijöihin. Käsityöt ovat hänen harrastuksiaan.', False)
        ], result_map)

    def should_return_false_if_text_mentions_warhandicapped_in_wrong_context(self, result_map):
        self._verify_flags([
            ('Satunnainen heppuu asuu yhdessä äitinsä, Satunnaisen Äidin kanssa sotainvalidien talossa.', False),
            ('Hän kuuluu Karjalaseuraan, Rakennustyöväen liittoon ja Sotainvalidien Veljesliittoon.', False)
        ], result_map)

    def should_return_true_if_text_mentions_being_warhandicapped_and_primary_person_sex_is_female_and_we_are_in_spouse_extractor(self, result_map):
        self._verify_flags([
            ('asuvat osakehuoneistossa. Rakennusmestari Joku on 20 %:n sotainvalidi. Hänelle on myönnetty', True)
        ], result_map, in_spouse=True, sex='Female')

    def should_return_none_if_primary_person_sex_is_female_and_we_are_not_in_spouse_extractor(self, result_map):
        self._verify_flags([
            ('asuvat osakehuoneistossa. Rakennusmestari Joku on 20 %:n sotainvalidi. Hänelle on myönnetty', None)
        ], result_map, in_spouse=False, sex='Female')

    def should_return_none_if_primary_person_sex_is_male_and_we_are_in_spouse_extractor(self, result_map):
        self._verify_flags([
            ('asuvat osakehuoneistossa. Rakennusmestari Joku on 20 %:n sotainvalidi. Hänelle on myönnetty', None)
        ], result_map, in_spouse=True, sex='Male')

    def should_return_false_if_text_does_not_mention_being_warhandicapped_or_wounded_and_primary_person_sex_is_female_and_we_are_in_spouse_extractor(self, result_map):
        self._verify_flags([
            ('Joku Meikäläinen on kersantti ja palveli talvisodassa 1./VKK:ssa, 2./VP 19:ssä ja '
             '2./VP 1 :ssä sekä jatkosodassa 1./RaskPsto 14:s sä. Hänelle on myönnetty Vm 2, Ts '
             'mm sekä Js mm. Hän on Lauritsalan Kisan jäsen. Hän kuuluu Paperityöväenliittoon Ul'
             'koilu ja pihanhoito sekä hiihto ovat hänen mieliharrastuksiaan. Rouva Ni-me-tön ku'
             'uluu Liiketyöntekijöihin. Käsityöt ovat hänen harrastuksiaan.', False)
        ], result_map, in_spouse=True, sex='Female')


class TestServedDuringWarFlagExtraction:
    def _verify_flags(self, expected_flags_and_texts, result_map, in_spouse=False, sex='Male'):
        flag = ServedDuringWarFlagExtractor.extraction_key

        result_map.add_results('mockPrimaryPerson', {'name': {'gender': sex}})

        # Wire the dependencies and mock result map directly to the extractor
        extractor = ServedDuringWarFlagExtractor(None, {'in_spouse_extractor': in_spouse})
        extractor.set_extraction_results_map(result_map)
        extractor.set_required_dependencies(['mockPrimaryPerson'])

        for e in expected_flags_and_texts:
            shortened_text = e[0][0:15]  # Make sure the extractor uses full_text, not this substring
            results, metadata = extractor.extract({'text': shortened_text, 'full_text': e[0]}, {}, {})
            assert results[flag] is e[1]

    def should_return_true_if_text_contains_mention_of_having_served_with_lut_suffix(self, result_map):
        self._verify_flags([
            ('Herra Alikersantti on sotilasarvoltaan alikersantti ja palvellut jatkosodassa ETp/VAK:ssa '
             'sekä ErP 21:ssa.', True)
        ], result_map)

    def should_return_true_if_text_contains_mention_of_having_served_with_li_suffix(self, result_map):
        self._verify_flags([
            ('Muut asuinp.: Kuhmoinen, Orimattila, Perniö 44—, Paimio. Sota Mies palveli sotamiehen'
             'ä jatkosodassa JR 20:ssa, Vapaa-aikansa hän viettää lueskellen.', True)
        ], result_map)

    def should_return_true_if_text_contains_mention_of_having_served_with_len_suffix(self, result_map):
        self._verify_flags([
            ('Herra Testilä oli molemmissa sodissa mukana palvellen tykkimiehenä.', True)
        ], result_map)

    def should_return_true_if_text_contains_mention_of_having_served_with_substitutions_and_or_hyphen(self, result_map):
        self._verify_flags([
            ('Herra Alikersantti on sotilasarvoltaan alikersantti ja pa1-vellut jatkosodassa ETp/VAK:ssa '
             'sekä ErP 21:ssa.', True)
        ], result_map)

    def should_return_false_if_text_contains_no_mention_of_having_served(self, result_map):
        self._verify_flags([
            ('Nimettömät asuvat rakentamassaan omakotitalossa. Nyrkkeilijä Nimetön on ammattiosaston jäsen '
             'ja kuuluu nuorisojaostoon. Hän harrastaa yleisurheilua, nyrkkeilyä ja hiihtoa. Nimetön on voi'
             'ttanut seiväshypyssä piirin mestaruuksia. Hän lukee ammattikirjallisuutta. Rouva Nimetön on o'
             'piskellut työväenopistossa. Rouva harrastaa puutarhanhoitoa, käsitöitä ja kirjallisuutta. Hän'
             'on ottanut osaa kirkollisiin toimiin. Herran äiti, Äiti Nimetön o.s. Epänimetön, asuu Kaarlel'
             'assa omakotitalossa.', False)
        ], result_map)

    def should_return_false_if_text_contains_mention_of_having_served_with_luksessa_suffix(self, result_map):
        self._verify_flags([
            ('Rautateiden Partaveitsi on ollut vuodesta -48 lähtien valtion rautateiden palveluksessa.', False)
        ], result_map)

    def should_return_true_if_text_mentions_having_served_and_primary_person_sex_is_female_and_we_are_in_spouse_extractor(self, result_map):
        self._verify_flags([
            ('Herra Alikersantti on sotilasarvoltaan alikersantti ja palvellut jatkosodassa ETp/VAK:ssa '
             'sekä ErP 21:ssa.', True)
        ], result_map, in_spouse=True, sex='Female')

    def should_return_none_if_primary_person_sex_is_female_and_we_are_not_in_spouse_extractor(self, result_map):
        self._verify_flags([
            ('Herra Alikersantti on sotilasarvoltaan alikersantti ja palvellut jatkosodassa ETp/VAK:ssa '
             'sekä ErP 21:ssa.', None)
        ], result_map, in_spouse=False, sex='Female')

    def should_return_none_if_primary_person_sex_is_male_and_we_are_in_spouse_extractor(self, result_map):
        self._verify_flags([
            ('Herra Alikersantti on sotilasarvoltaan alikersantti ja palvellut jatkosodassa ETp/VAK:ssa '
             'sekä ErP 21:ssa.', None)
        ], result_map, in_spouse=True, sex='Male')

    def should_return_false_if_text_does_not_mention_having_served_and_primary_person_sex_is_female_and_we_are_in_spouse_extractor(self, result_map):
        self._verify_flags([
            ('Nimettömät asuvat rakentamassaan omakotitalossa. Nyrkkeilijä Nimetön on ammattiosaston jäsen '
             'ja kuuluu nuorisojaostoon. Hän harrastaa yleisurheilua, nyrkkeilyä ja hiihtoa. Nimetön on voi'
             'ttanut seiväshypyssä piirin mestaruuksia. Hän lukee ammattikirjallisuutta. Rouva Nimetön on o'
             'piskellut työväenopistossa. Rouva harrastaa puutarhanhoitoa, käsitöitä ja kirjallisuutta. Hän'
             'on ottanut osaa kirkollisiin toimiin. Herran äiti, Äiti Nimetön o.s. Epänimetön, asuu Kaarlel'
             'assa omakotitalossa.', False)
        ], result_map, in_spouse=True, sex='Female')


def verify_flags(expected_flags_and_texts, result_map, in_spouse=False, sex='Female', subflag='lotta'):
    flag = LottaActivityFlagExtractor.extraction_key

    result_map.add_results('mockPrimaryPerson', {'name': {'gender': sex}})

    # Wire the dependencies and mock result map directly to the extractor
    extractor = LottaActivityFlagExtractor(None, {'in_spouse_extractor': in_spouse})
    extractor.set_extraction_results_map(result_map)
    extractor.set_required_dependencies(['mockPrimaryPerson'])

    for e in expected_flags_and_texts:
        shortened_text = e[0][0:15]  # Make sure the extractor uses full_text, not this substring
        results, metadata = extractor.extract({'text': shortened_text, 'full_text': e[0]}, {}, {})
        assert results[flag][subflag] is e[1]


class TestLottaActivityFlagExtraction:

    def should_return_true_if_text_contains_mention_of_lotta_activity(self, result_map):
        verify_flags([
            ('Emäntä oli sota-aikana mukana lottatoiminnas-sa ja hän on saanut talvisodan muistomitalin.', True)
        ], result_map)

    def should_return_true_if_text_contains_mention_of_lotta_activity(self, result_map):
        verify_flags([
            ('Emäntä oli sota-aikana mukana lottatoiminnas-sa ja hän on saanut talvisodan muistomitalin.', True)
        ], result_map, in_spouse=True, sex='Male')

    def should_return_true_if_text_contains_mention_of_lotta_activity_with_typo_and_hyphen(self, result_map):
        verify_flags([
            ('Emäntä oli sota-aikana mukana l0t-tatoiminnas-sa ja hän on saanut talvisodan muistomitalin.', True)
        ], result_map)

    def should_return_false_if_text_does_not_contain_mention_of_lotta_activity(self, result_map):
        verify_flags([
            ('Emäntä oli sota-aikana tanssilattioiden partaveitsi eikä piitannut sotatoiminnasta.', False)
        ], result_map, in_spouse=False, sex='Female')

    def should_return_false_if_text_does_not_contain_mention_of_lotta_activity(self, result_map):
        verify_flags([
            ('Emäntä oli sota-aikana tanssilattioiden partaveitsi eikä piitannut sotatoiminnasta.', False)
        ], result_map, in_spouse=True, sex='Male')

    def should_return_false_if_text_contains_lotta_name(self, result_map):
        verify_flags([
            ('Emännän nimi oli Lotta ja hän', False)
        ], result_map, in_spouse=False, sex='Female')

    def should_return_false_if_text_contains_word_vuotta(self, result_map):
        verify_flags([
            ('Emäntä asui kymmenen vuotta Vitsauskylässä.', False)
        ], result_map, in_spouse=False, sex='Female')

    def should_return_false_if_text_contains_lotta_like_word_with_wrong_suffix(self, result_map):
        verify_flags([
            ('Emäntä tuli ulos omakotitalosta ja kirkui.', False),
            ('Emäntä oli luullut olevansa kiillottaja koko elämänsä ajan.', False)
        ], result_map, in_spouse=False, sex='Female')

    def should_return_none_if_primary_person_is_male_and_we_are_not_in_spouse_extractor(self, result_map):
        verify_flags([('foo', None)], result_map, in_spouse=False, sex='Male')

    def should_return_none_if_primary_person_is_female_and_we_are_in_spouse_extractor(self, result_map):
        verify_flags([('bar', None)], result_map, in_spouse=True, sex='Female')

    class TestFoodLottaFlag:
        def should_extract_foodlotta_true_if_text_contains_mention_of_lotta_working_in_a_food_role(self, result_map):
            verify_flags([
                ('Rouva toimi sota-aikana muonituslottana.', True),
                ('Sodan aikana hän oli kanttiinilottana.', True),
            ], result_map, in_spouse=False, sex='Female', subflag='foodLotta')

        def should_extract_foodlotta_true_if_text_contains_mention_of_lotta_working_in_a_food_role_with_typos(self, result_map):
            verify_flags([
                ('Rouva toimi sota-aikana muoni-tuslot-tana.', True),
                ('Sodan aikana hän oli kantt11nilottana.', True),
            ], result_map, in_spouse=False, sex='Female', subflag='foodLotta')

        def should_not_extract_foodlotta_when_there_is_no_mention_of_foodlotta_work(self, result_map):
            verify_flags([
                ('Rouva toimi sota-aikana kodinhoitajana.', False)
            ], result_map, in_spouse=False, sex='Female', subflag='foodLotta')

    class TestOfficeLottaFlag:
        def should_extract_officelotta_true_if_text_contains_mention_of_lotta_working_in_an_office_role(self, result_map):
            verify_flags([
                ('Sodan aikana hän työskenteli kenttäpostissa ja kanslialottana.', True),
                ('Talvisodan aikana hän toimi keskuslottana Vahvialasssa.', True),
                ('Hän toimi sodan aikana viestilottana.', True),
                ('Hän oli viestityslottana sotien aikana.', True),
                ('Rouva Nyymi oli jatkosodan aikana toimistolottana.', True)
            ], result_map, in_spouse=False, sex='Female', subflag='officeLotta')

        def should_extract_officelotta_true_if_text_contains_mention_of_lotta_working_in_an_office_role_with_typos(self, result_map):
            verify_flags([
                ('Sodan aikana hän työskenteli kenttäpostissa ja kanslial0ttana.', True),
                ('Talvisodan aikana hän toimi keskus-lottana Vahvialasssa.', True),
                ('Hän toimi sodan aikana vie5tilottana.', True),
                ('Hän oli viestituslottana sotien aikana.', True),
                ('Rouva Nyymi oli jatkosodan aikana toimisto!ottana.', True)
            ], result_map, in_spouse=False, sex='Female', subflag='officeLotta')

        def should_not_extract_officelotta_when_there_is_no_mention_of_officelotta_work(self, result_map):
            verify_flags([
                ('on saanut Maanviljelysseurojen keskusliiton hopeisen ansiomerkin.', False),
                ('ja palveli talvisodassa Viestijoukoissa ja', False),
                ('Satunnainen Nimi on Hausjärven puhelinlaitoksen palveluksessa', False)
            ], result_map, in_spouse=False, sex='Female', subflag='officeLotta')

    class TestNurseLottaFlag:
        def should_extract_nurselotta_true_if_text_contains_mention_of_lotta_working_in_a_health_care_role(self, result_map):
            verify_flags([
                ('Nyymi on suorittanut lääkintälottakurs-sin Helsingissä -40 ja on sen', True),
                ('Hän toimi lääkintälottana talvisodassa- ja', True)
            ], result_map, in_spouse=False, sex='Female', subflag='nurseLotta')

        def should_extract_nurselotta_true_if_text_contains_mention_of_lotta_working_in_a_health_care_role_with_typos(self, result_map):
            verify_flags([
                ('Nyymi on suorittanut lääkin-tä1-ottakurs-sin Helsingissä -40 ja on sen', True),
                ('Hän toimi lääkintäl0ttana talvisodassa- ja', True)
            ], result_map, in_spouse=False, sex='Female', subflag='nurseLotta')

        def should_not_extract_nurselotta_when_there_is_no_mention_of_nurselotta_work(self, result_map):
            verify_flags([
                ('Mystinen Voima palveli lääkintäsotamiehenä jatkosodan.', False),
                ('käynyt keskikoulun ja suorittanut lääkintävoimistelijakurssin.', False)
            ], result_map, in_spouse=False, sex='Female', subflag='nurseLotta')

    class TestAntiairLottaFlag:
        def should_extract_antiairlotta_true_if_text_contains_mention_of_lotta_working_in_air_surveillance_role(self, result_map):
            verify_flags([
                ('Rouva oli sodan aikana ilmaval-vontalottana.', True),
                ('Rouva on toiminut Iv-lottana', True)
            ], result_map, in_spouse=False, sex='Female', subflag='antiairLotta')

        def should_extract_antiairlotta_true_if_text_contains_mention_of_lotta_working_in_air_surveillance_role_with_typos(self, result_map):
            verify_flags([
                ('Rouva oli sodan aikana ilmav4l-vontalottana.', True),
                ('Rouva on toiminut Iv-lottana', True),
                ('Rouva on toiminut is-lottana', True),
                ('Rouva on toiminut Islottana', True),
                ('Rouva on toiminut It-lottana', True)
            ], result_map, in_spouse=False, sex='Female', subflag='antiairLotta')

        def should_not_extract_antiairlotta_when_there_is_no_mention_of_antiairlotta_work(self, result_map):
            verify_flags([
                ('Hän on saanut 10-vuotislottamerkin', False),
                ('palveli jatkosodassa ilmavalvontajoukoissa.', False)
            ], result_map, in_spouse=False, sex='Female', subflag='antiairLotta')

    class TestPikkulottaFlag:
        def should_extract_pikkulotta_true_if_text_contains_mention_of_person_being_a_pikkulotta(self, result_map):
            verify_flags([
                ('Nyymi kuului sodan aikana Pikkulottiin.', True),
                ('Rouva Agentti on toiminut pikkulottana.', True)
            ], result_map, in_spouse=False, sex='Female', subflag='pikkulotta')

        def should_extract_pikkulotta_true_if_text_contains_mention_of_person_being_a_pikkulotta_with_typos(self, result_map):
            verify_flags([
                ('Nyymi kuului sodan aikana Pikku1ottiin.', True),
                ('Rouva Agentti on toiminut pikkul0t-tana.', True)
            ], result_map, in_spouse=False, sex='Female', subflag='pikkulotta')

        def should_not_extract_pikkulotta_if_text_contains_no_mention_of_person_being_a_pikkulotta(self, result_map):
            verify_flags([
                ('Hän on toiminut vaatturina pikkupojasta lähtien.', False)
            ], result_map, in_spouse=False, sex='Female', subflag='pikkulotta')

    class TestOrganizationLottaFlag:
        def should_extract_organizationlotta_when_there_is_mention_of_belonging_to_lotta_org(self, result_map):
            verify_flags([
                ('Hän kuului jatkosodassa Lotta Svärd-järjestöön.', True),
                ('Hän on toiminut lottajärjestössä.', True),
                ('Hän on osallistunut nuorisoseuratyöhön, Lottayhdistyksen ja', True)
            ], result_map, in_spouse=False, sex='Female', subflag='organizationLotta')
    
        def should_not_extract_organizationlotta_when_there_is_no_mention_of_belonging_to_lotta_org(self, result_map):
            verify_flags([
                ('Hän oli talvisodassa mustekaloihin erikoistuva kokki.', False),
            ], result_map, in_spouse=False, sex='Female', subflag='organizationLotta')
    
        def should_not_extract_organizationlotta_when_there_is_mention_of_lotta_specialization_and_mention_of_lotta_org(
                self, result_map):
            verify_flags([
                ('Hän palveli muonituslottana talvisodassa ja oli Lotta Svärd-järjestön jäsen.', False),
                ('Hän oli lääkintälotta jatkosodassa ja kuului lottajärjestöön.', False)
            ], result_map, in_spouse=False, sex='Female', subflag='organizationLotta')

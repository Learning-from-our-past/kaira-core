from core.utils.text_utils import remove_hyphens_from_text
from core.utils.text_utils import remove_spaces_from_text
from core.utils.text_utils import RegexListReplacer
import regex


class TestTextUtils:
    def should_return_empty_string_after_removing_all_hyphens(self):
        text = '-~֊־᐀᠆‐‑‒–—―⁓⁻₋−⸗⸺⸻゠︲﹘﹣－'

        assert remove_hyphens_from_text(text) == ''

    def should_correctly_return_text_without_hyphens(self):
        expected_text = (
            'Throughout history, humans have been interacting with the biosphere via pulses. '
            'We are at a crossroads of sharing and yearning. Who are we? Where on the great q'
            'uest will we be reenergized? Flow is the nature of rebirth, and of us. Consciou'
            'sness is a constant. Consciousness consists of ultrasentient particles of quant'
            'um energy. “Quantum” means an invocation of the unified.'
        )

        hyphenated_text = (
            'Throug-hout history, hu⸗mans have been int－eracting with the bios⸗phere via pulses. '
            'We are at a cro~ssroads of sha⸺ring and year⸗ning. Who ar᐀e we? Whe⁻re on the great q'
            'uest wi-ll we be re-ener⸗gized? Flow is the na-ture of rebirth, and of us. Consciou'
            'sness is a constant. Cons⁻ciousness co⁻nsists of ultra-sentient par⁓ticles of quant'
            'um energy. “Quantu゠m” means an invocation of the unified⁓.'
        )

        assert remove_hyphens_from_text(hyphenated_text) == expected_text

    def should_return_empty_string_after_removing_all_spaces(self):
        text = '  ᠎           ​  　﻿'

        assert remove_spaces_from_text(text) == ''

    def should_correctly_return_text_without_spaces(self):
        expected_text = (
            'Throughouthistory,humanshavebeeninteractingwiththebiosphereviapulses.'
            'Weareatacrossroadsofsharingandyearning.Whoarewe?Whereonthegreatq'
            'uestwillwebereenergized?Flowisthenatureofrebirth,andofus.Consciou'
            'snessisaconstant.Consciousnessconsistsofultrasentientparticlesofquant'
            'umenergy.“Quantum”meansaninvocationoftheunified.'
        )

        spaced_text = (
            'Thr oug ho ut hi st　ory, h uma ns have be　en interac ting with the biosph ere via pu lses. '
            'We are a t a cro﻿ssroa ds of sharing and yea rn﻿ing. Who are we? Where on the gre at q'
            'uest will we be re energiz ed? Flo　w is the nature of rebirth, and of us. Consci ou'
            'sness is a const ant. Conscio﻿us　ness consists of ult rasentient pa rticl es of quant'
            'um en er gy. “Qua nt um” m eans an inv oc at​io n of th᠎e un​ ifi e᠎d.'
        )

        assert remove_spaces_from_text(spaced_text) == expected_text

    def should_correctly_perform_arbitrary_list_of_replacements_on_string(self):
        replacements = [
            (r'[kh](iss)[ae]', r'kissa', (regex.IGNORECASE | regex.UNICODE)),
            (r'\b(?:lääkintäluutnantti){s<=2}\b', r'lääkintäluutnantti', None),
            (r'(?:(\d),(\d))', r'\1.\2', None),
        ]
        r = RegexListReplacer(replacements)

        input_text = (
            'Testinen oli 1ääkintäluutnentti sodassa. Vapaa-ajallaan hän '
            'on hyödyntänyt taitojaan pelastamalla hissan, jonka pH-arvo '
            'oli 11,5. Tämän jälkeen kisse oli melko tyytyväinen.'
        )
        expected_text = (
            'Testinen oli lääkintäluutnantti sodassa. Vapaa-ajallaan hän '
            'on hyödyntänyt taitojaan pelastamalla kissan, jonka pH-arvo '
            'oli 11.5. Tämän jälkeen kissa oli melko tyytyväinen.'
        )

        assert r.run_replacements(input_text) == expected_text

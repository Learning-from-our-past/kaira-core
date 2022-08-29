import regex
from core.utils.text_utils import hyphen_regex_pattern
from core.utils.text_utils import RegexListReplacer

"""
This file contains all the patterns that are used to clean up the Siirtokarja-
laisten tie person entry texts. The NLP parser is sensitive to mistakes, and
even simple mistakes in the text entries can change how the NLP parser
interprets the entire phrase that contains those mistakes.

Note that when adding new patterns, the order of these patterns matters! If you
are writing new patterns based file output by text preprocessing, then you will
want to add your patterns to the end of the list. If you are writing new
patterns based on the raw person entry texts, then you will want to place your
patterns at the beginning of the list. This may, however, impact how the patterns
which come after the new pattern function.
"""


clean_up_patterns = [
    # Change variants of "o.s." to "omaa sukuaan"
    (r'^(?:o[.,]?s[,.]?)(?=\s)', r'omaa sukuaan', regex.IGNORECASE),
    (r'(?<=[\s\n,.])(?:o[.,]?s[,.]?)(?=\s)', r'omaa sukuaan', regex.IGNORECASE),
    (r'(?:o[.,]s[.,])', r'omaa sukuaan', regex.IGNORECASE),
    # Change "n." to "noin"
    (r'(?:\sn\.\s)', r' noin ', None),
    # Change variants of "muut asuinp." to "muut asuinpaikat:"
    (
        r'(m)(?:uut){s<=1}\s?(?:asuinp){s<=1}[.,\s]?',
        r'\1uut asuinpaikat',
        regex.IGNORECASE,
    ),
    (r'(?:(m)uut\s?[B-Öb-ö]{0,3}sui.{0,3}:)', r'\1uut asuinpaikat:', regex.IGNORECASE),
    # Change just "asuinp." to "asuinpaikat"
    (r'(a)(?:suinp)[.,;]?(?!aikat)', r'\1suinpaikat', regex.IGNORECASE),
    # Change "puol." to "puoliso"
    (
        r'(?<![a-zöä])\s?(p)(?:uol)\s*[.,;]?\s*(?=[^a-zöä])',
        r' \1uoliso',
        regex.IGNORECASE,
    ),
    (r'(?<![a-zöä])(?:(p)uol){s<=1}[^a-zöä]', r'\1uoliso', regex.IGNORECASE),
    # Change "synt." to "syntyi"
    (r'\s?(?:synt\.){s<=1}\s?', r' syntyi ', None),
    # Fix floats to use dot instead of comma (NLP parser requires this)
    (r'(?:(\d),(\d))', r'\1.\2', None),
    # Fix incorrect variants of the ":ssa" and ":ssä" suffices
    (r'\s*(ss[aä])', r'\1', None),
    (r'\s+[;!*.\'’,/\-:](ss[aä])', r':\1', None),
    (r'[;!*.\'’,/\-](ss[aä]){i<=1}', r':\1', None),
    # Fix incorrect variants of the ":n" suffix
    (r'[;!*.\'’,/\-](n)(?=[\s|\.])', r':\1', None),
    # Change "v." to "vuonna"
    (r'\s(v)\.\s', r' \1uonna ', regex.IGNORECASE),
    # Change "k." to "kuoli"
    (r'\s(k)\.\s', r' kuoli ', None),
    # Change "s." to "syntyi"
    (r'\s(s)\.\s', r' syntyi ', None),
    # Expand "mlk:ssa"/"mlk:sso" to "maalaiskunnassa"
    (r'mlk[.,;:]ss[ao]', r'maalaiskunnassa', None),
    # Expand "mlk." to "maalaiskunta"
    (r'mlk\.', r'maalaiskunta', None),
    # Change "avioit." to "avioitunut"
    (r'(avioit)(?:[,.\-*:!;]?)?', r'\1unut', regex.IGNORECASE),
    # Replace special hyphen looking characters with a regular hyphen
    (hyphen_regex_pattern, r'-', None),
    # Change "v:sta" to "vuodesta"
    (r'(?:(v)[.:;\-*!,/\'’]st(?:a))', r'\1uodesta', regex.IGNORECASE),
    # Fix mentions of medals to have a space inbetween if they don't
    (r'(js|ts|vs)(mm[,.\s\-*/!;:])', r'\1 \2', regex.IGNORECASE),
    # Fix incorrect ";" characters to ":"
    (
        r'(karjalassa|lapset|tytär|vaimo|poika|asuinpaikat|reitti|avioliitosta'
        r'|isä|äiti|lapsensa|vanhemmat|sisarukset|kunniamerkit){s<=1};',
        r'\1:',
        regex.IGNORECASE,
    ),
    # Trim whitespace between "asuinpaikat" and ":"
    (r'(asuinpaikat)\s+:', r'\1:', regex.IGNORECASE),
    # Expand variants of "ent" to "entinen"
    (r'(?:ent[,.])', r'entinen', None),
    (r'(?<![a-öA-Ö])ent(?=\s)', r'entinen', None),
    # Fix some mentions of "muut asuinpaikat"
    (r'(?:(m)uut.{1,2}:)', r'\1uut asuinpaikat:', regex.IGNORECASE),
]


def get_siirtokarjalaisten_tie_cleaner():
    return RegexListReplacer(clean_up_patterns)

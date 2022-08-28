from pyparsing import Word, alphas, Literal, nums, Or, Optional, Group, ZeroOrMore

"""
 Pyparsing BNF definition for parsing strings of migration data.
 Parses string producing data structure containing places,
 municipalities and migration years of the Person.
"""
# Useful generic tokens
scandinavian_letters = 'ÄÖÅäöå-'
hyphens = '—--'
punctuation = Optional(Word(',.').suppress())

# Grammar for extracting years and year ranges in form of <-39>,
# <39-49>, <-39, 43-45> etc.
# <39> without hyphen in either side is interpreted as moved_out
_year = Or(
    [
        (Word(hyphens).suppress() + Word(nums).setResultsName('moved_out')),
        Word(nums).setResultsName('moved_in') + Word(hyphens).suppress(),
        Word(nums).setResultsName('moved_out'),
    ]
)
_year_range = Group(_year + Optional(_year) + punctuation)
_year_information = Optional(_year_range + Optional(_year_range))

# Rules for single place name and year data associated to it
_place_name = (
    Word(alphas + scandinavian_letters) + Optional(Literal('mlk'))
).setResultsName('place')
_place_with_year_data = (
    _place_name('place') + punctuation + _year_information('year_information')
)
_place_with_municipality = Optional(_place_name('municipality') + punctuation)
_place_or_place_with_year_data = (
    Or([_place_name('place'), _place_with_year_data]) + punctuation
)

# Rule for getting place and municipality name if one is set for location
_place_or_place_and_municipality = Or(
    [
        _place_or_place_with_year_data,
        _place_with_municipality + _place_or_place_with_year_data,
    ]
)

# Rule for extracting locations and migration years from string of migration locations
locations_extraction_grammar = ZeroOrMore(Group(_place_or_place_and_municipality))


def parse_locations(text):
    result = locations_extraction_grammar.parseString(text)

    # Concatenate municipality and place names in case they are
    # multipart eg. 'Viipurin mlk'
    for x in result:
        x['place'] = ' '.join(x['place'])
        if 'municipality' in x:
            x['municipality'] = ' '.join(x['municipality'])

    return result

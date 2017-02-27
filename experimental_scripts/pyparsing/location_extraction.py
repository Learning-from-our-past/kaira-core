from pyparsing import Word, alphas, Literal, Empty, nums, Or, Optional, Group, ZeroOrMore, Dict

s1 = "Viipurin mlk. -27, Pohjois-Karjala 31—32, Viipuri 32—. "
s2 = "Laasola -39. 42—44"
s3 = "Laasola -39. 42—"
s4 = "Laasola -39. —44"
s5 = "Laasola."
s6 = "Laasola -39."
s7 = "Laasola 29-39. 42—44"
s8 = "Kuolemajärvi. Laasola -39. 42—44"
s9 = "Suistamo, Kontuvaara -39, 42—44"
s10 = "Pohjoislnkeri. Miikkulainen -19. Metsäpirtti. Tappari19—21. Pyhäjärvi, Saapru 21—24. Sortavala24-28. Terijoki 28-31. Uusikirkko 31-39, 42-44"
s11 = "Kuolemajärvi Laasola -39. 42—44"
s12 = "Hiitola 40, 42—44"
s13 = "Kaukola, Kortteensalmi -39, Sortavalanmlk"

s14 = "Hiitola. Kuoksjärvi -39, 42—44."
s15 = "' Kurkijoki -40. 41-44."
s16 = "Kaukola, Liinamaa -39. 42^44."
s17 = "    Uusikirkko, Uiskola -39."
s18 = 'Kaukola, Kortteensalmi -39, Sortavalanmlk'
s19 = "Laasola 39."

# Useful generic tokens
scandinavian_letters = 'ÄÖÅäöå-'
hyphens = '—--'
punctuation = Optional(Word(',.').suppress())

# Grammar for extracting years and year ranges in form of <-39>, <39-49>, <-39, 43-45> etc.
year = Or([(Word(hyphens).suppress() + Word(nums).setResultsName('moved_out')), Word(nums).setResultsName('moved_in') + Word(hyphens).suppress(), Word(nums).setResultsName('moved_out')])
year_range = Group(year + Optional(year) + punctuation)
year_information = Optional(year_range + Optional(year_range))

# Rules for single place name and year data associated to it
place_name = (Word(alphas + scandinavian_letters) + Optional(Literal('mlk'))).setResultsName('place')
place_with_year_data = place_name('place') + punctuation + year_information('year_information')
place_with_municipality = Optional(place_name('municipality') + punctuation)
place_or_place_with_year_data = Or([place_name('place'), place_with_year_data]) + punctuation

# Rule for getting place and municipality name if one is set for location
place_or_place_and_municipality = Or([place_or_place_with_year_data, place_with_municipality + place_or_place_with_year_data])

# Rule for extracting locations and migration years from string of migration locations
locations_extraction_grammar = ZeroOrMore(Group(place_or_place_and_municipality))

result = locations_extraction_grammar.parseString(s2)
for x in result:
    x['place'] = ' '.join(x['place'])
    if 'municipality' in x:
        x['municipality'] = ' '.join(x['municipality'])

print(result.dump())
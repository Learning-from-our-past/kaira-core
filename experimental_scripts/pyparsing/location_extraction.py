from pyparsing import Word, alphas, Literal, Empty, nums, Or, Optional, Group, ZeroOrMore

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

additions = 'ÄÖÅäöå-'

hyphens = '—--'

place = (Word(alphas+additions) + Optional(Literal('mlk'))).setResultsName('place')

year = Or([(Word(hyphens).suppress() + Word(nums).setResultsName('moved_out')), Word(nums).setResultsName('moved_in')])

year_pair = Group(year + Optional(year) + Optional(Word('.,')).suppress())

year_information = Optional(year_pair + Optional(year_pair))

place_with_year_data = place('place') + Optional(Word('.,')).suppress() + year_information('year_information')

location = Or([place('place'), place_with_year_data]) + Optional(Word(',.').suppress())

place_with_municipality = Optional(place('municipality') + Optional(Word('.,')).suppress())

location_pattern = ZeroOrMore(Group(Or([location, place_with_municipality + location])))

result = location_pattern.parseString(s2)
print(result.dump())
CHILDREN_TEXTS = {
    'common_birth_place': 'o.s. Testinen, rouva, synt. 19. 7. -16 Hiitolassa. Puol. Mies Miehekäs, ahtaaja, synt. 12. 2.'
    '    17Ahlaisissa. Avioit. -44. Lapset: Irja Hellevi -45, Kirsti Anna-Liisa -47, Kalervo Viljam -53. '
    'Syntyneet Ahlaisissa. Asuinp. Karjalassa: Hiitola. Päijälä 40. 43—44.',
    'different_birth_places': 'o.s. Testinen, rouva, synt. 19. 7. -16 Hiitolassa. Puol. Mies Miehekäs, ahtaaja, synt. 12. 2.'
    '    17Ahlaisissa. Avioit. -44. Lapset: Irja Hellevi -45 Testikylä, Kirsti Anna-Liisa -47 Hiitola.'
    'Asuinp. Karjalassa: Hiitola. Päijälä 40. 43—44.',
}

EXPECTED = {
    'common_birth_place': [
        {
            'birthYear': 1945,
            'gender': 'Female',
            'location': {'locationName': 'Ahlainen', 'region': 'other'},
            'name': 'Irja Hellevi',
            'kairaId': 'testbook_1_1C_1',
        },
        {
            'birthYear': 1947,
            'gender': 'Female',
            'location': {'locationName': 'Ahlainen', 'region': 'other'},
            'name': 'Kirsti Anna-Liisa',
            'kairaId': 'testbook_1_1C_2',
        },
        {
            'birthYear': 1953,
            'gender': 'Male',
            'location': {'locationName': 'Ahlainen', 'region': 'other'},
            'name': 'Kalervo Viljam',
            'kairaId': 'testbook_1_1C_3',
        },
    ],
    'different_birth_places': [
        {
            'birthYear': 1945,
            'gender': 'Female',
            'location': {
                'locationName': 'Testikylä',  # This place is not in geodb, so we get only the name without region data
                'region': None,
            },
            'name': 'Irja Hellevi',
            'kairaId': 'testbook_1_1C_1',
        },
        {
            'birthYear': 1947,
            'gender': 'Female',
            'location': {'locationName': 'Hiitola', 'region': 'karelia'},
            'name': 'Kirsti Anna-Liisa',
            'kairaId': 'testbook_1_1C_2',
        },
    ],
}

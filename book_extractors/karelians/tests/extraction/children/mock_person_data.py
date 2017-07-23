CHILDREN_TEXTS = [
    "o.s. Testinen, rouva, synt. 19. 7. -16 Hiitolassa. Puol. Mies Miehekäs, ahtaaja, synt. 12. 2."
    "    17Ahlaisissa. Avioit. -44. Lapset: Irja Hellevi -45, Kirsti Anna-Liisa -47, Kalervo Viljam -53. "
    "Syntyneet Ahlaisissa. Asuinp. Karjalassa: Hiitola. Päijälä 40. 43—44."
]

EXPECTED = [
    {
        'birthYear': 1945,
        'gender': 'Female',
        'location': {
            'locationName': 'Ahlainen',
            'region': 'other'
        },
        'name': 'Irja Hellevi',
        'kairaId': 'testbook_1_1C'
    },
    {
        'birthYear': 1947,
        'gender': 'Female',
        'location': {
            'locationName': 'Ahlainen',
            'region': 'other'
        },
        'name': 'Kirsti Anna-Liisa',
        'kairaId': 'testbook_1_2C'
    },
    {
        'birthYear': 1953,
        'gender': 'Male',
        'location': {
            'locationName': 'Ahlainen',
            'region': 'other'
        },
        'name': 'Kalervo Viljam',
        'kairaId': 'testbook_1_3C'
    }
]
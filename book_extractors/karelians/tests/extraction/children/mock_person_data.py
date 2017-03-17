CHILDREN_TEXTS = [
    "o.s. Testinen, rouva, synt. 19. 7. -16 Hiitolassa. Puol. Mies Miehekäs, ahtaaja, synt. 12. 2."
    "    17Ahlaisissa. Avioit. -44. Lapset: Irja Hellevi -45, Kirsti Anna-Liisa -47, Kalervo Viljam -53. "
    "Syntyneet Ahlaisissa. Asuinp. Karjalassa: Hiitola. Päijälä 40. 43—44."
]

EXPECTED = [
    {
        'birthYear': 1945,
        'gender': 'Female',
        'location': 'Ahlaisissa',
        'name': 'Irja Hellevi',
        'coordinates': {
            'latitude': None,
            'longitude': None
        }
    },
    {
        'birthYear': 1947,
        'gender': 'Female',
        'location': 'Ahlaisissa',
        'name': 'Kirsti Anna-Liisa',
        'coordinates': {
            'latitude': None,
            'longitude': None
        }
    },
    {
        'birthYear': 1953,
        'gender': 'Male',
        'location': 'Ahlaisissa',
        'name': 'Kalervo Viljam',
        'coordinates': {
            'latitude': None,
            'longitude': None
        }
    }
]
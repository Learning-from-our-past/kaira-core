HOSTESS_TEXTS = {
    'normal': ", om. vuodesta 1967 Testi Mies Testikäs, synt. 29. 4. 1932 ja emäntä Maija Lahja Annikki o.s. Testinen, "
    "synt. 21. 8. 1945. Poika: Lapsi Lapsekas Lapsinen -66. Edellinen omistaja oli August Edellinen vuosina 1921—46. "
    "Tilan kok.pinta-ala on",
    'no_hostess': ", om. vuodesta 1945 Mies Miehekäs, synt.7. 3. 1891. "
    "Edellinen omistaja oli Kalle Ikonen. Tilan kok.pin",
}

EXPECTED = [
    {
        'firstNames': 'Maija Lahja Annikki',
        'gender': 'Female',
        'surname': 'Testinen',
        'birthData': {'birthDay': 21, 'birthMonth': 8, 'birthYear': 1945},
    },
    None,
]

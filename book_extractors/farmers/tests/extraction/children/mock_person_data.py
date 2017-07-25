CHILDREN_TEXTS = [
    ", om. vuodesta 1965 Testi Henkilon perikunta. Emännyyttä on vuodesta 1946 lähtien hoitanut ELina Suvi Testinen o.s."
    " Testikäs, synt. 10. 4. 1911. Lapset: Maija Sanelma -37, Raimo Juhani -39 ja Pentti Kaarlo Kalevi -42. Tilalla asuvat "
    "myös Testimiehen vaimo, Testivaimo o.s. Tetaileva ja heidän lapsensa Jouni -64 sekä Jaana -66 ja Testikäsmiehen vaimo Testailevavaimo o.s. Testeri. "
    "Edellinen omistaja oli Testi Henkilo vuosina 1946—65."
]

TWINS_AND_EXTRA_INFO_CHILDREN = ", om. vuodesta 1963 Lapsi ja Testi Testikäs. Isännyyttä on vuodesta 1928 lähtien hoitanut Lapsi Testikäs, " \
        "synt. 14. 1. 1897 ja emäntä Nainen Naisekas o.s. Testinen, synt. 31. 7. 1896. Lapset:Ester -15, Jenny -24, kaksoset Edith ja Toivo -27, " \
        "joka on tilan toinen omistaja, Hilma -28, Sirkka -29, Tyyne -32, Heikki -33, joka on tilan toinen omistaja sekä Martta -36. " \
        "Edelliset omistajat olivat Edellinen ja Edellinenvaimo Testikäs vuosina 1928—63."
EXPECTED_CHILDREN = [
    {
        "birthYear": 1937,
        "gender": "Female",
        "name": "Maija Sanelma",
        "kairaId": 'testbook_1_1C'
    },
    {
        "birthYear": 1939,
        "gender": "Male",
        "name": "Raimo Juhani",
        "kairaId": 'testbook_1_2C'
    },
    {
        "birthYear": 1942,
        "gender": "Male",
        "name": "Pentti Kaarlo Kalevi",
        "kairaId": 'testbook_1_3C'
    }
]
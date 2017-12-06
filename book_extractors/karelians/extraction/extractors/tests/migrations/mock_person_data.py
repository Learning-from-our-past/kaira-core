LOCATION_TEXTS = [
    'Asuinp. Karjalassa: Kuolemajärvi. Laasola -39. 42—44. '
    'Muut asuinp.: Urjala 39-40. Urjala. Honkola 40-42, Sauvo. Timperlä -44. Piikkiö. '
    'Viuhkalo 44—47. Paattinen, Auvaismäki 47-48. Paattinen, Kreivi-lä 48-, Rouvan evakkomatka: Koivisto. '
    'Humaljoki -39, Paattinen. Kreivilä 58— Rusit ovat saaneet maanhankintalain kautta tilansa v. -47. ',

    'Asuinp. Karjalassa: Kuolemajärvi, Laasola -39. 42-44. Muut asuinp.: '
    'Karkku 39-40. Urjala. Kehro 40—, Isokyrö 40—41. Honkajoki kk. 41—42. Sauvo 44—46. Päällinen 46—. Rusit asuvat '
    'maatilallaan',

    'Asuinp. Karjalassa: Viipurin mlk. -27, Pohjois-Karjala 31—32, Viipuri 32—. '
    'Muut asuinp.: Lohja, Mustiala, Paimio Harkian perhe asuu omakotitalossaan.',

    'Asuinp. Karjalassa: Kaukola, Kortteensalmi -39, Sortavalan mlk. '
    'Muut asuinp.: Vihti 39—41, Kajaani, Helsinki, Paimio. Perniö, Paimio. Huuhkat asuvat',

    'Asuinp. Karjalassa: Vuoksenranta, Oravankytö 23—39,    41—44.'
    'Muut asuinp.: Lottana -44, Kurikka 39—41, Ähtäri, Niemisvesi 44—. Viitaset asuvat',

    'autonkuljettaja, synt. 1. 12. -33 Valkjärvellä. Puol. Testi Testinen o.s. Testaaja, rouva, synt. 24. 6. -32 Kempeleellä. Lapset: Lapsi -54 Längelmäki, Lapsekas -57 Längelmäki, Lapsellinen -61 Längelmäki. Asuinp. Karjalassa: Valkjärvi, Marjaniemi -39,42—44. Muut asuinp.. Ypäjä 39—42, Kuhmoinen, Längelmäki, Hiukkaa, Längelmäki. Länkipohja. Aikaisemmin Karjalaisilla oli maatila, mutta vanhaemännän kuoltua se myytiin ja lapset muuttivat muualle. Herra Karjalainen on ollut vuodesta -59 Längelmäen Osuuskaupan palveluksessa. Ensi Karjalaisen isä. Antti, synt. -97 Valkjärvellä, kuoli Kangasalalla v. -66. Äiti. Hilda o.s. Paavilainen, synt. 1900, kuöli -53 Längelmäellä.'
]

# Texts where rouva words was included as place name
LOCATION_TEXTS_WITH_ROUVA_WORD = [
    {'text': 'Avioit. -32. Asuinp. Karjalassa: Vahviala. Viipuri 24—39. Muut asuinp.. Orivesi39-40. Lahti 40—. Rouva muutti v. -27 Sortavalasta Viipuriin, josta edelleen Orivedelle v. -39.',
     'expected': [
        {
            'movedOut': 39,
            'movedIn': 24,
            'region': 'karelia',
            'locationName': 'Vahviala'
        }, {
            'movedOut': 40,
            'movedIn': 39,
            'region': 'other',
            'locationName': 'Orivesi'
        }, {
            'movedOut': None,
            'movedIn': 40,
            'region': 'other',
            'locationName': 'Lahti'
        }
     ]},

    # Here Rouva is extracted as last one. Otherwise ok.
    {'text': 'ottolapsi. Asuinp. Karjalassa: Räisäiä, Tuulaskoski -39. 41—44. Muut asuinp.: Ilmajoki 39—, Kauhajoki 44-. Kokemäki 48—, Pirkkala 59—, Simo 52—, Pori 61—, Rouva Testaaja toimi lottana vv. 41—44. Hän kuuluu invalidiyhdistykseen',
     'expected': [
         {
             'locationName': 'Räisäiä',
             'movedIn': None,
             'movedOut': 39,
             'region': 'karelia'
         }, {
             'locationName': 'Räisäiä',
             'movedIn': 41,
             'movedOut': 44,
             'region': 'karelia'
         }, {
             'locationName': 'Ilmajoki',
             'movedIn': 39,
             'movedOut': None,
             'region': 'other'
         }, {
             'locationName': 'Kauhajoki',
             'movedIn': 44,
             'movedOut': None,
             'region': 'other'
         }, {
             'locationName': 'Kokemäki',
             'movedIn': 48,
             'movedOut': None,
             'region': 'other'
         }, {
             'locationName': 'Pirkkala',
             'movedIn': 59,
             'movedOut': None,
             'region': 'other'
         }, {
             'locationName': 'Simo',
             'movedIn': 52,
             'movedOut': None,
             'region': 'other'
         }, {
             'locationName': 'Pori',
             'movedIn': 61,
             'movedOut': None,
             'region': 'other'
         }
     ]},
    # Here extraction doesn't stop correctly to last entry but instead includes Rouva and all other stuff after it.
    {'text': 'Asuinp. Karjalassa: Käkisalmi -39. Muut asuinp.: Vaasa 44—46, Turku 46—. Rouva Testaaja lähti Viipurista v. -39 Kurikka -39 Turku -41 Viipuri 41—44 Turku 44—, Testaajat rakennuttivat vv. 53—55 omakotitalon.',
     'expected': [
        {
            'locationName': 'Käkisalmi',
            'movedIn': None,
            'movedOut': 39,
            'region': 'karelia'
        }, {
            'locationName': 'Vaasa',
            'movedIn': 44,
            'movedOut': 46,
            'region': 'other'
        }, {
            'locationName': 'Turku',
            'movedIn': 46,
            'movedOut': None,
            'region': 'other'
        }
     ]},
    # Here extraction doesn't stop correctly and instead includes persons name Saima interpreted as Saimaa and then later word Rouva.
    {'text': 'Asuinp. Karjalassa: Uusikirkko 1900-23, Heinjoki 25-39. 43-44. Muut asuinp.: Helsinki 23—24, Kouvola 24—25, Perniö 39—40, Miehikkälä 40—43. Koski Tl. 44— 45, Miehikkälä 45—47, Virolahti 47—. Saima Testaaja asuu yhdessä poikansa kanssa. Rouva Testaaja on käynyt kätilöopiston Helsingissä v.23—24 ja toiminut sen jälkeen ammatissaan.',
        'expected': [{
             'locationName': 'Uusikirkko',
             'movedIn': 1900,
             'movedOut': 23,
             'region': 'karelia'
         }, {
             'locationName': 'Heinjoki',
             'movedIn': 25,
             'movedOut': 39,
             'region': 'karelia'
         }, {
             'locationName': 'Heinjoki',
             'movedIn': 43,
             'movedOut': 44,
             'region': 'karelia'
         }, {
             'locationName': 'Helsinki',
             'movedIn': 23,
             'movedOut': 24,
             'region': 'other'
         }, {
             'locationName': 'Kouvola',
             'movedIn': 24,
             'movedOut': 25,
             'region': 'other'
         }, {
             'locationName': 'Perniö',
             'movedIn': 39,
             'movedOut': 40,
             'region': 'other'
         }, {
             'locationName': 'Miehikkälä',
             'movedIn': 40,
             'movedOut': 43,
             'region': 'other'
         }, {
             'locationName': 'Koski',
             'movedIn': 44,
             'movedOut': 45,
             'region': 'other'
         }, {
             'locationName': 'Miehikkälä',
             'movedIn': 45,
             'movedOut': 47,
             'region': 'other'
         }, {
             'locationName': 'Virolahti',
             'movedIn': 47,
             'movedOut': None,
             'region': 'other'
         }
        ]
    }
]

LOCATION_TEXTS_WITH_INCORRECT_REGION = [
    {'text': 'Poika -53 Helsinki. Asuinp. Karjalassa: Uusi kirkko. Lempiälä 12—28, Helsinki 28—. Muut asuinp.: Helsinki mlk. Testiset asuvat',
     'expected': [
        {
            'movedOut': 28,
            'village': {
              'locationName': 'Lempiälä'
            },
            'movedIn': 12,
            'region': 'karelia',
            'locationName': 'Uusikirkko'
        }, {
            'movedOut': None,
            'village': None,
            'movedIn': 28,
            'region': 'other',
            'locationName': 'Helsinki'
        }]
     },
    {'text': 'Poika -53 Helsinki. Asuinp. Karjalassa: Uusi kirkko. Lempiälä 12—28. Muut asuinp.: Kanneljärvi 28—. Testiset asuvat',
     'expected': [
        {
            'movedOut': 28,
            'village': {
              'locationName': 'Lempiälä'
            },
            'movedIn': 12,
            'region': 'karelia',
            'locationName': 'Uusikirkko'
        }, {
            'movedOut': None,
            'village': None,
            'movedIn': 28,
            'region': 'karelia',
            'locationName': 'Kanneljärvi'
        }]
     }
]

LOCATION_HEURISTICS = {
    'long_name_with_mlk': {
            'text': 'Asuinp. Karjalassa; Kristiinankaupungin mlk 23—39. Muut asuinp.: Kankaanpää 39— 40, '
                    'Hirvensalo -40, Perniö -40, Ähtäri, Hankavesi 41—44, Kristiinankaupungin mlk 45-. Aholat asuvat itse rakentamassaan omakotitalossa. '
                    'Herra Ahola on sotamies. Hän on saanut kunniamerkit Ts mm, Js mm, SVR m 1 ja SVR m 2. Kalastus ja puutarhanhoito '
                    'miellyttävät häntä. Hän on ollut asevarikkotehtävissä v.30—68.',
    },
    'short_white_listed_name': {
            'text': 'Asuinp. Karjalassa; Eno 23—39. Muut asuinp.: Kankaanpää 39— 40, '
                    'Hirvensalo -40, Perniö -40, Ähtäri, Hankavesi 41—44, Utö 45-. Aholat asuvat itse rakentamassaan omakotitalossa. '
                    'Herra Ahola on sotamies. Hän on saanut kunniamerkit Ts mm, Js mm, SVR m 1 ja SVR m 2. Kalastus ja puutarhanhoito '
                    'miellyttävät häntä. Hän on ollut asevarikkotehtävissä v.30—68.',
    },

    'short_white_listed_alias_name': {
            'text': 'Asuinp. Karjalassa; Ii 23—39. Muut asuinp.: Kankaanpää 39— 40, '
                    'Hirvensalo -40, Perniö -40, Ähtäri, Hankavesi 41—44, li 45-. Aholat asuvat itse rakentamassaan omakotitalossa. '
                    'Herra Ahola on sotamies. Hän on saanut kunniamerkit Ts mm, Js mm, SVR m 1 ja SVR m 2. Kalastus ja puutarhanhoito '
                    'miellyttävät häntä. Hän on ollut asevarikkotehtävissä v.30—68.',
    },

    'name_with_extra_hyphens': {
            'text': 'Asuinp. Karjalassa; -Viipuri 23—39. Muut asuinp.: Kankaanpää 39— 40, '
                    'Hirvensalo -40, Perniö -40, -Ähtäri, Hankavesi 41—44, Kristiinankaupungin mlk 45-. Aholat asuvat itse rakentamassaan omakotitalossa. '
                    'Herra Ahola on sotamies. Hän on saanut kunniamerkit Ts mm, Js mm, SVR m 1 ja SVR m 2. Kalastus ja puutarhanhoito '
                    'miellyttävät häntä. Hän on ollut asevarikkotehtävissä v.30—68.',
    },


    'short_place_name': {
        'text': 'Asuinp. Karjalassa; Viipuri 23—39, ktr. Muut asuinp.: Kankaanpää, ja 39— 40, '
                'Hirvensalo -40, Perniö -40, Ähtäri, Hankavesi 41—, ktr. Aholat asuvat itse rakentamassaan omakotitalossa. '
                'Herra Ahola on sotamies. Hän on saanut kunniamerkit Ts mm, Js mm, SVR m 1 ja SVR m 2. Kalastus ja puutarhanhoito '
                'miellyttävät häntä. Hän on ollut asevarikkotehtävissä v.30—68.',
        'expected': [
          {
            'movedOut': 40,
            'village': None,
            'movedIn': 39,
            'region': 'other',
            'locationName': 'Kankaanpää'
          },
          {
            'movedOut': 40,
            'village': None,
            'movedIn': None,
            'region': 'other',
            'locationName': 'Hirvensalo'
          },
          {
            'movedOut': 40,
            'village': None,
            'movedIn': None,
            'region': 'other',
            'locationName': 'Perniö'
          },
          {
            'movedOut': None,
            'village': {
              'locationName': 'Hankavesi'
            },
            'movedIn': 41,
            'region': 'other',
            'locationName': 'Ähtäri'
          }
        ]
    },
    'long_place_name': {
        'text': 'Asuinp. Karjalassa; Viipuri 23—39, Thisisnotarealplacebutsomenonsensewhichshouldnotbeconsideredasplace. Muut asuinp.: Kankaanpää, Lauhalan koulu 39— 40, '
                'Hirvensalo -40, Perniö -40, Ähtäri, Hankavesi 41—. Aholat asuvat itse rakentamassaan omakotitalossa. '
                'Herra Ahola on sotamies. Hän on saanut kunniamerkit Ts mm, Js mm, SVR m 1 ja SVR m 2. Kalastus ja puutarhanhoito '
                'miellyttävät häntä. Hän on ollut asevarikkotehtävissä v.30—68.',
        'expected': [
            {
                'region': 'other',
                'locationName': 'Kankaanpää',
                'movedIn': 39,
                'village': {
                  'locationName': 'Lauhalankoulu'
                },
                'movedOut': 40
            },
            {
                'region': 'other',
                'locationName': 'Hirvensalo',
                'movedIn': None,
                'village': None,
                'movedOut': 40
           },
           {
                'region': 'other',
                'locationName': 'Perniö',
                'movedIn': None,
                'village': None,
                'movedOut': 40
           },
           {
                'region': 'other',
                'locationName': 'Ähtäri',
                'movedIn': 41,
                'village': {
                  'locationName': 'Hankavesi'
                },
                'movedOut': None
           }
        ]
    }

}

# Expected location results for texts
EXPECTED_RESULTS = [
    {
        'finnish_locations': [{
            'movedIn': 39,
            'region': 'other',
            'movedOut': 40,
            'locationName': 'Urjala',
            'village': None
          }, {
            'movedIn': 40,
            'region': 'other',
            'movedOut': 42,
            'locationName': 'Urjala',
            'village': {
              'locationName': 'Honkola'
            }
          }, {
            'movedIn': None,
            'region': 'other',
            'movedOut': 44,
            'locationName': 'Sauvo',
            'village': {
              'locationName': 'Timperlä'
            }
          }, {
            'movedIn': 44,
            'region': 'other',
            'movedOut': None,
            'locationName': 'Piikkiö',
            'village': {
              'locationName': 'Viuhkalo'
            }
          }
        ]
    },
    {
        'finnish_locations': [{
            'movedIn': 39,
            'region': 'other',
            'movedOut': 42,
            'locationName': 'Ypäjä',
            'village': None
          }, {
            'movedIn': None,
            'region': 'other',
            'movedOut': None,
            'locationName': 'Kuhmoinen',
            'village': None
          }, {
            'movedIn': None,
            'region': 'other',
            'movedOut': None,
            'locationName': 'Längelmäki',
            'village': None
          }, {
            'movedIn': None,
            'region': 'other',
            'movedOut': None,
            'locationName': 'Hiukkaa',
            'village': None
          }, {
            'movedIn': None,
            'region': 'other',
            'movedOut': None,
            'locationName': 'Längelmäki',
            'village': None
          }, {
            'movedIn': None,
            'region': 'other',
            'movedOut': None,
            'locationName': 'Länkipohja',
            'village': None
          }
        ]
    }
]

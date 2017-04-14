LOCATION_TEXTS = [
    "Asuinp. Karjalassa: Kuolemajärvi. Laasola -39. 42—44. "
    "Muut asuinp.: Urjala 39-40. Urjala. Honkola 40-42, Sauvo. Timperlä -44. Piikkiö. "
    "Viuhkalo 44—47. Paattinen, Auvaismäki 47-48. Paattinen, Kreivi-lä 48-, Rouvan evakkomatka: Koivisto. "
    "Humaljoki -39, Paattinen. Kreivilä 58— Rusit ovat saaneet maanhankintalain kautta tilansa v. -47. ",

    "Asuinp. Karjalassa: Kuolemajärvi, Laasola -39. 42-44. Muut asuinp.: "
    "Karkku 39-40. Urjala. Kehro 40—, Isokyrö 40—41. Honkajoki kk. 41—42. Sauvo 44—46. Päällinen 46—. Rusit asuvat "
    "maatilallaan",

    "Asuinp. Karjalassa: Viipurin mlk. -27, Pohjois-Karjala 31—32, Viipuri 32—. "
    "Muut asuinp.: Lohja, Mustiala, Paimio Harkian perhe asuu omakotitalossaan.",

    "Asuinp. Karjalassa: Kaukola, Kortteensalmi -39, Sortavalan mlk. "
    "Muut asuinp.: Vihti 39—41, Kajaani, Helsinki, Paimio. Perniö, Paimio. Huuhkat asuvat",

    "Asuinp. Karjalassa: Vuoksenranta, Oravankytö 23—39,    41—44."
    "Muut asuinp.: Lottana -44, Kurikka 39—41, Ähtäri, Niemisvesi 44—. Viitaset asuvat"
]

LOCATION_HEURISTICS = {
    'long_name_with_mlk': {
            'text': "Asuinp. Karjalassa; Kristiinankaupungin mlk 23—39. Muut asuinp.: Kankaanpää 39— 40, "
                    "Hirvensalo -40, Perniö -40, Ähtäri, Hankavesi 41—44, Kristiinankaupungin mlk 45-. Aholat asuvat itse rakentamassaan omakotitalossa. "
                    "Herra Ahola on sotamies. Hän on saanut kunniamerkit Ts mm, Js mm, SVR m 1 ja SVR m 2. Kalastus ja puutarhanhoito "
                    "miellyttävät häntä. Hän on ollut asevarikkotehtävissä v.30—68.",
    },
    'short_white_listed_name': {
            'text': "Asuinp. Karjalassa; Eno 23—39. Muut asuinp.: Kankaanpää 39— 40, "
                    "Hirvensalo -40, Perniö -40, Ähtäri, Hankavesi 41—44, Utö 45-. Aholat asuvat itse rakentamassaan omakotitalossa. "
                    "Herra Ahola on sotamies. Hän on saanut kunniamerkit Ts mm, Js mm, SVR m 1 ja SVR m 2. Kalastus ja puutarhanhoito "
                    "miellyttävät häntä. Hän on ollut asevarikkotehtävissä v.30—68.",
    },

    'short_white_listed_alias_name': {
            'text': "Asuinp. Karjalassa; Ii 23—39. Muut asuinp.: Kankaanpää 39— 40, "
                    "Hirvensalo -40, Perniö -40, Ähtäri, Hankavesi 41—44, li 45-. Aholat asuvat itse rakentamassaan omakotitalossa. "
                    "Herra Ahola on sotamies. Hän on saanut kunniamerkit Ts mm, Js mm, SVR m 1 ja SVR m 2. Kalastus ja puutarhanhoito "
                    "miellyttävät häntä. Hän on ollut asevarikkotehtävissä v.30—68.",
    },


    'short_place_name': {
        'text': "Asuinp. Karjalassa; Viipuri 23—39, ktr. Muut asuinp.: Kankaanpää, ja 39— 40, "
                "Hirvensalo -40, Perniö -40, Ähtäri, Hankavesi 41—, ktr. Aholat asuvat itse rakentamassaan omakotitalossa. "
                "Herra Ahola on sotamies. Hän on saanut kunniamerkit Ts mm, Js mm, SVR m 1 ja SVR m 2. Kalastus ja puutarhanhoito "
                "miellyttävät häntä. Hän on ollut asevarikkotehtävissä v.30—68.",
        'expected': [
          {
            "movedOut": 40,
            "village": {
              "locationName": None
            },
            "movedIn": 39,
            "region": "other",
            "locationName": "Kankaanpää"
          },
          {
            "movedOut": 40,
            "village": {
              "locationName": None
            },
            "movedIn": None,
            "region": "other",
            "locationName": "Hirvensalo"
          },
          {
            "movedOut": 40,
            "village": {
              "locationName": None
            },
            "movedIn": None,
            "region": "other",
            "locationName": "Perniö"
          },
          {
            "movedOut": None,
            "village": {
              "locationName": "Hankavesi"
            },
            "movedIn": 41,
            "region": "other",
            "locationName": "Ähtäri"
          }
        ]
    },
    'long_place_name': {
        'text': "Asuinp. Karjalassa; Viipuri 23—39, Thisisnotarealplacebutsomenonsensewhichshouldnotbeconsideredasplace. Muut asuinp.: Kankaanpää, Lauhalan koulu 39— 40, "
                "Hirvensalo -40, Perniö -40, Ähtäri, Hankavesi 41—. Aholat asuvat itse rakentamassaan omakotitalossa. "
                "Herra Ahola on sotamies. Hän on saanut kunniamerkit Ts mm, Js mm, SVR m 1 ja SVR m 2. Kalastus ja puutarhanhoito "
                "miellyttävät häntä. Hän on ollut asevarikkotehtävissä v.30—68.",
        'expected': [
            {
                "region": "other",
                "locationName": "Kankaanpää",
                "movedIn": 39,
                "village": {
                  "locationName": "Lauhalankoulu"
                },
                "movedOut": 40
            },
            {
                "region": "other",
                "locationName": "Hirvensalo",
                "movedIn": None,
                "village": {
                  "locationName": None
                },
                "movedOut": 40
           },
           {
                "region": "other",
                "locationName": "Perniö",
                "movedIn": None,
                "village": {
                  "locationName": None
                },
                "movedOut": 40
           },
           {
                "region": "other",
                "locationName": "Ähtäri",
                "movedIn": 41,
                "village": {
                  "locationName": "Hankavesi"
                },
                "movedOut": None
           }
        ]
    }

}

# Expected location results for texts
EXPECTED_RESULTS = [
    {
        "finnish_locations": [{
            "movedIn": 39,
            "region": "other",
            "movedOut": 40,
            "locationName": "Urjala",
            "village": {
              "locationName": None
            }
          }, {
            "movedIn": 40,
            "region": "other",
            "movedOut": 42,
            "locationName": "Urjala",
            "village": {
              "locationName": "Honkola"
            }
          }, {
            "movedIn": None,
            "region": "other",
            "movedOut": 44,
            "locationName": "Sauvo",
            "village": {
              "locationName": "Timperlä"
            }
          }, {
            "movedIn": 44,
            "region": "other",
            "movedOut": None,
            "locationName": "Piikkiö",
            "village": {
              "locationName": "Viuhkalo"
            }
          }
        ]
    }
]

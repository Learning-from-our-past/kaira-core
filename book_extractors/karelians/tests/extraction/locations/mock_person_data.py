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
              "locationName": None,
              "coordinates": {
                "longitude": None,
                "latitude": None
              }
            },
            "movedIn": 39,
            "region": "other",
            "locationName": "Kankaanpää",
            "coordinates": {
              "longitude": "21.99682",
              "latitude": "62.97651"
            }
          },
          {
            "movedOut": 40,
            "village": {
              "locationName": None,
              "coordinates": {
                "longitude": None,
                "latitude": None
              }
            },
            "movedIn": None,
            "region": "other",
            "locationName": "Hirvensalo",
            "coordinates": {
              "longitude": "27.89087",
              "latitude": "61.56453"
            }
          },
          {
            "movedOut": 40,
            "village": {
              "locationName": None,
              "coordinates": {
                "longitude": None,
                "latitude": None
              }
            },
            "movedIn": None,
            "region": "other",
            "locationName": "Perniö",
            "coordinates": {
              "longitude": "23.15",
              "latitude": "60.25"
            }
          },
          {
            "movedOut": None,
            "village": {
              "locationName": "Hankavesi",
              "coordinates": {
                "longitude": "26.45",
                "latitude": "62.43333"
              }
            },
            "movedIn": 41,
            "region": "other",
            "locationName": "Ähtäri",
            "coordinates": {
              "longitude": "24.21264",
              "latitude": "62.59465"
            }
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
                "coordinates": {
                  "latitude": "62.97651",
                  "longitude": "21.99682"
                },
                "village": {
                  "coordinates": {
                    "latitude": None,
                    "longitude": None
                  },
                  "locationName": "Lauhalankoulu"
                },
                "movedOut": 40
            },
            {
                "region": "other",
                "locationName": "Hirvensalo",
                "movedIn": None,
                "coordinates": {
                  "latitude": "61.56453",
                  "longitude": "27.89087"
                },
                "village": {
                  "coordinates": {
                    "latitude": None,
                    "longitude": None
                  },
                  "locationName": None
                },
                "movedOut": 40
           },
           {
                "region": "other",
                "locationName": "Perniö",
                "movedIn": None,
                "coordinates": {
                  "latitude": "60.25",
                  "longitude": "23.15"
                },
                "village": {
                  "coordinates": {
                    "latitude": None,
                    "longitude": None
                  },
                  "locationName": None
                },
                "movedOut": 40
           },
           {
                "region": "other",
                "locationName": "Ähtäri",
                "movedIn": 41,
                "coordinates": {
                  "latitude": "62.59465",
                  "longitude": "24.21264"
                },
                "village": {
                  "coordinates": {
                    "latitude": "62.43333",
                    "longitude": "26.45"
                  },
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
            "coordinates": {
              "longitude": "23.53333",
              "latitude": "61.08333"
            },
            "region": "other",
            "movedOut": 40,
            "locationName": "Urjala",
            "village": {
              "coordinates": {
                "longitude": None,
                "latitude": None
              },
              "locationName": None
            }
          }, {
            "movedIn": 40,
            "coordinates": {
              "longitude": "23.53333",
              "latitude": "61.08333"
            },
            "region": "other",
            "movedOut": 42,
            "locationName": "Urjala",
            "village": {
              "coordinates": {
                "longitude": "25.64154",
                "latitude": "62.56873"
              },
              "locationName": "Honkola"
            }
          }, {
            "movedIn": None,
            "coordinates": {
              "longitude": "22.69642",
              "latitude": "60.34306"
            },
            "region": "other",
            "movedOut": 44,
            "locationName": "Sauvo",
            "village": {
              "coordinates": {
                "longitude": None,
                "latitude": None
              },
              "locationName": "Timperlä"
            }
          }, {
            "movedIn": 44,
            "coordinates": {
              "longitude": "22.51667",
              "latitude": "60.41667"
            },
            "region": "other",
            "movedOut": None,
            "locationName": "Piikkiö",
            "village": {
              "coordinates": {
                "longitude": None,
                "latitude": None
              },
              "locationName": "Viuhkalo"
            }
          }
        ]
    }
]

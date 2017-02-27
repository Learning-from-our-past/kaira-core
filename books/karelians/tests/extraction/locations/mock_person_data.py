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

# Expected location results for texts
EXPECTED_RESULTS = [
    {
        "finnish_locations": [{
            "movedIn": "39",
            "coordinates": {
              "longitude": "23.53333",
              "latitude": "61.08333"
            },
            "region": "other",
            "movedOut": "40",
            "locationName": "Urjala",
            "village": {
              "coordinates": {
                "longitude": "",
                "latitude": ""
              },
              "locationName": None
            }
          }, {
            "movedIn": "40",
            "coordinates": {
              "longitude": "23.53333",
              "latitude": "61.08333"
            },
            "region": "other",
            "movedOut": "42",
            "locationName": "Urjala",
            "village": {
              "coordinates": {
                "longitude": "25.64154",
                "latitude": "62.56873"
              },
              "locationName": "Honkola"
            }
          }, {
            "movedIn": "",
            "coordinates": {
              "longitude": "22.69642",
              "latitude": "60.34306"
            },
            "region": "other",
            "movedOut": "44",
            "locationName": "Sauvo",
            "village": {
              "coordinates": {
                "longitude": "",
                "latitude": ""
              },
              "locationName": "Timperlä"
            }
          }, {
            "movedIn": "44",
            "coordinates": {
              "longitude": "22.51667",
              "latitude": "60.41667"
            },
            "region": "other",
            "movedOut": "",
            "locationName": "Piikkiö",
            "village": {
              "coordinates": {
                "longitude": "",
                "latitude": ""
              },
              "locationName": "Viuhkalo"
            }
          }
        ]
    }
]

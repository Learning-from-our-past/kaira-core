# Person data is anonymized and tweaked and only usable for software testing.
PERSON_DATA = {
   'returnedToKarelia':True,
   'otherLocationCount':8,
   'karelianLocations':[
      {
         'coordinates':{
            'longitude':'30.14777',
            'latitude':'61.43684'
         },
         'locationName':'Lumivaara',
         'movedOut':'',
         'region':'karelia',
         'movedIn':''
      },
      {
         'coordinates':{
            'longitude':'31.8013',
            'latitude':'62.07013'
         },
         'locationName':'Hepolampi',
         'movedOut':'',
         'region':'karelia',
         'movedIn':''
      },
      {
         'coordinates':{
            'longitude':'29.30198',
            'latitude':'61.07768'
         },
         'locationName':'Kirvu',
         'movedOut':'',
         'region':'karelia',
         'movedIn':''
      },
      {
         'coordinates':{
            'longitude':'29.56764',
            'latitude':'61.14373'
         },
         'locationName':'Ojajärvi',
         'movedOut':'',
         'region':'karelia',
         'movedIn':''
      },
      {
         'coordinates':{
            'longitude':'30.44809',
            'latitude':'62.00364'
         },
         'locationName':'Jaakkima',
         'movedOut':'',
         'region':'karelia',
         'movedIn':''
      },
      {
         'coordinates':{
            'longitude':'',
            'latitude':''
         },
         'locationName':'lijärvi',
         'movedOut':'40',
         'region':'karelia',
         'movedIn':''
      },
      {
         'coordinates':{
            'longitude':'',
            'latitude':''
         },
         'locationName':'lijärvi',
         'movedOut':'44',
         'region':'karelia',
         'movedIn':'41'
      }
   ],
   'spouse':{
      'weddingYear':'1933',
      'originalFamily':'original',
      'deathYear':'',
      'hasSpouse':True,
      'birthData':{
         'birthYear':'1915',
         'birthDay':'2',
         'birthMonth':'2',
         'birthLocation':'Ylistarossa'
      },
      'spouseName':'SPOUSE NAME',
      'profession':'sairaanhoitaja'
   },
   'firstNames':'FIRST NAMES',
   'gender':'Male',
   'birthMonth':'3',
   'surname':'SURNAME',
   'girlCount':1,
   'originalFamily':'',
   'imagePath':'',
   'otherLocations':[
      {
         'coordinates':{
            'longitude':'25.5',
            'latitude':'61'
         },
         'locationName':'Hollola',
         'movedOut':'',
         'region':'other',
         'movedIn':''
      },
      {
         'coordinates':{
            'longitude':'27.83853',
            'latitude':'61.23663'
         },
         'locationName':'Kurhila',
         'movedOut':'40',
         'region':'other',
         'movedIn':''
      },
      {
         'coordinates':{
            'longitude':'25.66273',
            'latitude':'61.14071'
         },
         'locationName':'Vesivehmaa',
         'movedOut':'',
         'region':'other',
         'movedIn':''
      },
      {
         'coordinates':{
            'longitude':'25.65411',
            'latitude':'60.98277'
         },
         'locationName':'Lahti',
         'movedOut':'41',
         'region':'other',
         'movedIn':''
      },
      {
         'coordinates':{
            'longitude':'21.76382',
            'latitude':'60.86745'
         },
         'locationName':'Pirttikylä',
         'movedOut':'46',
         'region':'other',
         'movedIn':'44'
      },
      {
         'coordinates':{
            'longitude':'22.51306',
            'latitude':'62.93958'
         },
         'locationName':'Ylistaro',
         'movedOut':'58',
         'region':'other',
         'movedIn':''
      },
      {
         'coordinates':{
            'longitude':'22.85',
            'latitude':'63.23333'
         },
         'locationName':'Alahärmä',
         'movedOut':'',
         'region':'other',
         'movedIn':''
      },
      {
         'coordinates':{
            'longitude':'27.11667',
            'latitude':'65.6'
         },
         'locationName':'Hakola',
         'movedOut':'58',
         'region':'other',
         'movedIn':''
      }
   ],
   'originalText':'redacted',
   'childCount':2,
   'omakotitalo':True,
   'karelianLocationCount':7,
   'boyCount':1,
   'birthDay':'7',
   'maybePreviousMarriages':False,
   'birthYear':'1927',
   'birthLocation':'Lumivaarassa',
   'approximatePageNumber':'4-6',
   'children':[
      {
         'location':'',
         'gender':'Male',
         'birthYear':'1955',
         'name':'Child1',
         'coordinates':{
            'longitude':'',
            'latitude':''
         }
      },
      {
         'location':'',
         'gender':'Female',
         'birthYear':'1956',
         'name':'Child2',
         'coordinates':{
            'longitude':'',
            'latitude':''
         }
      }
   ],
   'profession':'huoltomies'
}

EXPECTED_JSON = """
[
    {
        "otherLocationCount": 8,
        "originalFamily": "",
        "originalText": "redacted",
        "birthYear": 1927,
        "omakotitalo": true,
        "locations": [
            {
                "movedOut": null,
                "locationName": "Lumivaara",
                "region": "karelia",
                "coordinates": {
                    "latitude": "61.43684",
                    "longitude": "30.14777"
                },
                "movedIn": null
            },
            {
                "movedOut": null,
                "locationName": "Hepolampi",
                "region": "karelia",
                "coordinates": {
                    "latitude": "62.07013",
                    "longitude": "31.8013"
                },
                "movedIn": null
            },
            {
                "movedOut": null,
                "locationName": "Kirvu",
                "region": "karelia",
                "coordinates": {
                    "latitude": "61.07768",
                    "longitude": "29.30198"
                },
                "movedIn": null
            },
            {
                "movedOut": null,
                "locationName": "Ojajärvi",
                "region": "karelia",
                "coordinates": {
                    "latitude": "61.14373",
                    "longitude": "29.56764"
                },
                "movedIn": null
            },
            {
                "movedOut": null,
                "locationName": "Jaakkima",
                "region": "karelia",
                "coordinates": {
                    "latitude": "62.00364",
                    "longitude": "30.44809"
                },
                "movedIn": null
            },
            {
                "movedOut": 40,
                "locationName": "lijärvi",
                "region": "karelia",
                "coordinates": {
                    "latitude": "",
                    "longitude": ""
                },
                "movedIn": null
            },
            {
                "movedOut": 44,
                "locationName": "lijärvi",
                "region": "karelia",
                "coordinates": {
                    "latitude": "",
                    "longitude": ""
                },
                "movedIn": 41
            },
            {
                "movedOut": null,
                "locationName": "Hollola",
                "region": "other",
                "coordinates": {
                    "latitude": "61",
                    "longitude": "25.5"
                },
                "movedIn": null
            },
            {
                "movedOut": 40,
                "locationName": "Kurhila",
                "region": "other",
                "coordinates": {
                    "latitude": "61.23663",
                    "longitude": "27.83853"
                },
                "movedIn": null
            },
            {
                "movedOut": null,
                "locationName": "Vesivehmaa",
                "region": "other",
                "coordinates": {
                    "latitude": "61.14071",
                    "longitude": "25.66273"
                },
                "movedIn": null
            },
            {
                "movedOut": 41,
                "locationName": "Lahti",
                "region": "other",
                "coordinates": {
                    "latitude": "60.98277",
                    "longitude": "25.65411"
                },
                "movedIn": null
            },
            {
                "movedOut": 46,
                "locationName": "Pirttikylä",
                "region": "other",
                "coordinates": {
                    "latitude": "60.86745",
                    "longitude": "21.76382"
                },
                "movedIn": 44
            },
            {
                "movedOut": 58,
                "locationName": "Ylistaro",
                "region": "other",
                "coordinates": {
                    "latitude": "62.93958",
                    "longitude": "22.51306"
                },
                "movedIn": null
            },
            {
                "movedOut": null,
                "locationName": "Alahärmä",
                "region": "other",
                "coordinates": {
                    "latitude": "63.23333",
                    "longitude": "22.85"
                },
                "movedIn": null
            },
            {
                "movedOut": 58,
                "locationName": "Hakola",
                "region": "other",
                "coordinates": {
                    "latitude": "65.6",
                    "longitude": "27.11667"
                },
                "movedIn": null
            }
        ],
        "returnedToKarelia": true,
        "imagePath": "",
        "surname": "SURNAME",
        "birthLocation": "Lumivaarassa",
        "girlCount": 1,
        "approximatePageNumber": "4-6",
        "children": [
            {
                "name": "Child1",
                "birthYear": 1955,
                "coordinates": {
                    "latitude": "",
                    "longitude": ""
                },
                "gender": "Male",
                "location": ""
            },
            {
                "name": "Child2",
                "birthYear": 1956,
                "coordinates": {
                    "latitude": "",
                    "longitude": ""
                },
                "gender": "Female",
                "location": ""
            }
        ],
        "birthDay": 7,
        "gender": "Male",
        "profession": "huoltomies",
        "childCount": 2,
        "boyCount": 1,
        "maybePreviousMarriages": false,
        "spouse": {
            "hasSpouse": true,
            "weddingYear": 1933,
            "deathYear": null,
            "spouseName": "SPOUSE NAME",
            "originalFamily": "original",
            "birthData": {
                "birthDay": 2,
                "birthLocation": "Ylistarossa",
                "birthMonth": 2,
                "birthYear": 1915
            },
            "profession": "sairaanhoitaja"
        },
        "firstNames": "FIRST NAMES",
        "karelianLocationCount": 7,
        "birthMonth": 3
    }
]
"""
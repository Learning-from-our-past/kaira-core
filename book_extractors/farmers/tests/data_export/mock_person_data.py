# Person data is anonymized and tweaked and only usable for software testing.
PERSON_DATA = {
   'farmName':'FARM NAME',
   'owner':{
      'gender':'Male',
      'birthData':{
         'birthMonth':'7',
         'birthDay':'28',
         'birthYear':'1903'
      },
      'firstNames':'First names',
      'ownerFrom':1942,
      'surname':'Surname'
   },
   'children':[
      {
         'name':'Child 1',
         'gender':'Female',
         'birthYear':'1925'
      },
      {
         'name':'Child 2',
         'gender':'Female',
         'birthYear':'1932'
      }
   ],
   'childCount':2,
   'approximatePageNumber':'0-2',
   'farmLocation':{
      'latitude':'60.68333',
      'locationName':'ANJALA',
      'longitude':'26.83333'
   },
   'hostess':{
      'gender':'Female',
      'birthData':{
         'birthMonth':'6',
         'birthDay':'15',
         'birthYear':'1901'
      },
      'firstNames':'First names',
      'surname':'Surname'
   },
   'quantities':{
      'dairyCow':'',
      'chicken':'150',
      'nuori':'',
      'lihotussika':'2',
      'sheep':'2',
      'slaughterAnimal':'',
      'emakko':'',
      'rooms':5
   },
   'maybePreviousMarriages':False,
   'boyCount':0,
   'farmDetails':{
      'wasteArea':'',
      'wholeArea':'48,49',
      'forestArea':'36,16',
      'meadowArea':'',
      'fieldArea':'5,51'
   },
   'girlCount':2,
   'keywordFlags':{
      'chicken':True,
      'salaojitus':False,
      'pine':False,
      'threshingMachine':False,
      'milkingMachine':False,
      'hiesu':False,
      'swedishTurnip':False,
      'someoneDead':False,
      'barley':False,
      'savi':True,
      'wheat':False,
      'hay':False,
      'stable':False,
      'moreeni':False,
      'potatoes':False,
      'oat':False,
      'kantatila':True,
      'tractor':False,
      'hieta':False,
      'rye':False,
      'multa':False,
      'sugarbeet':False,
      'garage':False,
      'horse':False,
      'cowhouse':False,
      'siirtotila':False,
      'muta':False,
      'birch':False,
      'spruce':True,
      'sauna':True
   }
}

EXPECTED_JSON = """
[
    {
        "farmName": "FARM NAME",
        "owner": {
            "gender": "Male",
            "birthData": {
                "birthMonth": 7,
                "birthDay": 28,
                "birthYear": 1903
            },
            "firstNames": "First names",
            "ownerFrom": 1942,
            "surname": "Surname"
        },
        "children": [
            {
                "name": "Child 1",
                "gender": "Female",
                "birthYear": 1925
            },
            {
                "name": "Child 2",
                "gender": "Female",
                "birthYear": 1932
            }
        ],
        "childCount": 2,
        "approximatePageNumber": "0-2",
        "farmLocation": {
            "latitude": "60.68333",
            "locationName": "ANJALA",
            "longitude": "26.83333"
        },
        "hostess": {
            "gender": "Female",
            "birthData": {
                "birthMonth": 6,
                "birthDay": 15,
                "birthYear": 1901
            },
            "firstNames": "First names",
            "surname": "Surname"
        },
        "quantities": {
            "dairyCow": null,
            "chicken": 150,
            "nuori": null,
            "lihotussika": 2,
            "sheep": 2,
            "slaughterAnimal": null,
            "emakko": null,
            "rooms": 5
        },
        "maybePreviousMarriages": false,
        "boyCount": 0,
        "farmDetails": {
            "wasteArea": null,
            "wholeArea": 48.49,
            "forestArea": 36.16,
            "meadowArea": null,
            "fieldArea": 5.51
        },
        "girlCount": 2,
        "keywordFlags": {
            "chicken": true,
            "salaojitus": false,
            "pine": false,
            "threshingMachine": false,
            "milkingMachine": false,
            "hiesu": false,
            "swedishTurnip": false,
            "someoneDead": false,
            "barley": false,
            "savi": true,
            "wheat": false,
            "hay": false,
            "stable": false,
            "moreeni": false,
            "potatoes": false,
            "oat": false,
            "kantatila": true,
            "tractor": false,
            "hieta": false,
            "rye": false,
            "multa": false,
            "sugarbeet": false,
            "garage": false,
            "horse": false,
            "cowhouse": false,
            "siirtotila": false,
            "muta": false,
            "birch": false,
            "spruce": true,
            "sauna": true
        }
    }
]
"""
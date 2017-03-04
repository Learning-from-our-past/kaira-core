import re

WHITE_LIST = {
  'names': {
    'eno': {},
    'evo': {},
    'ii': {},
    'li': {'alias': 'Ii'},
    'utö': {},
    'usa': {}
  },
  'patterns': [
    {
      'find': re.compile('([A-ZÄÖa-zäö-]*)(mlk)'),
      'replace': r'\1 mlk'
    }
  ]
}
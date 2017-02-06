import json
"""
General information about the app shown in About and update dialogs and used to provide links to places
and check updates. Should be updated accordingly when doing a release. Especially the version attribute.
"""
with open('./app_information.json', 'r', encoding='utf-8') as f:
    ABOUT_INFORMATION = json.loads(f.read())
    f.close()

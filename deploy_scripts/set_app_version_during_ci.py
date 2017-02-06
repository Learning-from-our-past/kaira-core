import json
import sys
import re

with open('./app_information.json', 'r', encoding='utf-8') as to_load:
    ABOUT_INFORMATION = json.loads(to_load.read())

    version_number = "v0.0.0"

    if len(sys.argv) > 1:
        version_number = sys.argv[1]

    if not re.match('v\d+\.\d+\.\d+', version_number):
        print('Please provide the version number in correct format: v0.1.1')
        sys.exit(1)

    # Replace the version number with given one
    ABOUT_INFORMATION["version"] = version_number
    to_load.close()

    with open('./app_information.json', 'w', encoding='utf-8') as to_save:
        json.dump(ABOUT_INFORMATION, to_save, indent=2)
        to_save.close()
        print("Application version set to ", ABOUT_INFORMATION["version"])

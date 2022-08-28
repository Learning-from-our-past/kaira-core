import sys
import getopt
import json


def main(argv):
    try:
        opts, args = getopt.getopt(argv, 'l')
    except getopt.GetoptError:
        sys.exit(2)

    inputfile = args[0]
    print_list = False

    for opt, arg in opts:
        if opt == '-l':
            print_list = True

    with open(inputfile, encoding='utf8') as data_file:
        data = json.load(data_file)

    data_file.close()

    person_count = len(data)
    many_locations_count = 0
    locations_threshold = 10
    location_over_all_count = 0
    persons_with_no_locations = 0

    long_place_name = 16
    persons_with_long_place_name = 0
    persons_with_short_place_name = 0
    short_place_name = 3

    persons_with_many_locations = []
    persons_with_short_place_names = []

    for idx, person in enumerate(data):
        location_over_all_count += len(person['locations'])

        if len(person['locations']) == 0:
            persons_with_no_locations += 1

        if len(person['locations']) > locations_threshold:
            many_locations_count += 1
            persons_with_many_locations.append(person)

        long = False
        short = False
        for l in person['locations']:
            if not long and len(l['locationName']) >= long_place_name:
                persons_with_long_place_name += 1
                long = True

            if not short and len(l['locationName']) <= short_place_name:
                persons_with_short_place_name += 1
                persons_with_short_place_names.append(l['locationName'])

    print('Persons:', person_count)
    print('Persons location avg:', location_over_all_count / person_count)
    print(
        'Persons with over',
        locations_threshold,
        'locations:',
        many_locations_count,
        '---',
        '{0:.2f}'.format(many_locations_count / person_count * 100),
        '%',
    )
    print(
        'Persons with 0 locations',
        persons_with_no_locations,
        '---',
        '{0:.2f}'.format(persons_with_no_locations / person_count * 100),
        '%',
    )
    print(
        'Persons with long place name',
        persons_with_long_place_name,
        '---',
        '{0:.2f}'.format(persons_with_long_place_name / person_count * 100),
        '%',
    )
    print(
        'Persons with short place name',
        persons_with_short_place_name,
        '---',
        '{0:.2f}'.format(persons_with_short_place_name / person_count * 100),
        '%',
    )

    if print_list:
        for p in persons_with_many_locations:
            print(p['surname'], p['firstNames'])
            print(', '.join([l['locationName'] for l in p['locations']]))

        # for p in list(set(persons_with_short_place_names)):
        #     print(p)


if __name__ == '__main__':
    main(sys.argv[1:])

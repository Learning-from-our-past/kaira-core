import sys
import getopt
import json
from deepdiff import DeepDiff


def main(argv):
    try:
        opts, args = getopt.getopt(argv, 'l')
    except getopt.GetoptError:
        sys.exit(2)

    inputfile1 = args[0]
    inputfile2 = args[1]

    with open(inputfile1, encoding='utf8') as data_file:
        data1 = json.load(data_file)

    with open(inputfile2, encoding='utf8') as data_file:
        data2 = json.load(data_file)

    assert len(data1) == len(data2)

    total = len(data1)
    datas = zip(data1, data2)
    for idx, person in enumerate(datas):
        diff = DeepDiff(person[0], person[1], ignore_order=True)

        percentage = round((idx / total) * 100)

        sys.stdout.write('Progress: %d%%  \r' % (percentage))
        sys.stdout.flush()

        if bool(diff):
            print(person[0]['primaryPerson']['name'])
            print(idx, diff)
            input('Continue')


if __name__ == '__main__':
    main(sys.argv[1:])

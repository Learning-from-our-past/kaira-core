import sys
import getopt
import json


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
    assert data1 == data2


if __name__ == '__main__':
    main(sys.argv[1:])
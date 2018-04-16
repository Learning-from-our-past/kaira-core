class Sex:
    male_names = set()
    female_names = set()

    @staticmethod
    def load_names():
        if len(Sex.male_names) == 0:
            f = open('./support_datasheets/men.names', 'r', encoding='utf8')
            for row in f:
                row = row.strip('\n')
                row = row.lower()
                Sex.male_names.add(row)

        if len(Sex.female_names) == 0:
            f = open('./support_datasheets/women.names', 'r', encoding='utf8')
            for row in f:
                row = row.strip('\n')
                row = row.lower()
                Sex.female_names.add(row)

    @staticmethod
    def find_sex(name_string):
        """
        Tries to determine sex from a string of name(s).
        :param name_string: A string containing one or more names.
        :return: 'Male', 'Female' or None
        """
        names = tuple(word.casefold() for word in name_string.split(' ') if word)
        num_male_names, num_female_names = Sex._count_sex_specific_names(names)
        sex = None
        if num_male_names > num_female_names:
            sex = 'Male'
        elif num_female_names > num_male_names:
            sex = 'Female'
        elif num_male_names == 0 and num_female_names == 0 and len(names) >= 1:
            raise SexException()

        return sex

    @staticmethod
    def _count_sex_specific_names(names):
        num_male_names = 0
        num_female_names = 0

        for name in names:
            if name in Sex.male_names:
                num_male_names += 1
            elif name in Sex.female_names:
                num_female_names += 1

        return num_male_names, num_female_names


class SexException(Exception):
    message = u'Sex not found!'
    eType = 'Sex WAS NOT FOUND'

    def __init__(self):
        pass

    def __unicode__(self):
        return self.message

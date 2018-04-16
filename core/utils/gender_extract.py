class Gender():
    male_names = []
    female_names = []

    @staticmethod
    def load_names():
        if len(Gender.male_names) == 0:
            f = open("./support_datasheets/men.names", "r", encoding="utf8")
            for row in f:
                row = row.strip("\n")
                row = row.lower()
                Gender.male_names.append(row)
            Gender.male_names = set(Gender.male_names)

        if len(Gender.female_names) == 0:
            f = open("./support_datasheets/women.names", "r", encoding="utf8")
            for row in f:
                row = row.strip("\n")
                row = row.lower()
                Gender.female_names.append(row)
            Gender.female_names = set(Gender.female_names)

    @staticmethod
    def find_gender(name_string):
        """
        Tries to determine sex from a string of name(s).
        :param name_string: A string containing one or more names.
        :return: 'Male', 'Female' or None
        """
        names = tuple(word.casefold() for word in name_string.split(' ') if word)
        num_male_names, num_female_names = Gender._count_sex_specific_names(names)
        sex = None
        if num_male_names > num_female_names:
            sex = 'Male'
        elif num_female_names > num_male_names:
            sex = 'Female'
        elif num_male_names == 0 and num_female_names == 0 and len(names) >= 1:
            raise GenderException()

        return sex

    @staticmethod
    def _count_sex_specific_names(names):
        num_male_names = 0
        num_female_names = 0

        for name in names:
            if name in Gender.male_names:
                num_male_names += 1
            elif name in Gender.female_names:
                num_female_names += 1

        return num_male_names, num_female_names


class GenderException(Exception):
    message = u"Gender not found!"
    eType = "GENDER WAS NOT FOUND"

    def __init__(self):
       pass

    def __unicode__(self):
        return self.message
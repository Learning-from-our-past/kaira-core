import re
class Gender():
    male_names = []
    female_names = []

    @staticmethod
    def load_names():
        if len(Gender.male_names) == 0:
            f = open("./names/men.names", "r", encoding="utf8")
            for row in f:
                row = row.strip("\n")
                row = row.lower()
                Gender.male_names.append(row)
            Gender.male_names = set(Gender.male_names)

        if len(Gender.female_names) == 0:
            f = open("./names/women.names", "r", encoding="utf8")
            for row in f:
                row = row.strip("\n")
                row = row.lower()
                Gender.female_names.append(row)
            Gender.female_names = set(Gender.female_names)

    @staticmethod
    def find_gender(name):
        firstname = re.search(r"(?P<name>^\w+)", name.lower(), re.UNICODE | re.IGNORECASE)
        try:
            if firstname.group("name") in Gender.male_names:
                return "Male"
            elif firstname.group("name") in Gender.female_names:
                return "Female"
            else:
                raise GenderException()
        except AttributeError:
            return ""


class GenderException(Exception):
    message = u"Gender not found!"
    eType = "GENDER WAS NOT FOUND"
    def __init__(self):
       pass

    def __unicode__(self):
        return self.message
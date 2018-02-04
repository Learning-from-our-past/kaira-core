
class RequiredDependenciesAreMissing(Exception):
    def __str__(self):
        return repr('There is a mismatch between the amount of expected dependencies of the extractor and'
                    'the amount of dependencies provided in YAML configuration.')

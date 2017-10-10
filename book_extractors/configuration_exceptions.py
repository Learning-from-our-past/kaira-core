class ConfigurationException(Exception):
    pass


class DependencyConfigurationException(ConfigurationException):
    def __init__(self, missing_contexts):
        self.missing_contexts = missing_contexts

    def __str__(self):
        return repr('There is a mismatch between the amount of dependencies and dependency contexts! '
                    'Please explicitly enter a context for each dependency. '
                    'The following extractors are missing a context: {0}'.format(self.missing_contexts))
    pass

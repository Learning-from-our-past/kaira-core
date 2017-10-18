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


class ContextKeywordConfigurationException(ConfigurationException):
    def __str__(self):
        return repr('Something is wrong with your dependency contexts! The context has to be either '
                    'current, main or a string of however many parents you want, separated by dots.')


class ParentKeywordConfigurationException(ConfigurationException):
    def __str__(self):
        return repr('Reached main pipeline before reaching the parent pipeline configured in the '
                    'dependency\'s contexts. This probably means there are too many \'parent\' '
                    'or that parent_data is not being passed correctly to subpipelines.')

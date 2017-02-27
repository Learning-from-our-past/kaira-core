from interface.valuewrapper import ValueWrapper


def unwrap(d):
    """
    Utility function to unwrap the given dict which contains ValueWrapped data
    and returns pure dict/list structure.
    :param d:
    :return:
    """
    def _unwrap(data):
        if isinstance(data, ValueWrapper):
            if isinstance(data.value, dict):
                result = {}
                for key, value in data.value.items():
                    result[key] = _unwrap(value)
            elif isinstance(data.value, list):
                result = []
                for index, value in enumerate(data.value):
                    result.append(_unwrap(value))
            else:
                return data.value  # primitive data structure
        else:
            return data

        return result

    r = {}
    for key, property in d.items():
        r[key] = _unwrap(property)

    return r




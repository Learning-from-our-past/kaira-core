import copy


class ExtractorResultsMap:
    """
    Class which wraps a dict containing the results of the all extractors which are executed during the
    data extraction of one person. Can be used to resolve the dependencies of the extractors.
    Each extractor has an unique id which is mapped to the results of the said extractor. During dependency resolving,
    each extractor can fetch the data they need from the this result map using their id as a key.
    """

    def __init__(self):
        self._extractor_results = {}

    def add_results(self, extractor_id, extraction_results):
        """
        Add results of the extractor to the results map. Note that this creates
        a deep copy of the results to preserve the data in its original format. In subpipelines
        sometimes the results of the subpipeline is modified afterwards.
        """
        self._extractor_results[extractor_id] = copy.deepcopy(extraction_results)

    def get_results(self, extractor_id):
        """
        Get results of the specified extractor. Used to get the data some extractor requires as a dependency.
        Returns a deep copy of the data to prevent changes to the original data.
        """
        if extractor_id in self._extractor_results:
            return copy.deepcopy(self._extractor_results[extractor_id])
        else:
            raise Exception('No extraction results could be found for the extractor. '
                            'Likely it was not executed before trying to access its results for dependency.')

    def clear(self):
        """
        Clears the extractor results. Should be done after one person's data extraction is finished.
        """
        self._extractor_results = {}

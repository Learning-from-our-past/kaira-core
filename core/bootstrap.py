import glob
import os
import yaml


def setup_extraction_framework_for_bookseries(bookseries_id, plugin_directory):
    available_bookseries = {x['book_series_id']: x for x in find_available_bookseries_from_directory(plugin_directory)}

    if bookseries_id not in available_bookseries:
        raise BookSeriesNotSupportedException()


def find_available_bookseries_from_directory(directory_path):
    """
    Find available bookseries by scanning book_extractors directory for manifest files.
    :return:
    """
    manifest_glob_pattern = os.path.join('.', directory_path, '*', 'manifest.yaml')
    manifest_files = [open(file) for file in glob.iglob(manifest_glob_pattern)]
    manifests = [yaml.load(file) for file in manifest_files]

    for file in manifest_files:
        file.close()

    return manifests


class BookSeriesNotSupportedException(Exception):
    def __str__(self):
        return repr('Bookseries is not supported.')

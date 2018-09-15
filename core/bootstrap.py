import glob
import os
import yaml
from core.bookseries import BookSeries


def setup_extraction_framework_for_bookseries(bookseries_id, plugin_directory, update_callback):
    available_bookseries = {x['book_series_id']: x for x in find_available_bookseries_from_directory(plugin_directory)}

    if bookseries_id not in available_bookseries:
        raise BookSeriesNotSupportedException()

    return BookSeries(available_bookseries[bookseries_id], update_callback)


def find_available_bookseries_from_directory(directory_path):
    """
    Find available bookseries by scanning extractors directory for manifest files.
    :return:
    """
    manifest_glob_pattern = os.path.join('.', directory_path, '*', 'manifest.yaml')
    manifest_files = [open(file, encoding='utf8') for file in glob.iglob(manifest_glob_pattern)]
    manifests = [yaml.load(file) for file in manifest_files]

    # Store path to the extractor plugin directory to the manifest object
    for (manifest, manifest_file) in zip(manifests, manifest_files):
        manifest['path'] = os.path.dirname(manifest_file.name)
        manifest_file.close()

    return manifests


class BookSeriesNotSupportedException(Exception):
    def __str__(self):
        return repr('Bookseries is not supported.')

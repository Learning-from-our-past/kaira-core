from invoke import task
import sys
import os
from shared.geo.update_geo_db import update_location_db


@task()
def test(ctx):
    """
    Run tests
    """
    ctx.run('python -m pytest')


@task(help={
    'input-files': 'List of input files, space separated, inside quotation marks.',
    'filter-duplicates': 'Whether to filter duplicates out while chunking.',
    'bookseries': 'Name of the bookseries we are going to be chunking.',
    'defaults': 'Whether to use default settings for the bookseries provided with -b'
})
def chunk(ctx, bookseries=None, input_files=None, filter_duplicates=False, defaults=False):
    """
    Run chunking on specified files or with default settings.
    Provide files to be chunked with -i. Files are assumed to be in the correct
    order. Use -b to specify which bookseries the books belong to and --filter
    to specify whether duplicates should be filtered out. Chunking can also be
    ran with default settings, using the --defaults flag, in which case only -b
    needs to be specified.

    Examples:
         invoke chunk -i "material/book1.html material/book2.html" -b mybookseries
         invoke chunk -b siirtokarjalaiset -fd
    """
    if bookseries:
        to_filter = '--filter ' if filter_duplicates else ''
        kaira_cmd = 'python main.py {}-b {}'.format(to_filter, bookseries)
    else:
        print('Error: a value for bookseries needs to be provided.')
        sys.exit(1)

    if defaults:
        default_settings = {
            'siirtokarjalaiset': {
                'filename_template': 'material/siirtokarjalaiset_{}.{}',
                'book_numerals': ['I', 'II', 'III', 'IV']
            }
        }

        series_defaults = default_settings[bookseries]
        inputs = [series_defaults['filename_template'].format(x, 'html')
                  for x in series_defaults['book_numerals']]
    else:
        inputs = input_files.split(' ')

    output_files = ['{}.xml'.format(x[:x.index('.')]) for x in inputs]

    kaira_cmd = '{} -c {} -o {} -n {}'.format(
        kaira_cmd,
        ' '.join(inputs),
        ' '.join(output_files),
        ' '.join([str(x) for x in range(1, len(inputs) + 1)])
    )

    ctx.run(kaira_cmd)


@task(optional=['bookpath', 'testset'], help={
    'bookpath': 'A path to the data xml-file which should be extracted.',
    'testset': 'If set, extract the testset_I.json file in material directory.'
})
def extract(ctx, bookpath=None, testset=None):
    """
    Extract data from xml-file and save it to json-format.
    Extract either predefined test_set_I.json from material/ directory with option -t
    or any xml-datafile from path provided with option -b.
    """
    if testset:
        ctx.run('python main.py -i material/testset_I.xml -o material/testset_I.json')
    elif bookpath:
        file_name = os.path.basename(bookpath)[0]
        ctx.run('python main.py -i {} -o material/{}.json'.format(bookpath, file_name))
    else:
        print('Error: either valid book path should be provided with option -p or run the test set with -t option.')
        sys.exit(1)


@task(help={'parallel': 'How many books to extract concurrently. Value should be 2 or 4.'})
def extract_parallel(ctx, parallel=2):
    """
    Extracts concurrently in 2 or 4 processes the siirtokarjalaisten_tie books in material/ directory.
    """
    if parallel == 2 or parallel == 4:
        ctx.run('tasks/multi_process_extractor.sh -p {}'.format(parallel))
    else:
        print('Error: -p option should be either 2 or 4.')
        sys.exit(1)


@task(help={'datasheet': 'Path to the datasheet containing location data.'})
def update_locationdb(ctx, datasheet=None):
    """
    Update location data in the Kaira's location.db which is used to add GPS-coordinates to the
    extraction results. Datasheet format specification can be found from shared/geo/update_geo_db.py
    """
    update_location_db(datasheet)
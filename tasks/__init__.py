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


@task()
def setup(ctx):
    """
    Setup the project by creating mongodb for geotagging.
    Assumes Mongodb is installed and running.
    """
    ctx.run('wget https://github.com/Learning-from-our-past/kaira-core/releases/download/mongodump2/geonames_dump.zip')
    ctx.run('unzip geonames_dump.zip')
    ctx.run('mongorestore dump')
    ctx.run('rm -rf dump/; rm -rf geonames_dump.zip')


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
        file_name = os.path.splitext('bookpath')[0]
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

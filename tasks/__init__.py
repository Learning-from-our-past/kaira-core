from invoke import task
import sys
import os
from core.utils.geo.update_geo_db import update_location_db


options_black_formatting = '--skip-string-normalization'


@task()
def code_check_flake8(ctx):
    """
    Run code format check with flake8
    """
    ctx.run('flake8 .')


@task()
def code_check_black(ctx):
    """
    Run code format check with black
    """
    ctx.run('black . --check {}'.format(options_black_formatting))


@task()
def code_check(ctx):
    """
    Run code format check
    """
    ctx.run('inv code-check-black && inv code-check-flake8')


@task()
def code_format(ctx):
    """
    Run code formatting
    """
    ctx.run('black . {}'.format(options_black_formatting))


@task()
def test(ctx):
    """
    Run tests
    """
    ctx.run('python -m pytest --ignore .direnv')


@task(
    help={
        'input-files': 'List of input files, space separated, inside quotation marks.',
        'filter-duplicates': 'Whether to filter duplicates out while chunking.',
        'bookseries': 'Name of the bookseries we are going to be chunking.',
        'defaults': 'Whether to use default settings for the bookseries provided with -b',
    }
)
def chunk(
    ctx, bookseries=None, input_files=None, filter_duplicates=False, defaults=False
):
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
                'book_numerals': ['I', 'II', 'III', 'IV'],
            }
        }

        series_defaults = default_settings[bookseries]
        inputs = [
            series_defaults['filename_template'].format(x, 'html')
            for x in series_defaults['book_numerals']
        ]
    else:
        inputs = input_files.split(' ')

    output_files = ['{}.xml'.format(x[: x.index('.')]) for x in inputs]

    kaira_cmd = '{} -c {} -o {} -n {}'.format(
        kaira_cmd,
        ' '.join(inputs),
        ' '.join(output_files),
        ' '.join([str(x) for x in range(1, len(inputs) + 1)]),
    )

    ctx.run(kaira_cmd)


@task(
    help={
        'bookpath': 'A path to the data xml-file which should be extracted.',
        'testset': 'Extract the testset_I.json file material directory. Overrides -b.',
    }
)
def extract(ctx, bookpath=None, testset=False):
    """
    Extract data from xml-file and save it to json-format.
    Extract either predefined testset_I.xml from material/ directory with option -t
    or any xml-datafile from path provided with option -b.
    """
    if testset:
        ctx.run('python main.py -i material/testset_I.xml -o material/testset_I.json')
    elif bookpath:
        file_name = os.path.splitext(os.path.basename(bookpath))[0]
        ctx.run('python main.py -i {} -o material/{}.json'.format(bookpath, file_name))
    else:
        print('Error: provide a valid book path using -b or extract testset with -t.')
        sys.exit(1)


@task(
    help={'parallel': 'How many books to extract concurrently. Value should be 2 or 4.'}
)
def extract_parallel(ctx, parallel=2):
    """
    Extracts concurrently in 2 or 4 processes the
    siirtokarjalaisten_tie books in material/ directory.
    """
    if parallel == 2 or parallel == 4:
        ctx.run('tasks/multi_process_extractor.sh -p {}'.format(parallel))
    else:
        print('Error: -p option should be either 2 or 4.')
        sys.exit(1)


@task(help={'datasheet': 'Path to the datasheet containing location data.'})
def update_locationdb(ctx, datasheet=None):
    """
    Update location data in the Kaira's location.db which is used to
    add GPS-coordinates to the extraction results. Datasheet format
    specification can be found from shared/geo/update_geo_db.py
    """
    update_location_db(datasheet)


@task(
    optional=['input_file', 'output_file', 'books'],
    help={
        'input_file': 'Input file with KairaIDs, one per row. Default: ids.txt',
        'output_file': 'Output file to place all the generated XML in. Default: ids.xml',
        'books': (
            'Paths to the books where the person entries corresponding to the '
            'KairaIDs can be found from. Default: siirtokarjalaiset_I-IV.xml in '
            'material/'
        ),
    },
)
def kairaid2xml(ctx, input_file=None, output_file=None, books=None):
    """
    Use a file that contains newline separated KairaIDs to generate
    an XML file with the person entries corresponding to the KairaIDs.
    """
    kairaid2xml_cmd = '-input {} -output {} -books {}'

    if not input_file:
        input_file = 'material/ids.txt'

    if not output_file:
        output_file = 'material/ids.xml'

    if not books:
        path_template = 'material/siirtokarjalaiset_{}.xml'
        book_suffices = ('I', 'II', 'III', 'IV')
        books = ' '.join([path_template.format(x) for x in book_suffices])

    kairaid2xml_cmd = kairaid2xml_cmd.format(input_file, output_file, books)
    ctx.run('python analysis_toolkit/kairaid2xml.py {}'.format(kairaid2xml_cmd))


@task(
    optional=['books'],
    help={
        'regex': 'The regular expression to use for testing.',
        'books': 'Paths to the books. Default: siirtokarjalaiset_I-IV.xml in material/',
        'hyphens': 'Remove hyphens from text before checking for regex matches.',
        'spaces': 'Remove spaces from text before checking for regex matches.',
        'ignore-case': 'Ignore case when checking for regex matches.',
        'display-text': 'Display the person entries that had matches after test.',
    },
)
def regex_test(
    ctx,
    regex=None,
    books=None,
    hyphens=False,
    spaces=False,
    display_text=False,
    ignore_case=True,
):
    """
    Run an "extraction" test using regex and get information about
    what kind of strings the regex matched and the frequency of each
    match.
    """
    regex_ext_cmd = '"{}" -books {} {}'

    if not books:
        path_template = 'material/siirtokarjalaiset_{}.xml'
        book_suffices = ('I', 'II', 'III', 'IV')
        books = ' '.join([path_template.format(x) for x in book_suffices])

    flag_list = []
    if hyphens:
        flag_list.append('--hyphens')
    if spaces:
        flag_list.append('--spaces')
    if display_text:
        flag_list.append('--display-text')
    if ignore_case:
        flag_list.append('--ignore-case')

    flags = ' '.join(flag_list)
    regex_ext_cmd = regex_ext_cmd.format(regex, books, flags)
    ctx.run(
        'python analysis_toolkit/simple_regex_extractor.py {}'.format(regex_ext_cmd)
    )


@task()
def nlp_setup(ctx):
    """
    Downloads and installs the Finnish Dependency Parser.
    The base repository URL is https://github.com/TurkuNLP/Finnish-dep-parser
    We are using our own repository which contains fixes to make FDP work on Mac OS X.
    """
    branch_name = 'turkunlp-updates'
    repository_url = 'https://github.com/Learning-from-our-past/Finnish-dep-parser.git'
    fdp_dir = 'dependencies/fin-dep-parser'
    ctx.run(
        'git clone -b {} --depth=1 {} {}'.format(branch_name, repository_url, fdp_dir)
    )
    ctx.run('rm -rf {}/.git'.format(fdp_dir))
    ctx.run('rm -rf {}/.gitignore'.format(fdp_dir))
    ctx.run('cd {}; ./install.sh'.format(fdp_dir))
    print(
        'Please specify the Python 2 interpreter in {}/init.sh '
        'if it is not "python2".'.format(fdp_dir)
    )


@task(
    optional=['output_file', 'bookseries'],
    help={
        'input-file': 'The XML file to run through fin-dep-parser.',
        'output-file': 'The path and filename to output NLP-tagged data in.',
        'no-clean-up': 'Do not remove temporary intermediary files.',
        'bookseries': (
            'Run books of a specific series through NLP-tagging with'
            'default settings. If specified, input-file is ignored.'
        ),
    },
)
def generate_nlp_xmls(
    ctx, input_file=None, output_file=None, no_clean_up=False, bookseries=None
):
    """
    Runs the an XML file through the Finnish Dependency Parser and
    outputs XML file with NLP-tagged, CoNLLU-formatted data within.
    """
    if bookseries is not None and input_file is not None:
        print(
            'Error: Please do not specify both bookseries and input-file. Specifying '
            'bookseries means we load the default settings for that bookseries, '
            'including input-file(s).'
        )
        sys.exit(1)

    kaira_cmd_fmt = 'python main.py -t {} -o {}'
    input_files = []
    if bookseries:
        default_settings = {
            'siirtokarjalaiset': {
                'filename_template': 'material/siirtokarjalaiset_{}.{}',
                'book_numerals': ['I', 'II', 'III', 'IV'],
            }
        }

        if bookseries not in default_settings:
            print(
                'Error: No default settings for the specified bookseries. Try one of:'
                '\n\t{}'.format(default_settings.keys())
            )
            sys.exit(1)

        series_settings = default_settings[bookseries]
        input_files += [
            series_settings['filename_template'].format(book_num, 'xml')
            for book_num in series_settings['book_numerals']
        ]
    else:
        input_files.append(input_file)

    for in_file in input_files:
        out_file = output_file
        if out_file is None:
            out_file = '{}_with_conllu.xml'.format(os.path.splitext(in_file)[0])
        kaira_cmd = kaira_cmd_fmt.format(in_file, out_file)
        if no_clean_up:
            kaira_cmd = '{} {}'.format(kaira_cmd, '--no-clean-up')
        ctx.run(kaira_cmd)

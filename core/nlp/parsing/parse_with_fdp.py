import os


def parse_through_fdp_and_output_file(file_path, base_path):
    output_path = '{}_nlp_data.conllu'.format(base_path)
    with RunInFinDepDir() as path_to_project_root:
        file_path = os.path.join(path_to_project_root, file_path)
        relative_output_path = os.path.join(path_to_project_root, output_path)
        command_fmt = 'cat {} | ./split_text_with_comments.sh | ./parse_conll.sh > {}'
        os.system(command_fmt.format(file_path, relative_output_path))

    return output_path


class RunInFinDepDir:
    def __init__(self):
        self._origin_dir = os.getcwd()
        self._fin_dep_dir = 'dependencies/fin-dep-parser'

    def __enter__(self):
        """
        :return: Path to project root directory
        """
        os.chdir(self._fin_dep_dir)
        sep = os.path.sep
        return (self._fin_dep_dir.count(sep) + 1) * '..{}'.format(sep)

    def __exit__(self, *args):
        os.chdir(self._origin_dir)

import yaml
import importlib
from book_extractors.extraction_pipeline import ExtractionPipeline


def extractor_constructor(loader, node):
    """
    Define a custom PyYaml constructor to instantiate pipeline extractors. Imports
    classes and modules dynamically based on names and paths in yaml.
    """
    extractor_params = loader.construct_mapping(node, deep=True)

    extractor_module = importlib.import_module(extractor_params['module'])
    extractor_class = getattr(extractor_module, extractor_params['class_name'])

    cursor_location_dependence = extractor_params['cursor_location_depend_on'] if 'cursor_location_depend_on' in extractor_params else None
    options = extractor_params['options'] if 'options' in extractor_params else None
    extractor = extractor_class(cursor_location_dependence, options)

    if 'pipeline' in extractor_params:
        extractor.set_subpipeline(extractor_params['pipeline'])

    return extractor


yaml.add_constructor('!Extractor', extractor_constructor)


def parse_config(path):
    file = open(path)
    loaded = yaml.load(file)
    return loaded


def build_pipeline_from_yaml(yaml_path):
    config = parse_config(yaml_path)

    return ExtractionPipeline(config['pipeline'], True)


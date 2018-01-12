import yaml
from book_extractors.extraction_pipeline import ExtractionPipeline


def parse_config(path):
    file = open(path)
    loaded = yaml.load(file)
    return loaded


def build_pipeline_from_yaml(yaml_path):
    config = parse_config(yaml_path)

    return ExtractionPipeline(config['pipeline'], True)


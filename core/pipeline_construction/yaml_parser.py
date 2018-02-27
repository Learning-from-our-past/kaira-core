import yaml
import importlib
from core.pipeline_construction.extraction_pipeline import ExtractionPipeline


class YamlParser:

    def __init__(self, extraction_results_map):
        self._extraction_results_map = extraction_results_map
        yaml.add_constructor('!Extractor', self._extractor_constructor)

    def _extractor_constructor(self, loader, node):
        """
        Define a custom PyYaml constructor to instantiate pipeline extractors. Imports
        classes and modules dynamically based on names and paths in yaml.
        """
        extractor_params = loader.construct_mapping(node, deep=True)

        extractor_module = importlib.import_module(extractor_params['module'])
        extractor_class = getattr(extractor_module, extractor_params['class_name'])

        cursor_location_dependence = extractor_params['cursor_location_depend_on'] if 'cursor_location_depend_on' in \
                                                                                      extractor_params else None
        options = extractor_params['options'] if 'options' in extractor_params else None
        extractor = extractor_class(cursor_location_dependence, options)

        extractor.set_extraction_results_map(self._extraction_results_map)

        if 'depends_on' in extractor_params:
            extractor.set_required_dependencies(extractor_params['depends_on'])

        if 'pipeline' in extractor_params:
            extractor.set_subpipeline(extractor_params['pipeline'])

        return extractor

    def _parse_config(self, path):
        file = open(path)
        loaded = yaml.load(file)
        return loaded

    def _parse_config_from_string(self, config):
        loaded = yaml.load(config)
        return loaded

    def build_pipeline_from_yaml(self, yaml_path):
        config = self._parse_config(yaml_path)

        return ExtractionPipeline(config['pipeline'])

    def build_pipeline_from_yaml_string(self, yaml_string):
        config = self._parse_config_from_string(yaml_string)

        return ExtractionPipeline(config['pipeline'])

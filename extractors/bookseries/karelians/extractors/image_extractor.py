from extractors.common.extraction_keys import KEYS
from core.pipeline_construction.base_extractor import BaseExtractor

# FIXME: Rename this class to describe its purpose...
# FIXME: Do not save the data as group.
class ImageExtractor(BaseExtractor):
    extraction_key = 'personMetadata'

    def _extract(self, entry, extraction_results, extraction_metadata):
        image_path = None
        page = None
        try:
            image_path = entry["img_path"]
        except KeyError:
            pass

        try:
            page = entry["approximated_page"]
        except KeyError:
            pass

        return self._add_to_extraction_results(
            {
                KEYS["imagepath"]: image_path,
                KEYS["approximatePage"]: page,
                KEYS["originalText"]: entry['text'],
            },
            extraction_results,
            extraction_metadata,
        )

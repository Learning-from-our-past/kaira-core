from book_extractors.common.extraction_keys import KEYS
from book_extractors.common.extractors.base_extractor import BaseExtractor


class ImageExtractor(BaseExtractor):
    extraction_key = 'personMetadata'

    def extract(self, entry, extraction_results):
        image_path = ""
        page = ""
        try:
            image_path = entry["image_path"]
        except KeyError:
            pass

        try:
            page = entry["approximated_page"]
        except KeyError:
            pass

        return self._constructReturnDict({
            KEYS["imagepath"]: image_path,
            KEYS["approximatePage"]: page,
            KEYS["originalText"]: entry['text']
        }, extraction_results)

from book_extractors.common.base_extractor import BaseExtractor
from book_extractors.common.extraction_keys import KEYS


class ImageExtractor(BaseExtractor):

    def extract(self, entry, start_position=0):
        image_path = ""
        page = ""
        try:
            image_path = entry["image_path"]
        except KeyError as e:
            pass

        try:
            page = entry["approximated_page"]
        except KeyError as e:
            pass

        return self._constructReturnDict({
            KEYS["imagepath"]: image_path,
            KEYS["approximatePage"]: page,
            KEYS["originalText"]: entry['text']
        })

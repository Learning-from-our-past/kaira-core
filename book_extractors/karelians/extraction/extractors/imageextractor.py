from book_extractors.common.base_extractor import BaseExtractor
from book_extractors.common.extraction_keys import KEYS


class ImageExtractor(BaseExtractor):

    def extract(self, entry, start_position=0):
        self.image_path = ""
        self.page = ""
        try:
            self.image_path = entry["image_path"]
        except KeyError as e:
            pass

        try:
            self.page = entry["approximated_page"]
        except KeyError as e:
            pass
        return self._constructReturnDict()

    def _constructReturnDict(self):
        return {KEYS["imagepath"]: self.image_path, KEYS["approximatePage"]: self.page}

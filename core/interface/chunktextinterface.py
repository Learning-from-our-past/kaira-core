from abc import abstractmethod


class ChunkTextInterface:
    def __init__(self, bookseries_id):
        self._bookseries_id = bookseries_id

    @abstractmethod
    def chunk_text(self, text, destination_path, book_number):
        """
        :param text: Text from file to be processed
        :param destination_path:
        :return: Should return string of the xml-document
        """
        pass

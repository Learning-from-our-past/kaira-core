from abc import abstractmethod

class ChunkTextInterface():


    @abstractmethod
    def chunk_text(self, text, destination_path):
        """
        :param text: Text from file to be processed
        :param destination_path:
        :return: Should return string of the xml-document
        """
        pass
from abc import abstractmethod

class ChunkTextInterface():

    @abstractmethod
    def chunk_text(self, text):
        pass
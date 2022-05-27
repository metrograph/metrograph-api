from models.Files.AbstractFile import AbstractFile

class File(AbstractFile):

    def __init__(self, path: str, name: str):
        super().__init__(path, name)
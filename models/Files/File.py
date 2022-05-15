from models.Files.AbstractFile import AbstractFile

class File(AbstractFile):

    def __init__(self, uuid, name):
        super().__init__(uuid, name)
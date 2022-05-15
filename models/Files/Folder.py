from models.Files.AbstractFile import AbstractFile
from models.Files.File import File

class Folder(AbstractFile):

    def __init__(self, uuid, name):
        super().__init__(uuid, name)
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def print_tree(tree, level=0):
        print(("\t"*level)+"| ", end='')
        #print(tree.uuid +' - ', end='')
        print(tree.name)
        
        for element in tree.children:
            if type(element) is Folder:
                Folder.print_tree(element, level=level+1)
            else:
                print(("\t"*(level+1))+"| ", end='')
                #print(element.uuid + ' - ', end='')
                print(element.name)



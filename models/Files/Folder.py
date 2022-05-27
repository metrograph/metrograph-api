from models.Files.AbstractFile import AbstractFile
from models.Files.File import File

class Folder(AbstractFile):

    def __init__(self, path: str, name: str):
        super().__init__(path, name)
        self.children = []

    def add_child(self, child):
        if type(child) is Folder:
            self.children.insert(0, child)
        else:
            self.children.append(child)

    def print_tree(tree, level=0):
        print(("\t"*level)+"| ", end='')
        print(tree.name)
        
        for element in tree.children:
            if type(element) is Folder:
                Folder.print_tree(element, level=level+1)
            else:
                print(("\t"*(level+1))+"| ", end='')
                print(element.name)
    
    def get_json_tree(tree):
        json_children = [] 
        for element in tree.children:
            if type(element) is Folder:
                json_children.append(Folder.get_json_tree(element))
            else:
                json_children.append({
                    'path': element.path,
                    'name': element.name
                })
        
        return {
            'path': tree.path,
            'name': tree.name,
            'children': json_children
        }



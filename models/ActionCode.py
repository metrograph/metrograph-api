from distutils.dir_util import copy_tree
from models.Files import Folder
from models.Files import File
from os import listdir
from os.path import isdir
from uuid import uuid4

class ActionCode:

    def __init__(self):
        pass

    def create_action_code_tree(tree, path):
        for element in listdir(path):
            element_path = f'{path}/{element}'
            element_uuid = str(uuid4())
            if isdir(element_path):
                child_folder = Folder(uuid=element_uuid, name=element)
                ActionCode.create_action_code_tree(child_folder, element_path)
                tree.add_child(child_folder)
            else:
                tree.add_child(File(uuid=element_uuid, name=element))

    
    def create_new(uuid, runtime, runtime_version):
        template_path = f'/home/metrograph/templates/{runtime}_{runtime_version}'
        action_path = f'/home/metrograph/actions/{uuid}'
        copy_tree(template_path, action_path)
        tree = Folder(uuid=uuid, name="root")
        ActionCode.create_action_code_tree(tree, action_path)
        return tree

        

        


from distutils.dir_util import copy_tree
from pathlib import Path
from models.Files import Folder
from models.Files import File
from os import listdir, mkdir
from os.path import isdir, exists
from uuid import uuid4
from shutil import rmtree

class ActionCode:

    TEMPLATES_PATH = '/home/metrograph/templates'
    ACTIONS_PATH = '/home/metrograph/actions'


    def __init__(self):
        pass

    def exists(uuid):
        actioncode_path = f'{ActionCode.ACTIONS_PATH}/{uuid}'
        return exists(actioncode_path)

    def get_by_uuid(uuid) -> Folder:
        actioncode_path = f'{ActionCode.ACTIONS_PATH}/{uuid}'
        if exists(f'{actioncode_path}'):
            tree = Folder(path=f"/{uuid}", name=uuid)
            ActionCode.create_action_code_tree(tree)
            return tree
        else:
            return None

    def create_action_code_tree(tree: Folder) -> None:
        for element in listdir(ActionCode.ACTIONS_PATH+tree.path):
            relative_path = f'{tree.path}/{element}'
            absolute_path = f'{ActionCode.ACTIONS_PATH}/{tree.path}/{element}'
            if isdir(absolute_path):
                child_folder = Folder(path=relative_path, name=element)
                ActionCode.create_action_code_tree(child_folder)
                tree.add_child(child_folder)
            else:
                tree.add_child(File(path=relative_path, name=element))

    def create_new(uuid, runtime, runtime_version) -> Folder:
        template_path = f'{ActionCode.TEMPLATES_PATH}/{runtime}_{runtime_version}'
        action_path = f'{ActionCode.ACTIONS_PATH}/{uuid}'
        copy_tree(template_path, action_path)
        tree = Folder(path=f"/{uuid}", name=uuid)
        ActionCode.create_action_code_tree(tree)
        return tree

    # Files editing methods

    def create_file(path: str):
        absolute_path = f'{ActionCode.ACTIONS_PATH+path}'
        if not exists(absolute_path):
            Path(absolute_path).touch()
            return True
        else:
            return False

    def create_folder(path: str):
        absolute_path = f'{ActionCode.ACTIONS_PATH+path}'
        if not exists(absolute_path):
            Path(absolute_path).mkdir()
            return True
        else:
            return False

    def rename_file(path: str, new_name:str):
        absolute_path = f'{ActionCode.ACTIONS_PATH+path}'
        file = Path(absolute_path)
        if file.exists():
            file.rename(Path(file.parent, new_name))
            return True
        else:
            return False

    def rename_folder(path: str, new_name:str):
        absolute_path = f'{ActionCode.ACTIONS_PATH+path}'
        folder = Path(absolute_path)
        if folder.exists():
            folder.rename(Path(folder.parent, new_name))
            return True
        else:
            return False

    def delete_file(path: str):
        absolute_path = f'{ActionCode.ACTIONS_PATH+path}'
        if exists(absolute_path):
            Path(absolute_path).unlink()
            return True
        else:
            return False

    def delete_folder(path: str):
        absolute_path = f'{ActionCode.ACTIONS_PATH+path}'
        if exists(absolute_path):
            rmtree(absolute_path)
            return True
        else:
            return False

    def update_file(action_uuid:str, path: str):
        pass
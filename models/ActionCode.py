from sanic import Sanic
from distutils.dir_util import copy_tree
from pathlib import Path
from models.Files import Folder
from models.Files import File
from os import listdir, mkdir
from os.path import isdir, exists
from uuid import uuid4
from shutil import rmtree

class ActionCode:

    #TEMPLATES_PATH = Sanic.get_app().config.HOME+'/templates'
    TEMPLATES_PATH = '/home/metrograph/templates'
    ACTIONS_PATH = Sanic.get_app().config.HOME+'/actions'


    def __init__(self):
        pass

    def action_path(uuid) -> str:
        return f'{ActionCode.ACTIONS_PATH}/{uuid}/action'

    def project_path(uuid) -> str:
        return f'{ActionCode.ACTIONS_PATH}/{uuid}'

    def exists(uuid):
        actioncode_path = f'{ActionCode.action_path(uuid)}'
        return exists(actioncode_path)

    def get_by_uuid(uuid) -> Folder:
        if exists(f'{ActionCode.action_path(uuid)}'):
            tree = Folder(path=f"/", name="root")
            ActionCode.create_action_code_tree(uuid, tree, isroot=True)
            return tree
        else:
            return None

    def create_action_code_tree(uuid: str, tree: Folder, isroot=False) -> None:
        for element in listdir(f'{ActionCode.action_path(uuid)}{tree.path}'):
            relative_path = f'{tree.path}{element}' if isroot else f'{tree.path}/{element}'
            absolute_path = f'{ActionCode.action_path(uuid)}/{element}' if isroot else f'{ActionCode.action_path(uuid)}{tree.path}/{element}'
            if isdir(absolute_path):
                child_folder = Folder(path=relative_path, name=element)
                ActionCode.create_action_code_tree(uuid, child_folder)
                tree.add_child(child_folder)
            else:
                tree.add_child(File(path=relative_path, name=element))

    def create_new(uuid, runtime, runtime_version) -> Folder:
        template_path = f'{ActionCode.TEMPLATES_PATH}/{runtime}_{runtime_version}'
        action_path = f'{ActionCode.ACTIONS_PATH}/{uuid}'
        copy_tree(template_path, action_path)
        tree = Folder(path=f"/", name="root")
        ActionCode.create_action_code_tree(uuid, tree)
        return tree

    # Files editing methods

    def create_file(uuid, path: str):
        absolute_path = f'{ActionCode.action_path(uuid)}{path}'
        if not exists(absolute_path):
            Path(absolute_path).touch()
            return True
        else:
            return False

    def create_folder(uuid, path: str):
        absolute_path = f'{ActionCode.action_path(uuid)}{path}'
        if not exists(absolute_path):
            Path(absolute_path).mkdir()
            return True
        else:
            return False

    def rename_file(uuid: str, path: str, new_name:str):
        absolute_path = f'{ActionCode.action_path(uuid)+path}'
        file = Path(absolute_path)
        if file.exists():
            file.rename(Path(file.parent, new_name))
            return True
        else:
            return False

    def rename_folder(uuid: str, path: str, new_name:str):
        absolute_path = f'{ActionCode.action_path(uuid)+path}'
        folder = Path(absolute_path)
        if folder.exists():
            folder.rename(Path(folder.parent, new_name))
            return True
        else:
            return False

    def delete_file(uuid: str, path: str):
        absolute_path = f'{ActionCode.action_path(uuid)+path}'
        if exists(absolute_path):
            Path(absolute_path).unlink()
            return True
        else:
            return False

    def delete_folder(uuid: str, path: str):
        absolute_path = f'{ActionCode.action_path(uuid)+path}'
        if exists(absolute_path):
            rmtree(absolute_path)
            return True
        else:
            return False

    def update_file(uuid: str, path: str, new_content:str):
        absolute_path = f'{ActionCode.action_path(uuid)+path}'
        if exists(absolute_path):
            with open(absolute_path, 'w') as f:
                f.write(new_content)
                return True
        else:
            return False

    def delete(uuid:str):
        absolute_path = f'{ActionCode.project_path(uuid)}'
        if exists(absolute_path):
            rmtree(absolute_path)
            return True
        else:
            return False
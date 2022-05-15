from distutils.dir_util import copy_tree


class ActionCode:

    def __init__(self):
        pass

    def get_path_tree(self):
        return None
    
    def create_new(uuid, runtime, runtime_version):
        template_path = "/home/metrograph/templates/python_3.9.10"
        action_path = "/home/metrograph/actions/3264789-132-145"
        copy_tree(template_path, action_path)

        

        


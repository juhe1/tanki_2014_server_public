from loaders.client_resource_loader import client_resource_loader
from utils.log import console_out

class ResourceLoader:
    def __init__(self, client_object):
        self.client_object = client_object
        self.loaded_resources = []

    def load_resource(self, path, version=None, language="en"):
        key = (path, version, language)

        if key in self.loaded_resources:
            return

        resource_objects = client_resource_loader.get_resource_objects(path, version, language)
        for resource_object in resource_objects:
            self.client_object.basic_commands.load_dependencies([resource_object])
            self.client_object.handle_basic_command.recive_dependencies_loaded_command()

        self.loaded_resources.append(key)

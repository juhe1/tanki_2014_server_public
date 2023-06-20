from client.layouts.battle.models.battle_map_model import battle_map_model_data
from client.space.model import Model

from xml.dom import minidom

class BattleMapModel(Model):
    model_id = 300100005

    def __init__(self, game_object, client_space, client_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

        self.load_map_resources(global_model.map_info)

        self.model_data = battle_map_model_data.BattleMapModelData(game_object, client_object, global_model.get_model_data())
        self.commands = None
        self.command_handler = None

    def load_map_resources(self, map_info):
        # load all librarys for the map
        dom = minidom.parse("client_resources" + map_info.map_resource_path + "/1/proplibs.xml")
        proplib_elements = dom.getElementsByTagName('library')

        for proplib_element in proplib_elements:
            resource_path = proplib_element.attributes['resource-id'].value
            self.client_object.resource_loader.load_resource(resource_path[1:], language=self.client_object.language)

        # load map resource
        self.client_object.resource_loader.load_resource(map_info.map_resource_path[1:], language=self.client_object.language)

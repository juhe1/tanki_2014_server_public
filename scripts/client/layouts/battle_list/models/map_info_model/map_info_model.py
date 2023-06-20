from client.layouts.battle_list.models.map_info_model import map_info_model_data
from client.space.model import Model

class MapInfoModel(Model):
    model_id = 300090019

    def __init__(self, game_object, client_space, client_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)
        self.model_data = map_info_model_data.MapInfoModelData(game_object, client_object, global_model.get_model_data())
        self.commands = None
        self.command_handler = None

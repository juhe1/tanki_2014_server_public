from client.layouts.battle_list.models.map_info_model import map_info_model
from space.global_model import GlobalModel
from . import map_info_model_cc

class MapInfoGlobalModel(GlobalModel):

    CLIENT_MODEL = map_info_model.MapInfoModel

    def __init__(self, global_game_object, global_space, map_info_model_cc, owner_id=None):
        super().__init__(global_game_object, global_space, owner_id)
        self.map_info_model_cc = map_info_model_cc

    def get_model_data(self):
        return self.map_info_model_cc

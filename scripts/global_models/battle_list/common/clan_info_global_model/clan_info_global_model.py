from client.layouts.battle_list.models.clan_info_model import clan_info_model
from space.global_model import GlobalModel
from . import clan_info_model_cc

class ClanInfoGlobalModel(GlobalModel):

    CLIENT_MODEL = clan_info_model.ClanInfoModel

    def __init__(self, global_game_object, global_space, clan_info_model_cc, owner_id=None):
        super().__init__(global_game_object, global_space, owner_id)
        self.clan_info_model_cc = clan_info_model_cc

    def get_model_data(self):
        return self.clan_info_model_cc

from client.layouts.battle_list.models.battle_dm_info_model import battle_dm_info_model
from space.global_model import GlobalModel
from . import battle_dm_info_model_cc

class BattleDmInfoGlobalModel(GlobalModel):

    CLIENT_MODEL = battle_dm_info_model.BattleDmInfoModel

    def __init__(self, global_game_object, global_space, battle_item_global_model, owner_id=None):
        super().__init__(global_game_object, global_space, owner_id)

        self.battle_item_global_model = battle_item_global_model
        self.user_infos = {}

    def get_battle_field_global_space(self):
        return self.battle_item_global_model.battle_field_global_space

    def get_user_ids(self):
        return [user_info.user_id for user_info in self.user_infos.values()]

    def update_user_score(self, user_info):
        self.broadcast_command("update_user_kills", (user_info,))

    def add_user(self, user_info, team):
        self.user_infos[user_info.user_id] = user_info
        self.broadcast_command("add_user", (user_info,))

    def remove_user(self, user_id):
        del self.user_infos[user_id]

    def get_model_data(self):
        _battle_dm_info_model_cc = battle_dm_info_model_cc.BattleDmInfoModelCC()
        _battle_dm_info_model_cc.user_infos = self.user_infos.values()
        return _battle_dm_info_model_cc

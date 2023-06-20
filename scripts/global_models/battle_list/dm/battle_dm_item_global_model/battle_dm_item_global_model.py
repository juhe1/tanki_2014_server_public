from client.layouts.battle_list.models.battle_dm_item_model import battle_dm_item_model
from space.global_model import GlobalModel
from . import battle_dm_item_model_cc

class BattleDmItemGlobalModel(GlobalModel):

    CLIENT_MODEL = battle_dm_item_model.BattleDmItemModel

    def __init__(self, global_game_object, global_space, battle_dm_info_global_model, owner_id=None):
        super().__init__(global_game_object, global_space, owner_id)
        self.battle_dm_info_global_model = battle_dm_info_global_model

    def get_model_data(self):
        _battle_dm_item_model_cc = battle_dm_item_model_cc.BattleDmItemModelCC()
        _battle_dm_item_model_cc.user_ids = self.battle_dm_info_global_model.get_user_ids()
        return _battle_dm_item_model_cc

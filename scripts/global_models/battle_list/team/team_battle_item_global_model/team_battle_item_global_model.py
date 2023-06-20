from client.layouts.battle_list.models.team_battle_item_model import team_battle_item_model
from global_models.battle.common.tank_global_model.team import Team
from space.global_model import GlobalModel
from . import team_battle_item_model_cc

class TeamBattleItemGlobalModel(GlobalModel):

    CLIENT_MODEL = team_battle_item_model.TeamBattleItemModel

    def __init__(self, global_game_object, global_space, team_battle_info_global_model, owner_id=None):
        super().__init__(global_game_object, global_space, owner_id)

        self.team_battle_info_global_model = team_battle_info_global_model
        self.team_battle_item_model_cc = team_battle_item_model_cc.TeamBattleItemModelCC()

    def get_model_data(self):
        self.team_battle_item_model_cc.blue_user_ids = self.team_battle_info_global_model.get_user_ids(Team.BLUE)
        self.team_battle_item_model_cc.red_user_ids = self.team_battle_info_global_model.get_user_ids(Team.RED)
        return self.team_battle_item_model_cc

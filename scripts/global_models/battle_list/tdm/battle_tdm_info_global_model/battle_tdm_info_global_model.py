from global_models.battle_list.team.team_battle_info_global_model import team_battle_info_global_model

class BattleTdmInfoGlobalModel(team_battle_info_global_model.TeamBattleInfoGlobalModel):
    def __init__(self, global_game_object, global_space, battle_item_global_model, battle_data, owner_id=None):
        super().__init__(global_game_object, global_space, battle_item_global_model, battle_data, owner_id)

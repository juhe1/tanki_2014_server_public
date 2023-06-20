from global_models.battle_list.team.team_battle_item_global_model import team_battle_item_global_model

class BattleTdmItemGlobalModel(team_battle_item_global_model.TeamBattleItemGlobalModel):

    def __init__(self, global_game_object, global_space, battle_tdm_info_global_model, owner_id=None):
        super().__init__(global_game_object, global_space, battle_tdm_info_global_model, owner_id)

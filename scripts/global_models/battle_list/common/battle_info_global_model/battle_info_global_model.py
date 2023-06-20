from global_models.battle_list.dm.battle_dm_info_global_model import battle_dm_info_global_model
from global_models.battle_list.team.team_battle_info_global_model import team_battle_info_global_model
from global_models.battle_list.dm.battle_dm_item_global_model import battle_dm_item_global_model
from global_models.battle_list.team.team_battle_item_global_model import team_battle_item_global_model
from global_models.lobby.rank_notifier_global_model import rank_notifier_global_model
from global_models.lobby.uid_notifier_global_model import uid_notifier_global_model
from client.layouts.battle_list.models.battle_info_model import battle_info_model
from global_models.battle.common.statistics_global_model import statistics_global_model
from client.layouts.battle_list.battle_data.battle_mode import BattleMode
from space.global_model import GlobalModel
from space import global_space_registry

class BattleInfoGlobalModel(GlobalModel):

    CLIENT_MODEL = battle_info_model.BattleInfoModel

    def __init__(self, global_game_object, global_space, battle_info_model_cc, battle_item_global_model, owner_id=None):
        super().__init__(global_game_object, global_space, owner_id)

        self.battle_info_model_cc = battle_info_model_cc
        self.battle_item_global_model = battle_item_global_model
        self.statistics_global_model = None

        self.battle_mode_specifig_info_global_model = self.get_battle_mode_specifig_info_global_model(self.battle_info_model_cc.battle_mode)
        self.battle_mode_specifig_item_global_model = self.get_battle_mode_specifig_item_global_model(self.battle_info_model_cc.battle_mode)

    def get_model_data(self):
        if self.statistics_global_model == None:
            self.statistics_global_model = self.battle_item_global_model.battle_field_global_space.get_global_model(statistics_global_model.StatisticsGlobalModel, global_game_object_name="default_game_object")

        self.battle_info_model_cc.round_started = self.statistics_global_model.round_started
        self.battle_info_model_cc.time_left_in_seconds = self.statistics_global_model.get_time_left_in_seconds()
        return self.battle_info_model_cc

    def get_battle_mode_specifig_info_global_model(self, battle_mode):
        if battle_mode == BattleMode.DM:
            return self.global_game_object.get_global_model(battle_dm_info_global_model.BattleDmInfoGlobalModel)

        if battle_mode.is_team_battle():
            return self.global_game_object.get_global_model(team_battle_info_global_model.TeamBattleInfoGlobalModel)

    def get_battle_mode_specifig_item_global_model(self, battle_mode):
        if battle_mode == BattleMode.DM:
            return self.battle_item_global_model.global_game_object.get_global_model(battle_dm_item_global_model.BattleDmItemGlobalModel)

        if battle_mode.is_team_battle():
            return self.battle_item_global_model.global_game_object.get_global_model(team_battle_item_global_model.TeamBattleItemGlobalModel)

    def add_user_to_notifiers(self, user_info):
        _uid_notifier_global_model = global_space_registry.get_global_model(uid_notifier_global_model.UidNotifierGlobalModel, global_space_name="lobby", global_game_object_name="panel")
        _uid_notifier_global_model.add_uid(user_info)

        _rank_notifier_global_model = global_space_registry.get_global_model(rank_notifier_global_model.RankNotifierGlobalModel, global_space_name="lobby", global_game_object_name="panel")
        _rank_notifier_global_model.add_rank(user_info)

    def swap_teams(self):
        self.battle_mode_specifig_info_global_model.swap_teams()
        self.battle_mode_specifig_item_global_model.broadcast_command("swap_teams", ())

    def set_team_score(self, team, score):
        self.battle_mode_specifig_info_global_model.set_team_score(team, score)

    def set_team_score_from_server(self, team, score):
        self.battle_mode_specifig_info_global_model.set_team_score_from_server(team, score)

    def update_user_score(self, killer_user_info):
        self.battle_mode_specifig_info_global_model.update_user_score(killer_user_info)

    def add_team_score(self, team, score):
        self.battle_mode_specifig_info_global_model.add_team_score(team, score)

    def add_user(self, user_info, team=None):
        self.add_user_to_notifiers(user_info)

        self.battle_mode_specifig_info_global_model.add_user(user_info, team)
        self.battle_mode_specifig_item_global_model.broadcast_command("reserve_slot", (user_info.user_id, team))

    def remove_user(self, user_id):
        self.battle_mode_specifig_info_global_model.remove_user(user_id)
        self.battle_mode_specifig_item_global_model.broadcast_command("release_slot", (user_id,))

        self.broadcast_command("remove_user", (user_id,))

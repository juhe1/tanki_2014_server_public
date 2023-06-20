from global_models.battle.common.battle_field_global_model import battle_field_global_model
from global_models.battle.common.statistics_global_model import battle_fund_calculator
from client.layouts.battle.models.statistics_dm_model import statistics_dm_model
from space.global_model import GlobalModel
from . import statistics_dm_model_cc

class StatisticsDmGlobalModel(GlobalModel):

    CLIENT_MODEL = statistics_dm_model.StatisticsDmModel

    def __init__(self, global_game_object, global_space, owner_id=None):
        super().__init__(global_game_object, global_space, owner_id)
        self.battle_field_global_model = global_game_object.get_global_model(battle_field_global_model.BattleFieldGlobalModel)

        self.user_infos = {}

    def share_fund(self, fund):
        user_infos = self.battle_field_global_model.get_all_user_infos()
        battle_fund_calculator.share_battle_fund_between_tanks(user_infos, fund)

    def get_user_infos(self):
        return list(self.user_infos.values())

    def add_user(self, user_info, team):
        self.user_infos[user_info.user_id] = user_info
        self.broadcast_command("user_connected", (user_info.user_id, self.get_user_infos()))

    def remove_user(self, user_id):
        del self.user_infos[user_id]
        self.broadcast_command("user_disconnected", (user_id,))

    def get_model_data(self):
        _statistics_dm_model_cc = statistics_dm_model_cc.StatisticsDmModelCC()
        _statistics_dm_model_cc.user_infos = self.get_user_infos()
        return _statistics_dm_model_cc

    def change_user_stats(self, user_info, team):
        self.broadcast_command("change_user_stat", (user_info,))

    def refresh_user_stat(self):
        self.broadcast_command("refresh_user_stat", (self.get_user_infos(),))


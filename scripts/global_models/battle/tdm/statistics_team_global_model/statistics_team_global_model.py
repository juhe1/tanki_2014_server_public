from global_models.battle.common.battle_field_global_model import battle_field_global_model
from global_models.battle.common.statistics_global_model import battle_fund_calculator
from client.layouts.battle.models.statistics_team_model import statistics_team_model
from global_models.battle.common.tank_global_model.team import Team
from space.global_model import GlobalModel
from . import statistics_team_model_cc
from database import battles_table

class StatisticsTeamGlobalModel(GlobalModel):

    CLIENT_MODEL = statistics_team_model.StatisticsTeamModel

    def __init__(self, global_game_object, global_space, owner_id=None):
        super().__init__(global_game_object, global_space, owner_id)

        self.battle_field_global_model = global_game_object.get_global_model(battle_field_global_model.BattleFieldGlobalModel)
        self.statistics_team_model_cc = statistics_team_model_cc.StatisticsTeamModelCC()

        self.battle_info_global_model = self.battle_field_global_model.battle_info_global_model
        self.battle_info_model_cc = self.battle_info_global_model.battle_info_model_cc

        self.score_blue = 0
        self.score_red = 0
        self.blue_user_infos = {}
        self.red_user_infos = {}

    def share_fund(self, fund):
        blue_fund, red_fund = battle_fund_calculator.calculate_blue_and_red_fund(self.score_blue, self.score_red, fund)

        battle_fund_calculator.share_battle_fund_between_tanks(self.battle_field_global_model.get_team_user_infos(Team.BLUE), blue_fund)
        battle_fund_calculator.share_battle_fund_between_tanks(self.battle_field_global_model.get_team_user_infos(Team.RED), red_fund)

    def swap_teams(self):
        temp = self.blue_user_infos
        self.blue_user_infos = self.red_user_infos
        self.red_user_infos = temp
        self.broadcast_command("swap_team", (list(self.red_user_infos.values()), list(self.blue_user_infos.values())))

    def get_team_user_infos_by_user_id(self, user_id):
        if user_id in self.blue_user_infos:
            return self.blue_user_infos
        return self.red_user_infos

    def get_team_user_infos(self, team):
        if team == Team.BLUE:
            return self.blue_user_infos
        return self.red_user_infos

    def add_team_score(self, team, score):
        if team == Team.BLUE:
            self.score_blue += score
            team_score = self.score_blue
            battles_table.set_score_team1(team_score, self.battle_info_model_cc.battle_id)
        else:
            self.score_red += score
            team_score = self.score_red
            battles_table.set_score_team2(team_score, self.battle_info_model_cc.battle_id)

        self.broadcast_command("change_team_score", (team, team_score))

    def set_team_score(self, team, score):
        if team == Team.BLUE:
            self.score_blue = score
            team_score = self.score_blue
            battles_table.set_score_team1(team_score, self.battle_info_model_cc.battle_id)
        else:
            self.score_red = score
            team_score = self.score_red
            battles_table.set_score_team2(team_score, self.battle_info_model_cc.battle_id)

        self.broadcast_command("change_team_score", (team, team_score))

    def set_team_score_from_server(self, team, score):
        if team == Team.BLUE:
            self.score_blue = score
            return

        self.score_red = score

    def add_user(self, user_info, team):
        self.get_team_user_infos(team)[user_info.user_id] = user_info
        self.broadcast_command("user_connect", (user_info.user_id, list(self.get_team_user_infos(team).values()), team))

    def remove_user(self, user_id):
        self.get_team_user_infos_by_user_id(user_id).pop(user_id)
        self.broadcast_command("user_disconnect", (user_id,))

    def get_model_data(self):
        self.statistics_team_model_cc.score_blue = self.score_blue
        self.statistics_team_model_cc.score_red = self.score_red
        self.statistics_team_model_cc.blue_user_infos = list(self.blue_user_infos.values())
        self.statistics_team_model_cc.red_user_infos = list(self.red_user_infos.values())
        return self.statistics_team_model_cc

    def change_user_stats(self, user_info):
        team = Team.RED

        if user_info.user_id in self.blue_user_infos:
            team = Team.BLUE

        self.broadcast_command("change_user_stat", (user_info, team))

    def refresh_user_stat(self):
        self.broadcast_command("refresh_user_stat", (list(self.blue_user_infos.values()), Team.BLUE))
        self.broadcast_command("refresh_user_stat", (list(self.red_user_infos.values()), Team.RED))

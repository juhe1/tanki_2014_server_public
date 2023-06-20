from client.layouts.battle_list.models.team_battle_info_model import team_battle_info_model
from global_models.battle.common.tank_global_model.team import Team
from space.global_model import GlobalModel
from . import team_battle_info_model_cc

class TeamBattleInfoGlobalModel(GlobalModel):

    CLIENT_MODEL = team_battle_info_model.TeamBattleInfoModel

    def __init__(self, global_game_object, global_space, battle_item_global_model, battle_data, owner_id=None):
        super().__init__(global_game_object, global_space, owner_id)

        self.battle_item_global_model = battle_item_global_model
        self.battle_data = battle_data
        self.team_battle_info_model_cc = self.create_cc()

        self.blue_user_infos = {}
        self.red_user_infos = {}
        self.red_score = 0
        self.blue_score = 0
    
    def create_cc(self):
        cc = team_battle_info_model_cc.TeamBattleInfoModelCC()
        cc.auto_balance = self.battle_data.auto_balance
        cc.friendly_fire = self.battle_data.friendly_fire
        return cc

    def get_team_user_infos(self, team):
        if team == Team.RED:
            return self.red_user_infos

        return self.blue_user_infos

    def swap_teams(self):
        temp = self.blue_user_infos
        self.blue_user_infos = self.red_user_infos
        self.red_user_infos = temp
        self.broadcast_command("swap_teams", ())
    
    def set_team_score_from_server(self, team, score):
        if team == Team.RED:
            self.red_score += score
            return
        self.blue_score += score

    def set_team_score(self, team, score):
        if team == Team.RED:
            self.red_score = score
            team_score = self.red_score
        else:
            self.blue_score = score
            team_score = self.blue_score

        self.broadcast_command("update_team_score", (team_score, team))

    def add_team_score(self, team, score):
        if team == Team.RED:
            self.red_score += score
            team_score = self.red_score
        else:
            self.blue_score += score
            team_score = self.blue_score

        self.broadcast_command("update_team_score", (team_score, team))

    def update_user_score(self, user_info):
        self.broadcast_command("update_user_score", (user_info.user_id, user_info.score))

    def get_battle_field_global_space(self):
        return self.battle_item_global_model.battle_field_global_space

    def get_user_ids(self, team):
        return list(self.get_team_user_infos(team).keys())

    def add_user(self, user_info, team):
        self.get_team_user_infos(team)[user_info.user_id] = user_info
        self.broadcast_command("add_user", (user_info, team))

    def remove_user(self, user_id):
        if user_id in self.blue_user_infos:
            self.blue_user_infos.pop(user_id)
            return

        self.red_user_infos.pop(user_id)

    def get_model_data(self):
        self.team_battle_info_model_cc.blue_user_infos = list(self.blue_user_infos.values())
        self.team_battle_info_model_cc.red_user_infos = list(self.red_user_infos.values())
        self.team_battle_info_model_cc.blue_score = self.blue_score
        self.team_battle_info_model_cc.red_score = self.red_score
        return self.team_battle_info_model_cc

from global_models.battle.bonus.battle_field_bonus_global_model import battle_field_bonus_global_model
from global_models.battle_list.common.battle_select_global_model import battle_select_global_model
from global_models.battle.mine.battle_mines_global_model import battle_mines_global_model
from global_models.battle.common.battle_field_global_model import battle_field_global_model
from global_models.battle.dm.statistics_dm_global_model import statistics_dm_global_model
from global_models.battle.tdm.statistics_team_global_model import statistics_team_global_model
from client.layouts.lobby.models.user_property_model import user_property_model
from client.layouts.battle.models.statistics_model import statistics_model
from client.layouts.battle_list.battle_data.battle_mode import BattleMode
from global_models.battle.common.tank_global_model.team import Team
from space.global_model import GlobalModel
from database import user_propertyes_table
from database import battle_users_table
from database import battles_table
from . import statistics_model_cc
from utils.time import timer

import server_properties
import threading
import datetime

class StatisticsGlobalModel(GlobalModel):

    CLIENT_MODEL = statistics_model.StatisticsModel

    def __init__(self, global_game_object, global_space, owner_id=None):
        super().__init__(global_game_object, global_space, owner_id)

        self.battle_field_global_model = global_game_object.get_global_model(battle_field_global_model.BattleFieldGlobalModel)
        self.battle_field_bonus_global_model = global_game_object.get_global_model(battle_field_bonus_global_model.BattleFieldBonusGlobalModel)
        self.battle_mines_global_model = global_game_object.get_global_model(battle_mines_global_model.BattleMinesGlobalModel)
        self.battle_info_global_model = self.battle_field_global_model.battle_info_global_model
        battle_select_global_space = self.battle_info_global_model.global_space
        self.battle_select_global_model = battle_select_global_space.get_global_model(battle_select_global_model.BattleSelectGlobalModel, global_game_object_name="default_game_object")
        self.battle_info_model_cc = self.battle_info_global_model.battle_info_model_cc
        self.battle_mode = self.battle_info_model_cc.battle_mode

        self.statistics_model_cc = self.create_cc()
        self.fund = 100
        self.round_started = True

        self.battle_timer = None
        time_limit_in_sec = self.battle_info_model_cc.limits.time_limit_in_sec

        if not time_limit_in_sec == 0:
            self.set_time(time_limit_in_sec)

        self.statistics_dm_global_model = global_game_object.get_global_model(statistics_dm_global_model.StatisticsDmGlobalModel)
        self.statistics_team_global_model = global_game_object.get_global_model(statistics_team_global_model.StatisticsTeamGlobalModel)
        self.battle_mode_specifig_statistic_global_model = self.get_battle_mode_specifig_statistic_global_model()

    def get_battle_mode_specifig_statistic_global_model(self):
        if self.battle_mode == BattleMode.DM:
            return self.statistics_dm_global_model

        if self.battle_mode in [BattleMode.TDM, BattleMode.CTF, BattleMode.CP]:
            return self.statistics_team_global_model

    def set_time(self, time):
        if self.battle_timer:
            self.battle_timer.destroy()

        self.battle_timer = timer.Timer(time)
        self.battle_timer.add_event_listener(self.battle_end)
        self.battle_timer.start()

    def set_fund(self, fund):
        self.fund = fund

    def add_fund(self, fund):
        if fund <= 0: return
        self.fund += fund
        battles_table.set_fund(self.fund, self.battle_info_model_cc.battle_id)
        self.battle_field_bonus_global_model.battle_fund_changed()
        self.broadcast_command("fund_change", (self.fund,))
        # TODO: send fund update command to clients

    def give_fund_to_active_user(self, client_object, user_info):
        _user_property_model = client_object.client_space_registry.get_model(user_property_model.UserPropertyModel, game_object_name="panel", space_name="lobby")
        _user_property_model.add_crystals(user_info.fund)
        _user_property_model.save_score_buffer()

    def give_fund_to_nonactive_user(self, user_info):
        user_propertyes_table.add_crystals(user_info.fund, user_info.user_id)

    def give_fund_to_users(self):
        user_infos = self.battle_field_global_model.get_all_user_infos()

        for user_info in user_infos:
            client_object = self.battle_field_global_model.get_client_objects_by_user_id(user_info.user_id)

            if client_object != None:
                self.give_fund_to_active_user(client_object, user_info)
                continue

            self.give_fund_to_nonactive_user(user_info)

    def add_user(self, user_info, team):
        self.battle_mode_specifig_statistic_global_model.add_user(user_info, team)

    def remove_user(self, user_id):
        self.battle_mode_specifig_statistic_global_model.remove_user(user_id)

    def set_team_score_from_server(self, team, score):
        self.battle_mode_specifig_statistic_global_model.set_team_score_from_server(team, score)

    def add_kill(self, killer_user_info, killer_team, target_user_info):
        killer_user_info.kills += 1
        killer_user_info.score += server_properties.KILL_SCORE
        target_user_info.deaths += 1

        self.battle_mode_specifig_statistic_global_model.change_user_stats(killer_user_info, killer_team)
        self.battle_mode_specifig_statistic_global_model.change_user_stats(target_user_info, killer_team)

        self.add_fund(server_properties.KILL_FUND)

        score_limit = self.battle_info_model_cc.limits.score_limit

        if self.battle_mode.is_team_battle():
            self.battle_mode_specifig_statistic_global_model.add_team_score(killer_team, 1)

        if self.battle_mode == BattleMode.DM and score_limit != 0:
            if killer_user_info.kills >= self.battle_info_model_cc.limits.score_limit:
                self.battle_end()

    def remove_mines(self, user_infos):
        for user_info in user_infos:
            self.battle_mines_global_model.remove_user_mines(user_info.user_id)

    def swap_every_tank_team(self):
        for tank_global_model in self.battle_field_global_model.get_all_tank_global_models():
            if tank_global_model == None: return
            tank_global_model.swap_teams()

    def battle_end(self):
        user_infos = self.battle_field_global_model.get_all_user_infos()
        self.round_started = False
        self.battle_field_bonus_global_model.remove_all_bonuses()
        self.remove_mines(user_infos)
        self.battle_mode_specifig_statistic_global_model.share_fund(self.fund)
        self.battle_info_global_model.broadcast_command("finish_round")
        self.give_fund_to_users()

        if self.battle_timer != None:
            self.battle_timer.destroy()

        self.broadcast_command("round_finish", (server_properties.ROUND_END_SCREEN_TIME_IN_SEC, user_infos))
        self.battle_field_global_model.broadcast_command("battle_finish")

        battle_start_timer = threading.Timer(server_properties.ROUND_END_SCREEN_TIME_IN_SEC, self.start_new_round)
        battle_start_timer.start()

    def prepare_to_spawn_every_tank(self):
        for tank_global_model in self.battle_field_global_model.get_all_tank_global_models():
            if tank_global_model == None: return
            tank_global_model.prepare_to_spawn()

    def send_battle_start_commands(self, user_infos):
        self.battle_mode_specifig_statistic_global_model.refresh_user_stat()
        self.battle_field_global_model.broadcast_command("battle_restart")

        new_time_limit = self.battle_info_model_cc.limits.time_limit_in_sec
        self.broadcast_command("round_start", (new_time_limit,))
        self.battle_info_global_model.broadcast_command("start_round")

    def reset_user_infos(self, user_infos):
        for user_info in user_infos:
            user_info.deaths = 0
            user_info.kills = 0
            user_info.score = 0
            user_info.fund = 0

    def reset_battle_database_data(self):
        battle_id = self.battle_info_model_cc.battle_id
        battles_table.set_fund(0, battle_id)
        battles_table.set_score_team1(0, battle_id)
        battles_table.set_score_team2(0, battle_id)
        battles_table.set_battle_start_time(datetime.datetime.now(), battle_id)

        for user_id in self.battle_field_global_model.get_all_user_ids():
            battle_users_table.set_deaths(0, user_id)
            battle_users_table.set_kills(0, user_id)
            battle_users_table.set_score(0, user_id)

    def reset_timer(self):
        time_limit_in_sec = self.battle_info_model_cc.limits.time_limit_in_sec

        if not time_limit_in_sec == 0:
            self.set_time(time_limit_in_sec)

    def start_new_round(self):
        self.fund = 0
        self.round_started = True
        user_infos = self.battle_field_global_model.get_all_user_infos()

        if self.battle_mode.is_team_battle():
            self.battle_mode_specifig_statistic_global_model.set_team_score(Team.RED, 0)
            self.battle_mode_specifig_statistic_global_model.set_team_score(Team.BLUE, 0)
            self.battle_info_global_model.set_team_score(Team.BLUE, 0)
            self.battle_info_global_model.set_team_score(Team.RED, 0)
            self.battle_mode_specifig_statistic_global_model.swap_teams()
            self.battle_info_global_model.swap_teams()
            self.battle_field_global_model.swap_teams()
            self.swap_every_tank_team()
            battle_users_table.swap_teams(self.battle_info_model_cc.battle_id)
            self.battle_select_global_model.swap_place_holder_teams(self.battle_field_global_model.get_all_user_ids())

        self.reset_timer()
        self.reset_user_infos(user_infos)
        self.reset_battle_database_data()
        self.send_battle_start_commands(user_infos)
        self.prepare_to_spawn_every_tank()

    def get_time_left_in_seconds(self):
        return int(self.battle_timer.get_time_left_in_seconds())

    def is_user_spectator(self, user_id):
        return self.battle_field_global_model.is_user_spectator(user_id)

    def create_cc(self):
        _statistics_model_cc = statistics_model_cc.StatisticsModelCC()
        _statistics_model_cc.battle_name = self.battle_info_model_cc.name
        _statistics_model_cc.limits = self.battle_info_model_cc.limits
        _statistics_model_cc.max_people_count = self.battle_info_model_cc.max_people_count
        return _statistics_model_cc

    def get_model_data(self):
        self.statistics_model_cc.fund = self.fund
        self.statistics_model_cc.suspicious_user_ids = [] # TODO: get suspicious_user_ids
        self.statistics_model_cc.time_left = self.get_time_left_in_seconds()
        return self.statistics_model_cc

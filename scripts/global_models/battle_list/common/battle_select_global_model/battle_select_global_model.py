from global_models.battle_list.common.battle_item_global_model import battle_item_global_model
from client.layouts.battle_list.models.battle_select_model import battle_select_model
from global_models.lobby.rank_notifier_global_model import rank_notifier_global_model
from global_models.battle.common.battle_field_global_model import battle_field_global_model
from global_models.battle_list.common.clan_info_global_model import clan_info_global_model
from global_models.lobby.uid_notifier_global_model import uid_notifier_global_model
from global_models.battle_list.common.map_info_global_model import map_info_global_model
from global_models.battle_list.common.clan_info_global_model import clan_info_model_cc
from global_models.battle_list.common.map_info_global_model import map_info_model_cc
from global_models.battle.common.battle_field_global_model.user_info import UserInfo
from client.layouts.battle_list.battle_data import battle_limits
from client.layouts.battle_list.battle_data import battle_theme
from client.layouts.battle_list.battle_data import battle_data
from client.layouts.battle_list.battle_data import battle_mode
from global_models.battle.common.tank_global_model import team
from space.global_model import GlobalModel
from loaders.map_loader import map_loader
from utils.data_types import range_data
from database import battle_users_table
from database import battles_table
from utils.log import console_out

from datetime import datetime

class BattleSelectGlobalModel(GlobalModel):

    CLIENT_MODEL = battle_select_model.BattleSelectModel

    def __init__(self, global_game_object, global_space, owner_id=None):
        super().__init__(global_game_object, global_space, owner_id)

        self.battle_item_global_game_objects_by_id = {}
        self.map_game_object_by_id = {}
        self.current_battle_id = 0
        self.placeholder_info_by_user_id = {}
        self.all_battle_ids = []

        self.create_map_global_game_objects()

    def init_done(self):
        self.load_battles_from_database()

    def swap_place_holder_teams(self, user_ids):
        for user_id in user_ids:
            if not user_id in self.placeholder_info_by_user_id: continue
            placeholder_info = self.placeholder_info_by_user_id[user_id]

            if placeholder_info.team == team.Team.RED:
                placeholder_info.team = team.Team.BLUE
                continue

            placeholder_info.team = team.Team.RED

    def get_placeholder_info(self, user_id):
        if not user_id in self.placeholder_info_by_user_id:
            return

        return self.placeholder_info_by_user_id[user_id]

    def add_placeholder_info(self, user_id, placeholder_info):
        self.placeholder_info_by_user_id[user_id] = placeholder_info

    def remove_placeholder_info(self, user_id):
        del self.placeholder_info_by_user_id[user_id]

    def get_map_global_game_object_by_id(self, id):
        return self.map_game_object_by_id[id]

    def get_all_map_global_game_objects(self):
        return self.map_game_object_by_id.values()

    def create_map_global_game_objects(self):
        all_maps = map_loader.get_all_maps()

        for map_info in all_maps:
            map_global_game_object = self.global_space.add_global_game_object("map_" + map_info.name_en)
            self.map_game_object_by_id[map_info.map_id] = map_global_game_object

            _map_info_model_cc = map_info_model_cc.MapInfoModelCC()
            _map_info_model_cc.map_id = map_info.map_id
            _map_info_model_cc.name_en = map_info.name_en
            _map_info_model_cc.name_ru = map_info.name_ru
            _map_info_model_cc.max_people = map_info.max_people
            _map_info_model_cc.preview_image = map_info.preview_image
            _map_info_model_cc.rank_limit = range_data.Range(map_info.rank_limit_max, map_info.rank_limit_min)
            _map_info_model_cc.supported_modes = map_info.supported_modes
            _map_info_model_cc.theme = map_info.theme

            _clan_info_model_cc = clan_info_model_cc.ClanInfoModelCC()

            map_global_game_object.add_global_model(map_info_global_model.MapInfoGlobalModel, model_args=(_map_info_model_cc,))
            map_global_game_object.add_global_model(clan_info_global_model.ClanInfoGlobalModel, model_args=(_clan_info_model_cc,))

    def calculate_time_left(self, time_limit_in_sec, battle_start_time):
        time_from_start = (datetime.now() - battle_start_time).total_seconds()
        time_left_in_sec = int(time_limit_in_sec - time_from_start)

        if time_left_in_sec < 0:
            return 0

        return time_left_in_sec

    def add_placeholder_from_database_to_battle(self, _battle_field_global_model, battle_id):
        battle_user_rows = battle_users_table.get_users_by_battle_id(battle_id)
        for battle_user_row in battle_user_rows:

            user_info = UserInfo()
            user_info.deaths = battle_user_row["deaths"]
            user_info.kills = battle_user_row["kills"]
            user_info.rank = battle_user_row["_rank"]
            user_info.score = battle_user_row["score"]
            user_info.uid = battle_user_row["uid"]
            user_info.user_id = battle_user_row["user_id"]
            user_info.suspicious = battle_user_row["suspicious"]

            _battle_field_global_model.add_placeholder(user_info, team.int_to_team(battle_user_row["team"]))

    def load_battles_from_database(self):
        battle_rows = battles_table.get_all_battle_rows()

        for battle_row in battle_rows:
            _battle_data = battle_data.BattleData()
            _battle_data.battle_id = battle_row["battle_id"]
            _battle_data.auto_balance = battle_row["auto_balance"]
            _battle_data.battle_mode = battle_mode.battle_mode_int_to_enum(battle_row["battle_mode"])
            _battle_data.friendly_fire = battle_row["friendly_fire"]
            _battle_data.limits = battle_limits.BattleLimits()
            _battle_data.limits.score_limit = battle_row["score_limit"]
            _battle_data.limits.time_limit_in_sec = battle_row["time_limit_in_sec"]
            _battle_data.map_id = battle_row["map_id"]
            _battle_data.max_people_count = battle_row["max_people_count"]
            _battle_data.name = battle_row["name"]
            _battle_data.private_battle = battle_row["private_battle"]
            _battle_data.pro_battle = battle_row["pro_battle"]
            _battle_data.rank_range = range_data.Range(battle_row["rank_range_max"], battle_row["rank_range_min"])
            _battle_data.theme = battle_theme.battle_theme_int_to_enum(battle_row["theme"])
            _battle_data.without_bonuses = battle_row["without_bonuses"]
            _battle_data.without_crystals = battle_row["without_crystals"]
            _battle_data.without_supplies = battle_row["without_supplies"]
            _battle_data.without_upgrades = battle_row["without_upgrades"]

            battle_item_global_game_object = self.create_new_battle(_battle_data)
            battle_field_global_game_object = battle_item_global_game_object.get_global_model(battle_item_global_model.BattleItemGlobalModel).battle_field_global_game_object
            _battle_field_global_model = battle_field_global_game_object.get_global_model(battle_field_global_model.BattleFieldGlobalModel)

            statistics_global_model = _battle_field_global_model.statistics_global_model

            if _battle_data.limits.time_limit_in_sec != 0:
                time_left_in_sec = self.calculate_time_left(_battle_data.limits.time_limit_in_sec, battle_row["battle_start_time"])
                statistics_global_model.set_time(time_left_in_sec)

            statistics_global_model.set_fund(battle_row["fund"])
            if battle_row["score_team1"] + battle_row["score_team2"] > 0:
                _battle_field_global_model.set_team_score_from_server(team.Team.BLUE, battle_row["score_team1"])
                _battle_field_global_model.set_team_score_from_server(team.Team.RED, battle_row["score_team2"])

            self.add_placeholder_from_database_to_battle(_battle_field_global_model, _battle_data.battle_id)
            console_out.color_print("[BATTLE_SELECT_GLOBAL_MODEL] RECOVERED_BATTLE: \"" + _battle_data.name + "\" #" + str(_battle_data.battle_id), "yellow")

    def generate_new_battle_id(self, battle_id=None):
        if battle_id != None:
            return battle_id

        while self.current_battle_id in self.all_battle_ids:
            self.current_battle_id += 1

        return self.current_battle_id

    def create_new_battle(self, _battle_data, battle_id=None):
        _battle_data.battle_id = self.generate_new_battle_id(battle_id)
        self.all_battle_ids.append(_battle_data.battle_id)

        battle_item_global_game_object = self.global_space.add_global_game_object("battle_item_" + str(_battle_data.battle_id))
        battle_item_global_game_object.add_global_model(battle_item_global_model.BattleItemGlobalModel, model_args=(_battle_data,))

        self.battle_item_global_game_objects_by_id[battle_item_global_game_object.id] = battle_item_global_game_object

        for client_model in self.get_all_client_models():
            client_model.add_battle_items([battle_item_global_game_object])

        return battle_item_global_game_object

    def get_all_battle_item_global_game_objects(self):
        return self.battle_item_global_game_objects_by_id.values()

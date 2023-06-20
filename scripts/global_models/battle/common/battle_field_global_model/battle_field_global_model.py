from global_models.battle.common.battle_field_global_model.battle_field_model_cc import BattleFieldModelCC
from global_models.battle.bonus.bonus_postpone_global_model import bonus_postpone_global_model
from global_models.battle.bonus.battle_field_bonus_global_model import battle_field_bonus_global_model
from global_models.battle_list.common.battle_select_global_model import battle_select_global_model
from global_models.battle_list.common.battle_info_global_model import battle_info_global_model
from global_models.battle.common.battle_debug_global_model import battle_debug_global_model
from global_models.battle.common.lighting_sfx_global_model import lighting_sfx_global_model
from global_models.battle.mine.battle_mines_global_model import battle_mines_global_model
from global_models.battle.dm.statistics_dm_global_model import statistics_dm_global_model
from global_models.battle.tdm.statistics_team_global_model import statistics_team_global_model
from global_models.lobby.rank_notifier_global_model import rank_notifier_global_model
from global_models.battle.dm.battle_dm_global_model import battle_dm_global_model
from global_models.battle.tdm.battle_tdm_global_model import battle_tdm_global_model
from global_models.battle.common.billboards_global_model import billboards_global_model
from global_models.battle.common.team_kick_global_model import team_kick_global_model
from global_models.battle.common.statistics_global_model import statistics_global_model
from global_models.battle.common.battle_map_global_model import battle_map_global_model
from client.layouts.lobby.models.user_property_model import user_property_model
from client.layouts.battle.models.battle_field_model import battle_field_model
from client.layouts.battle_list.battle_data.battle_mode import BattleMode
from global_models.battle.common.tank_global_model import tank_global_model
from global_models.battle.common.tank_global_model.team import Team
from loaders.client_resource_loader import client_resource_loader
from space.global_model import GlobalModel
from space import global_space_registry
from utils.data_types import range_data
from database import battle_users_table
from . import battle_field_sounds
from . import placeholder_info
from . import user_info
import server_properties

class BattleFieldGlobalModel(GlobalModel):

    CLIENT_MODEL = battle_field_model.BattleFieldModel

    def __init__(self, global_game_object, global_space, battle_item_global_model, owner_id=None):
        super().__init__(global_game_object, global_space, owner_id)

        self.active = True
        self.battle_info_global_model = battle_item_global_model.battle_info_global_game_object.get_global_model(battle_info_global_model.BattleInfoGlobalModel)
        self.battle_info_global_model_data = self.battle_info_global_model.battle_info_model_cc
        self.battle_select_global_model = global_space_registry.get_global_model(battle_select_global_model.BattleSelectGlobalModel, global_game_object_name="default_game_object", global_space_name="battle_select")
        self.statistics_global_model = None
        self.team_kick_global_model = None
        self.battle_events = BattleEvents()

        self.spectator_user_ids = []
        self.team1_user_ids = []
        self.team2_user_ids = []
        self.user_infos_by_user_id = {}
        self.client_objects_by_user_id = {}

    def init_done(self):
        self.battle_map_global_game_object = self.create_map_global_game_object()
        self.battle_field_model_cc = self.create_cc()
        self.create_models()
        self.statistics_global_model = self.global_game_object.get_global_model(statistics_global_model.StatisticsGlobalModel)

    def swap_teams(self):
        temp = self.team1_user_ids
        self.team1_user_ids = self.team2_user_ids
        self.team2_user_ids = temp

    def get_client_objects_by_user_id(self, user_id):
        if not user_id in self.client_objects_by_user_id: return
        return self.client_objects_by_user_id[user_id]

    def rank_up(self, user_id, rank_id):
        self.statistics_global_model.broadcast_command("on_rank_changed", (user_id, rank_id))
        battle_users_table.set_rank(rank_id, user_id)
        self.user_infos_by_user_id[user_id].rank = rank_id
        _rank_notifier_global_model = global_space_registry.get_global_model(rank_notifier_global_model.RankNotifierGlobalModel, global_space_name="lobby", global_game_object_name="panel")
        _rank_notifier_global_model.set_ranks()

    def set_team_score_from_server(self, team, score):
        self.statistics_global_model.set_team_score_from_server(team, score)
        self.battle_info_global_model.set_team_score_from_server(team, score)

    def add_kill_to_models(self, killer_user_info, target_user_info):
        killer_team = self.get_user_team(killer_user_info.user_id)
        self.statistics_global_model.add_kill(killer_user_info, killer_team, target_user_info)
        self.battle_info_global_model.update_user_score(killer_user_info)

        if self.battle_info_global_model_data.battle_mode.is_team_battle():
            self.battle_info_global_model.add_team_score(killer_team, 1)

    def add_kill_to_database(self, killer_user_info, target_user_info):
        battle_users_table.set_score(killer_user_info.score, killer_user_info.user_id)
        battle_users_table.set_kills(killer_user_info.kills, killer_user_info.user_id)
        battle_users_table.set_deaths(target_user_info.deaths, target_user_info.user_id)

    def add_score_to_user_property(self, score, user_id):
        client_object = self.client_objects_by_user_id[user_id]
        _user_property_model = client_object.client_space_registry.get_model(user_property_model.UserPropertyModel, game_object_name="panel", space_name="lobby")
        _user_property_model.add_buffered_score(score)
        # TODO: save score when user leaves

    def add_kill(self, killer_id, target_id):
        killer_user_info = self.user_infos_by_user_id[killer_id]
        target_user_info = self.user_infos_by_user_id[target_id]

        self.add_kill_to_models(killer_user_info, target_user_info)
        self.add_kill_to_database(killer_user_info, target_user_info)
        self.add_score_to_user_property(server_properties.KILL_SCORE, killer_id)

    def update_battle_field_global_space(self):
        for client_model in self.get_all_client_models():
            client_model.update_battle_field_global_space()

    def get_team_list(self, team):
        if team == Team.BLUE:
            return self.team1_user_ids
        if team == Team.RED:
            return self.team2_user_ids
        return self.team1_user_ids

    def create_new_user_info_from_client_object(self, client_object):
        _user_property_model = client_object.client_space_registry.get_model(user_property_model.UserPropertyModel, game_object_name="panel", space_name="lobby")
        user_property_model_data = _user_property_model.model_data

        new_user_info = user_info.UserInfo()
        new_user_info.rank = user_property_model_data.rank
        new_user_info.uid = user_property_model_data.uid
        new_user_info.user_id = user_property_model_data.user_id
        return new_user_info

    def remove_user_id_from_team_list(self, user_id):
        team = self.get_user_team(user_id)
        team_list = self.get_team_list(team)
        team_list.remove(user_id)

    def remove_user_from_lists(self, user_id):
        self.statistics_global_model.remove_user(user_id)
        self.battle_info_global_model.remove_user(user_id)
        del self.user_infos_by_user_id[user_id]

    def remove_tank_by_user_id(self, user_id):
        _tank_global_model = self.global_space.get_global_model(tank_global_model.TankGlobalModel, global_game_object_id=user_id)
        _tank_global_model.remove_tank()

    # this function is called when user leaves the battle by clicking battle_list or garage button
    def leave_battle(self, user_id):
        if not user_id in self.get_all_user_ids(): return

        self.remove_user_id_from_team_list(user_id)
        self.remove_user_from_lists(user_id)

        self.remove_tank_by_user_id(user_id)
        battle_users_table.delete_user(user_id)
        self.client_objects_by_user_id.pop(user_id)
        self.battle_events.dispatch_event("user_leaved", (user_id,))

    def add_placeholder_info(self, user_id):
        team = self.get_user_team(user_id)
        _placeholder_info = placeholder_info.PlaceholderInfo(team, self.battle_info_global_model_data.battle_id)
        self.battle_select_global_model.add_placeholder_info(user_id, _placeholder_info)

    # this function is called when user leaves the battle by closing the client
    def exit_battle(self, user_id):
        if not user_id in self.get_all_user_ids(): return

        self.remove_tank_by_user_id(user_id)
        self.add_placeholder_info(user_id)
        self.client_objects_by_user_id.pop(user_id)
        self.battle_events.dispatch_event("user_leaved", (user_id,))

    def add_user_to_lists(self, user_info, team):
        self.statistics_global_model.add_user(user_info, team)
        self.battle_info_global_model.add_user(user_info, team)
        self.user_infos_by_user_id[user_info.user_id] = user_info

    def add_new_user_to_battle(self, client_object, team):
        user_id = client_object.user_id

        if not user_id in self.user_infos_by_user_id:
            user_info = self.create_new_user_info_from_client_object(client_object)
        else:
            user_info = self.user_infos_by_user_id[user_id]

        self.add_user_to_lists(user_info, team)
        battle_users_table.add_user(user_info, team, self.battle_info_global_model_data.battle_id)

    # this function will handle adding user that has placeholder in this battle
    def add_existing_player_to_battle(self, user_id):
        self.battle_select_global_model.remove_placeholder_info(user_id)

    def add_user_to_team_kick(self, user_id, team, client_object):
        if self.team_kick_global_model != None:
            exclude = client_object.user_property_model.model_data.has_vote_immunity()
            self.team_kick_global_model.add_user(user_id, team, exclude)

    def try_join(self, team, client_object):
        team_list = self.get_team_list(team)
        user_id = client_object.user_id
        is_user_in_team_list = user_id in team_list

        if len(team_list) >= self.battle_info_global_model_data.max_people_count and not is_user_in_team_list:
            return False

        self.client_objects_by_user_id[user_id] = client_object
        self.add_user_to_team_kick(user_id, team, client_object)
        self.battle_events.dispatch_event("user_joined", (user_id, team))

        if is_user_in_team_list:
            self.add_existing_player_to_battle(user_id)
            return True

        team_list.append(user_id)
        self.add_new_user_to_battle(client_object, team)
        return True

    def add_placeholder(self, user_info, team):
        team_list = self.get_team_list(team)
        user_id = user_info.user_id

        if len(team_list) >= self.battle_info_global_model_data.max_people_count:
            return False

        team_list.append(user_id)

        self.add_user_to_lists(user_info, team)
        self.add_placeholder_info(user_id)
        return True

    def get_all_user_ids(self):
        return list(self.user_infos_by_user_id.keys())

    def get_all_user_infos(self):
        return list(self.user_infos_by_user_id.values())

    def get_team_user_infos(self, team):
        return [self.user_infos_by_user_id[_id] for _id in self.get_team_list(team)]

    def get_all_tank_global_models(self):
        out = []

        for user_id in self.get_all_user_ids():
            global_game_object = self.global_space.get_global_game_object_by_id(user_id)
            if global_game_object == None: continue
            out.append(global_game_object.get_global_model(tank_global_model.TankGlobalModel))

        return out

    def get_tank_global_model_by_user_id(self, user_id):
        global_game_object = self.global_space.get_global_game_object_by_id(user_id)
        if global_game_object == None: return
        return global_game_object.get_global_model(tank_global_model.TankGlobalModel)

    def get_user_team(self, user_id):
        if self.battle_info_global_model_data.battle_mode == BattleMode.DM:
            return Team.NONE
        if user_id in self.team1_user_ids:
            return Team.BLUE
        return Team.RED

    def join_as_spectator(self, user_id):
        self.spectator_user_ids.append(user_id)

    def is_user_spectator(self, user_id):
        return user_id in self.spectator_user_ids

    def create_models(self):
        battle_mode = self.battle_info_global_model_data.battle_mode

        if battle_mode == BattleMode.DM:
            self.global_game_object.add_global_model(battle_dm_global_model.BattleDmGlobalModel)
            self.global_game_object.add_global_model(statistics_dm_global_model.StatisticsDmGlobalModel)

        if battle_mode == BattleMode.TDM:
            self.global_game_object.add_global_model(battle_tdm_global_model.BattleTdmGlobalModel)

        if battle_mode in [BattleMode.TDM, BattleMode.CTF, BattleMode.CP]:
            self.global_game_object.add_global_model(statistics_team_global_model.StatisticsTeamGlobalModel)
            self.team_kick_global_model = self.global_game_object.add_global_model(team_kick_global_model.TeamKickGlobalModel)

        self.global_game_object.add_global_model(bonus_postpone_global_model.BonusPostponeGlobalModel)
        self.global_game_object.add_global_model(battle_field_bonus_global_model.BattleFieldBonusGlobalModel)
        self.global_game_object.add_global_model(battle_debug_global_model.BattleDebugGlobalModel)
        self.global_game_object.add_global_model(battle_mines_global_model.BattleMinesGlobalModel)
        self.global_game_object.add_global_model(lighting_sfx_global_model.LightingSfxGlobalModel, model_args=([],)) # TODO: create battle_field lighting_effects
        self.global_game_object.add_global_model(statistics_global_model.StatisticsGlobalModel)
        self.global_game_object.add_global_model(billboards_global_model.BillboardsGlobalModel)

    def create_map_global_game_object(self):
        battle_map_global_game_object = self.global_space.add_global_game_object("battle_map")
        battle_map_global_game_object.add_global_model(battle_map_global_model.BattleMapGlobalModel, model_args=(self.battle_info_global_model,))
        return battle_map_global_game_object

    def create_cc(self):
        cc = BattleFieldModelCC()
        cc.battlefield_sounds = battle_field_sounds.BattleFieldSounds()
        cc.battlefield_sounds.battle_finish_sound = client_resource_loader.get_resource_id("/battle/sounds/battle_field/battle_end")
        cc.battlefield_sounds.kill_sound = client_resource_loader.get_resource_id("/battle/sounds/battle_field/kill")
        cc.color_transform_multiplier = server_properties.COLOR_TRANSFORM_MULTIPLIER
        cc.idle_kick_period_msec = server_properties.IDLE_KICK_PERIOD_MSEC
        cc.map_game_object_id = self.battle_map_global_game_object.id
        cc.range = range_data.Range(max=3, min=1) # TODO: find correct number (no idea what it is)
        cc.shadow_map_correction_factor = 0 # TODO: find correct number (no idea what it is)
        cc.tank_activation_delay_in_ms = server_properties.TANK_ACTIVATION_DELAY_IN_MS
        return cc

    def get_model_data(self):
        self.battle_field_model_cc.active = self.active
        return self.battle_field_model_cc


class BattleEvents:
    def __init__(self):
        self.listenners_by_event_name = {}

    def add_event_listenner(self, event_name, function):
        if not event_name in self.listenners_by_event_name:
            self.listenners_by_event_name[event_name] = []

        self.listenners_by_event_name[event_name].append(function)

    def remove_event_listenner(self, event_name, function):
        self.listenners_by_event_name[event_name].remove(functionn)

    def dispatch_event(self, event_name, args=()):
        if not event_name in self.listenners_by_event_name:
            return

        for function in self.listenners_by_event_name[event_name]:
            function(*args)

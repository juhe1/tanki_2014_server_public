from global_models.battle.common.battle_debug_global_model import battle_debug_global_model
from global_models.battle.common.battle_map_global_model import battle_map_global_model
from client.layouts.battle.models.battle_mines_model import battle_mines_model
from global_models.battle.common.tank_global_model.team import Team
from global_models.battle.mine.mine_rtree import MineRTree
from global_models.battle.mine.mine import Mine
from panda3d.core import Vec3
from utils.collision import _3d_utils
from space.global_model import GlobalModel
from . import battle_mines_model_cc
import server_properties
from utils import panda_math
from game import game

import threading

class BattleMinesGlobalModel(GlobalModel):

    CLIENT_MODEL = battle_mines_model.BattleMinesModel

    def __init__(self, global_game_object, global_space, owner_id=None):
        super().__init__(global_game_object, global_space, owner_id)

        self.battle_mines_model_cc = battle_mines_model_cc.BattleMinesModelCC()
        self.battle_debug_global_model = global_game_object.get_global_model(battle_debug_global_model.BattleDebugGlobalModel)

        map_info = self.global_space.get_global_model(battle_map_global_model.BattleMapGlobalModel, global_game_object_name="battle_map").map_info
        self.map_collision_geometry = map_info.collision_geometry

        self.mine_rtree = MineRTree()
        self.mines_by_id = {}
        self.mines_by_user_id = {}
        self.current_mine_id = 0

    def get_all_mines(self):
        return list(self.mines_by_id.values())

    def generate_new_mine_id(self):
        self.current_mine_id += 1
        return self.current_mine_id

    def get_opponent_team(self, team):
        if team == Team.NONE:
            return Team.NONE
        if team == Team.BLUE:
            return Team.RED
        return Team.BLUE

    def check_mine_hit(self, tank_global_model):
        tank_state = tank_global_model.tank_state
        tank_half_size = tank_global_model.size / 2

        tank_bound_min, tank_bound_max = tank_global_model.get_bounding_box()
        mine_ids = self.mine_rtree.get_mine_ids_inside_bound(tank_bound_min, tank_bound_max, tank_state.position, self.get_opponent_team(tank_global_model.team))

        for mine_id in mine_ids:
            mine = self.mines_by_id[mine_id]
            mine_position = mine.position + Vec3(0,0,60)

            is_mine_owner = mine.owner_id == tank_global_model.global_game_object.id
            if _3d_utils.point_inside_box_check(tank_state.orientation, tank_state.position, tank_half_size, mine_position) and mine.activated and not is_mine_owner:
                self.explode_mine(mine, tank_global_model)

    def calculate_mine_position(self, mine_adder_position):
        mine_adder_position += Vec3(0, 0, 100)
        mine_offset = Vec3(0, 0, server_properties.MINE_OFFSET_FROM_GROUND)

        ray_result = self.map_collision_geometry.physics_world.rayTestClosest(mine_adder_position, mine_adder_position + Vec3(0,0,-4000))

        if not ray_result.hasHit():
            return

        intersection_point = ray_result.getHitPos()

        return intersection_point + mine_offset

    def add_mine(self, mine_adder_global_tank_model):
        mine_adder_position = mine_adder_global_tank_model.tank_state.position
        mine_position = self.calculate_mine_position(mine_adder_position)

        if mine_position == None: return

        mine = Mine()
        mine.mine_id = self.generate_new_mine_id()
        mine.owner_id = mine_adder_global_tank_model.global_game_object.id
        mine.position = mine_position
        mine.team = mine_adder_global_tank_model.team

        self.broadcast_command("put_mine", (mine.mine_id, mine.position, mine.owner_id))

        if not mine.owner_id in self.mines_by_user_id:
            self.mines_by_user_id[mine.owner_id] = []

        self.mines_by_id[mine.mine_id] = mine
        self.mines_by_user_id[mine.owner_id].append(mine)
        self.mine_rtree.add_mine(mine)

        timer = threading.Timer(server_properties.MINE_ACTIVATE_TIME_MS/1000, self.activate_mine, args=(mine,))
        timer.start()

    def explode_mine(self, mine, tank_global_model):
        from global_models.battle.common.tank_global_model.tank_global_model import TankGlobalModel

        self.broadcast_command("explode_mine", (mine.mine_id, tank_global_model.global_game_object.id))
        self.remove_mine_from_server(mine)

        damage = 20 # TODO: calculate_damage
        damager_tank_global_model = self.global_space.get_global_model(TankGlobalModel, global_game_object_id=mine.owner_id)
        protection_name = "jeaaaaa" # TODO: add real protection
        tank_global_model.damage_tank(damage, damager_tank_global_model, protection_name, apply_effect=False)

    def remove_user_mines(self, user_id):
        if not user_id in self.mines_by_user_id:
            return

        for mine in self.mines_by_user_id[user_id][:]: # make a copy of the list using [:] to avoid index errors
            self.remove_mine_from_server(mine)

        self.broadcast_command("remove_mines", (user_id,))

    def remove_mine_from_server(self, mine):
        self.mines_by_id.pop(mine.mine_id)
        self.mines_by_user_id[mine.owner_id].remove(mine)
        self.mine_rtree.remove_mine(mine)

    def activate_mine(self, mine):
        mine.activated = True
        self.broadcast_command("activate_mine", (mine.mine_id,))

    def get_model_data(self):
        self.battle_mines_model_cc.battle_mines = self.get_all_mines() # TODO: get mines
        return self.battle_mines_model_cc

from global_models.battle.supplie_effect.duration_controller_global_model import duration_controller_global_model
from global_models.battle.supplie_effect.effect_description_global_model import effect_description_global_model
from global_models.battle.common.battle_field_global_model import battle_field_global_model
from global_models.battle.common.battle_field_global_model import battle_field_global_model
from global_models.battle.mine.battle_mines_global_model import battle_mines_global_model
from global_models.battle.weapon.weapon_common_global_model import weapon_common_global_model
from global_models.battle.common.battle_map_global_model import battle_map_global_model
from client.layouts.battle.models.battle_field_model import battle_field_model
from client.layouts.battle_list.battle_data.battle_mode import BattleMode
from client.layouts.battle.models.inventory_model import inventory_model
from loaders.client_resource_loader import client_resource_loader
from client.layouts.battle.models.tank_model import tank_model
from client.layouts.battle.tank.enums import DeathReason
from global_models.battle.common.tank_global_model.team import Team
from space.global_model import GlobalModel
from utils.time.timer import Timer
from utils import own_math
from . import tank_resources
from . import tank_sounds
from . import tank_state
import server_properties
from game import game
from utils import panda_math

from panda3d.core import Material, Vec3
import threading
import random
import time
import math
import numpy as np

FIRST_AID_EFFECT_INDEX = 1
DOUBLE_ARMOR_EFFECT_INDEX = 2
DOUBLE_POWER_EFFECT_INDEX = 3
NITRO_EFFECT_INDEX = 4

class TankGlobalModel(GlobalModel):

    CLIENT_MODEL = tank_model.TankModel

    def __init__(self, global_game_object, global_space, tank_model_cc, color_database_item, tank_database_item, owner_id=None):
        super().__init__(global_game_object, global_space, owner_id)

        self.color_database_item = color_database_item
        self.tank_database_item = tank_database_item
        self.tank_model_cc = tank_model_cc

        self.map_info = global_space.get_global_model(battle_map_global_model.BattleMapGlobalModel, global_game_object_name="battle_map").map_info
        self.battle_field_global_model = global_space.get_global_model(battle_field_global_model.BattleFieldGlobalModel, global_game_object_name="default_game_object")
        self.battle_info_global_model_data = self.battle_field_global_model.battle_info_global_model_data
        self.owner_client_object = self.battle_field_global_model.get_client_objects_by_user_id(self.owner_id)
        self.inventory_model = self.owner_client_object.client_space_registry.get_model(inventory_model.InventoryModel, game_object_name="default_game_object", space_id=global_space.id)
        self.battle_mines_global_model = global_space.get_global_model(battle_mines_global_model.BattleMinesGlobalModel, global_game_object_name="default_game_object")

        tank_parts = self.tank_model_cc.tank_parts
        weapon_game_object = self.global_space.get_global_game_object_by_id(tank_parts.weapon_id)
        weapon_game_object.get_global_model(weapon_common_global_model.WeaponCommonGlobalModel).init(self)
        #self.hull_game_object = self.global_space.get_global_game_object_by_id(tank_parts.hull_id)
        #self.color_game_object = self.global_space.get_global_game_object_by_id(tank_parts.color_id)

        self.temperature = Temperature(self)
        self.specification = TankSpecification(
            self,
            tank_model_cc.tank_initialization_data.speed,
            tank_model_cc.tank_initialization_data.turn_speed,
            tank_model_cc.tank_initialization_data.turret_rotation_speed,
            tank_model_cc.tank_initialization_data.acceleration
        )

        self.logic_state = tank_state.LogicState()
        self.tank_state = tank_state.TankState()
        self.health = self.tank_model_cc.max_health
        self.team = self.battle_field_global_model.get_user_team(owner_id)
        self.size = self.tank_database_item.garage_item.tank_physics.hull_size

        self.double_armor_effect_activated = False
        self.double_power_effect_activated = False
        self.effect_duration_controller_global_models_by_index = {}

        self.dead_timer = Timer(server_properties.TANK_DEAD_TIME_IN_MS / 1000)
        self.dead_timer.set_done()
        self.spawn_timer = Timer(server_properties.TANK_SPAWN_DELAY_IN_MS / 1000)
        self.activation_timer = Timer(server_properties.TANK_ACTIVATION_DELAY_IN_MS / 1000)
        self.spawn_point = None

        self.effect_description_global_game_objects_by_index = {}

        self.visual_node = None
        self.add_missing_data_to_cc()
        self.create_tank_visualizer()

    def remove_tank(self):
        self.reset_supplies()
        tank_parts = self.tank_model_cc.tank_parts
        self.global_space.get_global_game_object_by_id(tank_parts.hull_id).remove_global_game_object()
        self.global_space.get_global_game_object_by_id(tank_parts.weapon_id).remove_global_game_object()
        self.global_space.get_global_game_object_by_id(tank_parts.color_id).remove_global_game_object()
        self.global_space.get_global_game_object_by_id(self.global_game_object.id).remove_global_game_object()

    def swap_teams(self):
        if self.team == Team.RED:
            self.team = Team.BLUE
            return
        self.team = Team.RED

    def set_temperature(self, temperature):
        self.broadcast_command("set_temperature", (temperature,))

    def create_tank_visualizer(self):
        if not server_properties.DEBUG_ENABLED: return
        material = Material()
        material.set_diffuse((1, 0, 0, 1))

        self.visual_node = loader.loadModel("../models/box.egg")
        self.visual_node.set_material(material)

        # Attach the material to the geom
        self.visual_node.reparentTo(game.worldNP)
        self.visual_node.setScale(self.size.x, self.size.y, self.size.z)

    def get_bounding_box(self):
        half_size = self.size / 2
        orientation = self.tank_state.orientation

        vertex1 = panda_math.rotate_vec3(Vec3(-half_size.x, -half_size.y, -half_size.z), orientation)
        vertex2 = panda_math.rotate_vec3(Vec3(half_size.x, -half_size.y, -half_size.z), orientation)
        vertex3 = panda_math.rotate_vec3(Vec3(-half_size.x, half_size.y, -half_size.z), orientation)
        vertex4 = panda_math.rotate_vec3(Vec3(half_size.x, half_size.y, -half_size.z), orientation)
        vertex5 = panda_math.rotate_vec3(Vec3(-half_size.x, -half_size.y, half_size.z), orientation)
        vertex6 = panda_math.rotate_vec3(Vec3(half_size.x, -half_size.y, half_size.z), orientation)
        vertex7 = panda_math.rotate_vec3(Vec3(-half_size.x, half_size.y, half_size.z), orientation)
        vertex8 = panda_math.rotate_vec3(Vec3(half_size.x, half_size.y, half_size.z), orientation)

        vertexes = np.array([
            [vertex1.x, vertex2.x, vertex3.x, vertex4.x, vertex5.x, vertex6.x, vertex7.x, vertex8.x],
            [vertex1.y, vertex2.y, vertex3.y, vertex4.y, vertex5.y, vertex6.y, vertex7.y, vertex8.y],
            [vertex1.z, vertex2.z, vertex3.z, vertex4.z, vertex5.z, vertex6.z, vertex7.z, vertex8.z]
        ])

        x_min, y_min, z_min = [np.min(sub_array) for sub_array in np.split(vertexes, 3)]
        x_max, y_max, z_max = [np.max(sub_array) for sub_array in np.split(vertexes, 3)]
        bound_min = Vec3(x_min, y_min, z_min) + self.tank_state.position
        bound_max = Vec3(x_max, y_max, z_max) + self.tank_state.position

        return (bound_min, bound_max)

    def add_missing_data_to_cc(self):
        self.tank_model_cc.sounds = tank_sounds.TankSounds()
        self.tank_model_cc.sounds.engine_idle_sound = client_resource_loader.get_resource_id("/battle/sounds/tank/engine_idle")
        self.tank_model_cc.sounds.engine_moving_sound = client_resource_loader.get_resource_id("/battle/sounds/tank/engine_moving")
        self.tank_model_cc.sounds.engine_start_moving_sound = client_resource_loader.get_resource_id("/battle/sounds/tank/engine_start_moving")
        self.tank_model_cc.sounds.engine_start_sound = client_resource_loader.get_resource_id("/battle/sounds/tank/engine_start")
        self.tank_model_cc.sounds.engine_stop_moving_sound = client_resource_loader.get_resource_id("/battle/sounds/tank/engine_stop_moving")
        self.tank_model_cc.sounds.turret_rotation_sound = client_resource_loader.get_resource_id("/battle/sounds/tank/turret_rotation")

        self.tank_model_cc.tank_resources = tank_resources.TankResources()
        self.tank_model_cc.tank_resources.dead_color = client_resource_loader.get_resource_id("/battle/images/dead_color")
        self.tank_model_cc.tank_resources.death_sound = client_resource_loader.get_resource_id("/battle/sounds/tank/death_sound")

        self.tank_model_cc.tank_initialization_data.incarnation_id = 1 # TODO: find out what is incarnation_id

    def get_model_data(self):
        self.tank_model_cc.tank_initialization_data.logic_state = self.logic_state.state
        self.tank_model_cc.tank_initialization_data.tank_state = self.tank_state
        self.tank_model_cc.tank_initialization_data.team = self.team
        self.tank_model_cc.tank_initialization_data.health = int(self.health)
        return self.tank_model_cc

    def confirm_death(self):
        self.broadcast_command("death_confirmed")

    def reset_inventory_timers(self):
        if not self.battle_info_global_model_data.without_supplies:
            self.inventory_model.reset_timers()

    def get_all_effect_description_global_game_objects(self):
        return list(self.effect_description_global_game_objects_by_index.values())

    def reset_effect(self, effect_description_global_game_object):
        effect_description_global_game_object.get_global_model(duration_controller_global_model.DurationControllerGlobalModel).time_end()

    def reset_supplies(self):
        if not self.battle_info_global_model_data.without_supplies:
            self.inventory_model.reset_timers()

        for effect_description_global_game_object in self.get_all_effect_description_global_game_objects():
            self.reset_effect(effect_description_global_game_object)

    def kill_tank(self, reason, killer_tank_global_model=None):
        self.logic_state.state = tank_state.LogicStateEnum.DEAD
        self.dead_timer.start()
        self.temperature.reset_temperature()

        killer_id = None
        if killer_tank_global_model != None:
            killer_id = killer_tank_global_model.owner_id

        self.broadcast_command("kill", (reason, killer_id, server_properties.TANK_DEAD_TIME_IN_MS))
        self.battle_mines_global_model.remove_user_mines(self.global_game_object.id)

    def subtract_health(self, health):
        self.set_health(self.health - health)

    def add_health(self, health):
        self.set_health(self.health + health)

    def set_health(self, health):
        self.health = health
        health_rounded = round(self.health)
        self.broadcast_command("set_health", (int(health_rounded),)) # TODO: send only to spectators and to damaged player

    def subtract_protection(self, protection_name, damage):
        protection = self.color_database_item.get_property_value(protection_name)
        if protection == None: return damage
        return damage - damage * (protection * 0.01)

    def apply_effects_to_damage(self, damage, damager_double_power_effect_activated):
        if self.double_armor_effect_activated:
            damage = damage * 0.5

        if damager_double_power_effect_activated:
            damage = damage * 2

        return damage

    def damage_tank(self, damage, damager_tank_global_model, protection_name, apply_effect=True):
        friendly_fire = False # TODO: get friendly_fire some where

        if self.logic_state.state == tank_state.LogicStateEnum.DEAD: return

        if self.battle_info_global_model_data.battle_mode != BattleMode.DM and friendly_fire:
            if damager_tank_global_model.team == self.team: return

        if apply_effect:
            damage = self.apply_effects_to_damage(damage, damager_tank_global_model.double_power_effect_activated)

        damage = self.subtract_protection(protection_name, damage)
        self.subtract_health(damage)

        if self.health > 0: return

        self.kill_tank(DeathReason.KILLED_IN_BATTLE, damager_tank_global_model)
        self.battle_field_global_model.add_kill(damager_tank_global_model.owner_id, self.owner_id)

    def move(self, move_command, specification_id, client_time):
        # TODO: do anticheat stuff

        if self.logic_state.state == tank_state.LogicStateEnum.DEAD: return

        if move_command.position.z <= server_properties.MIN_ALLOWED_Z and self.logic_state.state != tank_state.LogicStateEnum.DEAD:
            self.kill_tank(DeathReason.SUICIDE)

        # update state
        self.tank_state.position = move_command.position
        self.tank_state.angular_velocity = move_command.angular_velocity
        self.tank_state.chassis_control = move_command.control
        self.tank_state.linear_velocity = move_command.linear_velocity
        self.tank_state.orientation = move_command.orientation

        self.battle_mines_global_model.check_mine_hit(self)

        if server_properties.DEBUG_ENABLED:
            self.visual_node.setPos(move_command.position.x, move_command.position.y, move_command.position.z)
            self.visual_node.setHpr(math.degrees(move_command.orientation.z), math.degrees(move_command.orientation.x), math.degrees(move_command.orientation.y))

        # move the tank in every client
        self.broadcast_command_only_to_other_players("move", (move_command,))

    def update_movement_control(self, client_time, specification_id, movement_control):
        self.tank_state.chassis_control = movement_control
        self.broadcast_command_only_to_other_players("update_movement_control", (movement_control, ))

    def rotate_turret(self, client_time, rotate_turret_command, incarnation_id):
        # TODO: check turret rotate command

        self.tank_state.turret_angle = rotate_turret_command.angle
        self.tank_state.turret_control = rotate_turret_command.control
        self.broadcast_command_only_to_other_players("rotate_turret", (rotate_turret_command, ))

    def generate_new_spawn(self):
        spawns = self.map_info.get_spawns_by_team(self.team)
        self.spawn_point = random.choice(spawns) # choose random spawn_point

        self.tank_state.orientation = self.spawn_point.position
        self.tank_state.position = self.spawn_point.rotation

    def prepare_to_spawn(self):
        if not self.dead_timer.is_time_passed():
            return

        self.spawn_timer.start()
        self.generate_new_spawn()
        self.reset_supplies()

        incarnation_id = 1
        spawn_timer = threading.Timer(server_properties.TANK_SPAWN_DELAY_IN_MS / 1000, self.spawn, args=(incarnation_id,))
        spawn_timer.start()

        self.broadcast_command("prepare_to_spawn", (self.spawn_point.position, self.spawn_point.rotation))

    def spawn(self, incarnation_id):
        # check that enought time is bassed from preparing
        if not self.spawn_timer.is_time_passed():
            return

        self.health = self.tank_model_cc.max_health
        self.activation_timer.start()

        self.logic_state.state = tank_state.LogicStateEnum.ACTIVATING

        spawn_commmand_args = (self.team, self.spawn_point.position, self.spawn_point.rotation, round(self.health), incarnation_id)
        self.broadcast_command("spawn", spawn_commmand_args)

        self.spawn_point = None

    def activate(self):
        # check that enought time is bassed from spawning
        if not self.activation_timer.is_time_passed() and self.logic_state.state != tank_state.LogicStateEnum.ACTIVATING:
            return

        self.logic_state.state = tank_state.LogicStateEnum.ACTIVE
        self.broadcast_command("activate_tank", ())

    def create_effect_description_game_object(self, index, time_in_sec, effect_end_function=None):
        inventory = False # TODO: find out what this does
        effect_description_global_game_object = self.global_space.add_global_game_object("effect_description")
        effect_description_global_game_object.add_global_model(effect_description_global_model.EffectDescriptionGlobalModel, model_args=(index, inventory, self.global_game_object.id))
        effect_description_global_game_object.add_global_model(duration_controller_global_model.DurationControllerGlobalModel, model_args=(time_in_sec, effect_end_function,))
        effect_description_global_game_object.clone_to_clients()
        effect_description_global_game_object.load_object_from_clients()
        self.effect_description_global_game_objects_by_index[index] = effect_description_global_game_object
        return effect_description_global_game_object

    def full_effect_timer(self, index, time_in_sec, effect_end_function):
        if not index in self.effect_description_global_game_objects_by_index: return
        effect_description_global_game_object = self.effect_description_global_game_objects_by_index[index]
        effect_description_global_game_object.get_global_model(duration_controller_global_model.DurationControllerGlobalModel).destroy()
        self.create_effect_description_game_object(index, time_in_sec, effect_end_function)

    def deactivate_first_aid(self):
        self.effect_description_global_game_objects_by_index.pop(FIRST_AID_EFFECT_INDEX)

    def activate_first_aid_effect(self):
        if FIRST_AID_EFFECT_INDEX in self.effect_description_global_game_objects_by_index:
            return

        effect_description_global_game_object = self.create_effect_description_game_object(index=FIRST_AID_EFFECT_INDEX, time_in_sec=server_properties.FIRST_AID_EFFECT_TIME_IN_SEC, effect_end_function=self.deactivate_first_aid)

        thread = threading.Thread(target=self.first_aid_heal_effect, args=(effect_description_global_game_object,))
        thread.start()

    def first_aid_heal_effect(self, effect_description_global_game_object):
        self.first_aid_heal_effect_activated = True
        healed = 0
        max_health = self.tank_model_cc.max_health

        while self.health < max_health:
            self.add_health(server_properties.FIRST_AID_HEAL_STEP_HP)
            healed += server_properties.FIRST_AID_HEAL_STEP_HP
            if self.health > max_health and healed > max_health: break
            time.sleep(server_properties.FIRST_AID_HEAL_STEPPING_SPEED_IN_SECONDS)

        self.reset_effect(effect_description_global_game_object)
        self.first_aid_heal_effect_activated = False

    def deactivate_double_armor_effect(self):
        self.double_armor_effect_activated = False
        self.effect_description_global_game_objects_by_index.pop(DOUBLE_ARMOR_EFFECT_INDEX)

    def activate_double_armor_effect(self):
        if DOUBLE_ARMOR_EFFECT_INDEX in self.effect_description_global_game_objects_by_index:
            self.full_effect_timer(DOUBLE_ARMOR_EFFECT_INDEX, server_properties.DOUBLE_ARMOR_EFFECT_TIME_IN_SEC, self.deactivate_double_armor_effect)
            return

        self.create_effect_description_game_object(index=DOUBLE_ARMOR_EFFECT_INDEX, time_in_sec=server_properties.DOUBLE_ARMOR_EFFECT_TIME_IN_SEC, effect_end_function=self.deactivate_double_armor_effect)
        self.double_armor_effect_activated = True

    def deactivate_double_power_effect(self):
        self.double_power_effect_activated = False
        self.effect_description_global_game_objects_by_index.pop(DOUBLE_POWER_EFFECT_INDEX)

    def activate_double_power_effect(self):
        if DOUBLE_POWER_EFFECT_INDEX in self.effect_description_global_game_objects_by_index:
            self.full_effect_timer(DOUBLE_POWER_EFFECT_INDEX, server_properties.DOUBLE_POWER_EFFECT_TIME_IN_SEC, self.deactivate_double_power_effect)
            return

        self.create_effect_description_game_object(index=DOUBLE_POWER_EFFECT_INDEX, time_in_sec=server_properties.DOUBLE_POWER_EFFECT_TIME_IN_SEC, effect_end_function=self.deactivate_double_power_effect)
        self.double_power_effect_activated = True

    def deactivate_nitro_effect(self):
        self.specification.reset_tank_speed()
        self.effect_description_global_game_objects_by_index.pop(NITRO_EFFECT_INDEX)

    def activate_nitro_effect(self):
        if NITRO_EFFECT_INDEX in self.effect_description_global_game_objects_by_index:
            self.full_effect_timer(NITRO_EFFECT_INDEX, server_properties.NITRO_EFFECT_TIME_IN_SEC, self.deactivate_nitro_effect)
            return

        self.nitro_effect_activated = True
        self.create_effect_description_game_object(index=NITRO_EFFECT_INDEX, time_in_sec=server_properties.NITRO_EFFECT_TIME_IN_SEC, effect_end_function=self.deactivate_nitro_effect)
        self.specification.set_tank_speed_with_factor(server_properties.NITRO_SPEED_COEFFICIENT)

    def drop_mine(self):
        self.battle_mines_global_model.add_mine(self)

class TemperatureChangeTask:
    def __init__(self, temp_return_rate, owner_tank_global_model, burn_damage_min, burn_damage_max, temperature_limit, turret_max_freezing, body_max_freezing, protection_name):
        self.temperature = 0
        self.temp_return_rate = temp_return_rate
        self.owner_tank_global_model = owner_tank_global_model
        self.burn_damage_min = burn_damage_min
        self.burn_damage_max = burn_damage_max
        self.turret_max_freezing = turret_max_freezing
        self.body_max_freezing = body_max_freezing
        self.temperature_limit = temperature_limit
        self.protection_name = protection_name


class Temperature:
    def __init__(self, tank_global_model):
        self.tank_global_model = tank_global_model
        self.temperature_change_task_by_id = {}
        self.create_thread()
        self.temperature = 0

        self.create_thread()

    def create_thread(self):
        thread = threading.Thread(target=self.apply_temperature_effects, args=())
        thread.start()

    def create_temperature_change_task(self, cooling_rate, temperature_limit, burn_damage_min, burn_damage_max, turret_max_freezing, body_max_freezing, protection_name):
        temperature_change_task = TemperatureChangeTask(cooling_rate, self.tank_global_model, burn_damage_min, burn_damage_max, temperature_limit, turret_max_freezing, body_max_freezing, protection_name)
        return temperature_change_task

    def add_temperature(self, add_temperature, temperature_change_task_id, temperature_change_task_creation_function):

        def get_temperature_change_task():
            if not temperature_change_task_id in self.temperature_change_task_by_id:
                temperature_change_task = temperature_change_task_creation_function()
                self.temperature_change_task_by_id[temperature_change_task_id] = temperature_change_task
                return temperature_change_task

            temperature_change_task = self.temperature_change_task_by_id[temperature_change_task_id]
            return temperature_change_task

        temperature_change_task = get_temperature_change_task()

        add_temperature = own_math.trim_add_value(self.temperature, add_temperature, temperature_change_task.temperature_limit)
        self.temperature += add_temperature
        temperature_change_task.temperature += add_temperature

    def reset_temperature(self):
        for temperature_change_task in list(self.temperature_change_task_by_id.values()):
            temperature_change_task.temperature = 0

        self.temperature_change_task_by_id = {}
        self.temperature = 0

    def apply_temperature_effects(self):
        _time = 0

        def apply_burn_effect(temperature_change_task):
            # this if statement will make sure that we will apply burn damage only once per second
            if not _time % 1 == 0: return

            damage_factor = temperature_change_task.temperature / temperature_change_task.temperature_limit
            damage = temperature_change_task.burn_damage_min + (temperature_change_task.burn_damage_max - temperature_change_task.burn_damage_min) * damage_factor
            self.tank_global_model.damage_tank(damage, temperature_change_task.owner_tank_global_model, temperature_change_task.protection_name)

        def apply_cold_effect(temperature_change_task):
            freezing_factor = temperature_change_task.temperature / temperature_change_task.temperature_limit

            print("temp:", temperature_change_task.temperature, "freezing_factor:", freezing_factor)

            turret_freezing_factor = own_math.map_factor_to_range(_from=1, to=temperature_change_task.turret_max_freezing, factor=freezing_factor)
            body_freezing_factor = own_math.map_factor_to_range(_from=1, to=temperature_change_task.body_max_freezing, factor=freezing_factor)

            self.tank_global_model.specification.set_tank_speed_with_factors(
                speed_factor=body_freezing_factor,
                turn_speed_factor=body_freezing_factor,
                turret_rotation_speed_factor=turret_freezing_factor,
                acceleration_factor=body_freezing_factor
            )

        while True:
            time.sleep(server_properties.TEMPERATURE_UPDATE_DELAY)
            _time += server_properties.TEMPERATURE_UPDATE_DELAY

            for _id, temperature_change_task in self.temperature_change_task_by_id.copy().items():
                if temperature_change_task.temperature == 0:
                    self.temperature_change_task_by_id.pop(_id)
                    continue

                subtract_temperature = temperature_change_task.temp_return_rate * server_properties.TEMPERATURE_UPDATE_DELAY
                subtract_temperature = own_math.trim_subtract_value(temperature_change_task.temperature, subtract_temperature, 0)

                self.temperature -= subtract_temperature
                temperature_change_task.temperature -= subtract_temperature
                self.tank_global_model.set_temperature(self.temperature * server_properties.TEMPERATURE_CHANGE_FACTOR)

                if temperature_change_task.temperature > 0:
                    apply_burn_effect(temperature_change_task)

                if temperature_change_task.temperature < 0:
                    apply_cold_effect(temperature_change_task)


class TankSpecification:
    def __init__(self, tank_global_model, speed, turn_speed, turret_rotation_speed, acceleration, specification_id=0):
        self.tank_global_model = tank_global_model
        self.tank_model_cc = tank_global_model.tank_model_cc
        self.set_specification_data(speed, turn_speed, turret_rotation_speed, acceleration, specification_id)

    def set_specification_data(self, speed, turn_speed, turret_rotation_speed, acceleration, specification_id):
        self.speed = speed
        self.turn_speed = turn_speed 
        self.turret_rotation_speed = turret_rotation_speed 
        self.acceleration = acceleration 
        self.specification_id = specification_id

    def set_specification(self, speed, turn_speed, turret_rotation_speed, acceleration, specification_id=0):
        self.set_specification_data(speed, turn_speed, turret_rotation_speed, acceleration, specification_id)
        self.tank_global_model.broadcast_command("set_specification", (speed, turn_speed, turret_rotation_speed, acceleration, specification_id))

    def reset_tank_speed(self):
        speed = self.tank_model_cc.tank_initialization_data.speed
        turn_speed = self.tank_model_cc.tank_initialization_data.turn_speed
        turret_rotation_speed = self.tank_model_cc.tank_initialization_data.turret_rotation_speed
        acceleration = self.tank_model_cc.tank_initialization_data.acceleration
        self.set_specification(speed, turn_speed, turret_rotation_speed, acceleration)

    def set_tank_speed_with_factor(self, speed_factor):
        tank_initialization_data = self.tank_model_cc.tank_initialization_data

        speed = tank_initialization_data.speed * speed_factor
        turn_speed = tank_initialization_data.turn_speed * speed_factor
        turret_rotation_speed = tank_initialization_data.turret_rotation_speed * speed_factor
        acceleration = tank_initialization_data.acceleration * speed_factor
        self.set_specification(speed, turn_speed, turret_rotation_speed, acceleration)

    def set_tank_speed_with_factors(self, speed_factor=1, turn_speed_factor=1, turret_rotation_speed_factor=1, acceleration_factor=1):
        tank_initialization_data = self.tank_model_cc.tank_initialization_data

        speed = tank_initialization_data.speed * speed_factor
        turn_speed = tank_initialization_data.turn_speed * turn_speed_factor
        turret_rotation_speed = tank_initialization_data.turret_rotation_speed * turret_rotation_speed_factor
        acceleration = tank_initialization_data.acceleration * acceleration_factor
        self.set_specification(speed, turn_speed, turret_rotation_speed, acceleration)

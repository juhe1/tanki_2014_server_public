from global_models.battle.bonus.bonus_common_global_model import bonus_common_global_model
from global_models.battle.common.battle_field_global_model import battle_field_global_model
from client.layouts.lobby.models.user_property_model import user_property_model
from global_models.battle.bonus.bonus_common_global_model import bonus_common_model_cc
from client.layouts.battle.models.battle_field_bonus_model import battle_field_bonus_model
from global_models.battle.bonus.bonus_notification_global_model import bonus_notification_model_cc
from global_models.battle.bonus.bonus_notification_global_model import bonus_notification_global_model
from global_models.battle.common.tank_global_model import tank_global_model
from loaders.client_resource_loader import client_resource_loader
from global_models.battle.bonus import bonus
from loaders.map_loader.map_info import BonusType
from space.global_model import GlobalModel
from . import battle_field_bonus_model_cc
from utils.time.timer import Timer
import server_properties

import threading
import datetime
import random
import time

class BattleFieldBonusGlobalModel(GlobalModel):

    CLIENT_MODEL = battle_field_bonus_model.BattleFieldBonusModel

    def __init__(self, global_game_object, global_space, owner_id=None):
        super().__init__(global_game_object, global_space, owner_id)

        self.battle_field_bonus_model_cc = self.create_cc()
        self.battle_field_global_model = global_game_object.get_global_model(battle_field_global_model.BattleFieldGlobalModel)

        self.bonus_common_global_model_by_bonus_type = {}
        self.bonuses_by_id = {}
        self.bonus_current_id = 0
        self.num_fund_changes_from_last_crystal_drop = 0

        self.gold_notification_global_model = None

        self.create_bonus_common_game_objects()
        self.init_supplie_box_spawners()
        self.create_notification_game_objects()

    def create_notification_game_objects(self):
        bonus_notification_cc = bonus_notification_model_cc.BonusNotificationModelCC()
        bonus_notification_cc.sound_notification = client_resource_loader.get_resource_id("/battle/sounds/gold")
        bonus_notification_cc.notification_message = server_properties.GOLD_NOTIFICATION_MESSAGE

        gold_notification_global_game_object = self.global_space.add_global_game_object("gold_notification")
        self.gold_notification_global_model = gold_notification_global_game_object.add_global_model(bonus_notification_global_model.BonusNotificationGlobalModel, model_args=(bonus_notification_cc,))

    def create_bonus_common_game_objects(self):
        self.bonus_common_global_model_by_bonus_type[BonusType.ARMOR_BOX] = self.create_bonus_common_global_model(BonusType.ARMOR_BOX, "/battle/3ds/bonuses/armor_box")
        self.bonus_common_global_model_by_bonus_type[BonusType.CRYSTAL_BOX] = self.create_bonus_common_global_model(BonusType.CRYSTAL_BOX, "/battle/3ds/bonuses/crystal_box")
        self.bonus_common_global_model_by_bonus_type[BonusType.GOLD_BOX] = self.create_bonus_common_global_model(BonusType.GOLD_BOX, "/battle/3ds/bonuses/gold_box")
        self.bonus_common_global_model_by_bonus_type[BonusType.MED_BOX] = self.create_bonus_common_global_model(BonusType.MED_BOX, "/battle/3ds/bonuses/med_box")
        self.bonus_common_global_model_by_bonus_type[BonusType.NOS_BOX] = self.create_bonus_common_global_model(BonusType.NOS_BOX, "/battle/3ds/bonuses/nos_box")
        self.bonus_common_global_model_by_bonus_type[BonusType.POWER_BOX] = self.create_bonus_common_global_model(BonusType.POWER_BOX, "/battle/3ds/bonuses/power_box")

    def create_bonus_common_global_model(self, bonus_type, resource_name):
        bonus_common_global_game_object = self.global_space.add_global_game_object("bonus")
        bonus_common_cc = bonus_common_model_cc.BonusCommonModelCC()
        bonus_common_cc.box_resource = client_resource_loader.get_resource_id(resource_name)
        _bonus_common_global_model = bonus_common_global_game_object.add_global_model(bonus_common_global_model.BonusCommonGlobalModel, model_args=(bonus_common_cc, bonus_type,))
        return _bonus_common_global_model

    def generate_new_bonus_id(self):
        if self.bonus_current_id >= 0xffffffff:
            self.bonus_current_id = 0

        self.bonus_current_id += 1
        return self.bonus_current_id

    def get_all_bonuses(self):
        return list(self.bonuses_by_id.values())

    def remove_all_bonuses(self):
        for bonus in self.get_all_bonuses():
            bonus.destroy()

        self.bonuses_by_id = {}

    def remove_bonus(self, bonus_id):
        if not self.remove_bonus_from_server(bonus_id): return
        self.broadcast_command("remove_bonuses", ([bonus_id],))

    def remove_bonus_from_server(self, bonus_id):
        if not bonus_id in self.bonuses_by_id: return False
        self.bonuses_by_id.pop(bonus_id)
        return True

    def spawn_bonus(self, bonus_common_global_model):
        bonus_id = self.generate_new_bonus_id()
        _bonus = bonus.Bonus(bonus_id, bonus_common_global_model, self.remove_bonus)

        if _bonus.spawn_position == None:
            return

        self.bonuses_by_id[_bonus.bonus_id] = _bonus
        self.broadcast_command("spawn_bonuses", ([_bonus],))

    def get_random_supplie_bonus_type(self):
        supplie_bonus_types = [BonusType.ARMOR_BOX, BonusType.MED_BOX, BonusType.NOS_BOX, BonusType.POWER_BOX]
        return random.choice(supplie_bonus_types)

    def init_supplie_box_spawners(self):
        thread = threading.Thread(target=self.spawn_supplie_boxes_loop)
        thread.start()

    # TODO: stop this loop when model is removed
    def spawn_supplie_boxes_loop(self):
        while True:
            time.sleep(server_properties.SUPPLIE_BOX_SPAWN_TIME_IN_SEC)

            random_supplie_bonus_global_model = self.bonus_common_global_model_by_bonus_type[self.get_random_supplie_bonus_type()]
            self.spawn_bonus(random_supplie_bonus_global_model)

    def attempt_to_take_bonus(self, bonus_id, user_id):
        user_tank_global_model = self.global_space.get_global_model(tank_global_model.TankGlobalModel, global_game_object_id=user_id)

        if user_tank_global_model == None: return
        if not bonus_id in self.bonuses_by_id: return

        bonus = self.bonuses_by_id[bonus_id]
        bonus_type = bonus.bonus_type

        if bonus_type == BonusType.MED_BOX:
            user_tank_global_model.activate_first_aid_effect()

        if bonus_type == BonusType.ARMOR_BOX:
            user_tank_global_model.activate_double_armor_effect()

        if bonus_type == BonusType.POWER_BOX:
            user_tank_global_model.activate_double_power_effect()

        if bonus_type == BonusType.NOS_BOX:
            user_tank_global_model.activate_nitro_effect()

        if bonus_type == BonusType.GOLD_BOX:
            self.gold_taken(user_id)

        if bonus_type == BonusType.CRYSTAL_BOX:
            self.add_crystals_to_user_id(user_id, server_properties.CRYSTAL_BOX_REWARD)

        self.remove_bonus_from_server(bonus_id)
        self.broadcast_command("bonus_taken", (bonus_id,))

    def battle_fund_changed(self):
        self.try_drop_gold()
        self.try_drop_crystal_box()

    def add_crystals_to_user_id(self, user_id, crystals):
        client_object = self.battle_field_global_model.get_client_objects_by_user_id(user_id)
        _user_property_model = client_object.client_space_registry.get_model(user_property_model.UserPropertyModel, game_object_name="panel", space_name="lobby")
        _user_property_model.add_crystals(crystals)

    def gold_taken(self, user_id):
        self.broadcast_command("gold_taken", (user_id,))
        self.add_crystals_to_user_id(user_id, server_properties.GOLD_BOX_REWARD)
    
    def spawn_gold(self):
        bonus_common_model = self.bonus_common_global_model_by_bonus_type[BonusType.GOLD_BOX]
        self.spawn_bonus(bonus_common_model)

    def try_drop_gold(self):
        random_number = random.randint(1, server_properties.GOLD_BOX_DROP_PROBABILITY)
        if random_number != 1: return
        
        self.gold_notification_global_model.send_notification()

        timer = threading.Timer(server_properties.GOLD_DROP_TIME, self.spawn_gold)
        timer.start()

    def try_drop_crystal_box(self):
        self.num_fund_changes_from_last_crystal_drop += 1

        if self.num_fund_changes_from_last_crystal_drop >= server_properties.NUM_FUND_CHANGES_FOR_CRYSTAL_DROP:
            bonus_common_model = self.bonus_common_global_model_by_bonus_type[BonusType.CRYSTAL_BOX]
            self.spawn_bonus(bonus_common_model)

    def create_cc(self):
        _battle_field_bonus_model_cc = battle_field_bonus_model_cc.BattleFieldBonusModelCC()
        _battle_field_bonus_model_cc.bonus_fall_speed = server_properties.BONUS_FALL_SPEED
        return _battle_field_bonus_model_cc

    def get_model_data(self):
        self.battle_field_bonus_model_cc.bonuses = list(self.bonuses_by_id.values())
        return self.battle_field_bonus_model_cc

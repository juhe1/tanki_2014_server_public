from global_models.battle.common.tank_global_model.team import Team
from panda3d.core import Vec3
from enum import IntEnum

import random

class MapInfo:
    def __init__(self):
        self.map_id = 0
        self.name_en = ""
        self.name_ru = ""
        self.max_people = 0
        self.preview_image = 0
        self.rank_limit_max = 0
        self.rank_limit_min = 0
        self.map_theme = ""
        self.supported_modes = []
        self.sky_box = ""
        self.sky_box_revolution_axis = None
        self.sky_box_revolution_speed = 0.0
        self.map_resource = ""
        self.environment_sound = ""
        self.graphics_settings = ""
        self.gravity = 0.0
        self.collision_geometry = None

        self.blue_spawns = []
        self.red_spawns = []
        self.dm_spawns = []

        self.bonus_region_dictionarys_by_battle_mode = {} # example: {DM:{ARMOR_BOX:[BonusRegion()], GOLD_BOX:[BonusRegion()]}}

    def get_spawns_by_team(self, _team):
        if _team == Team.NONE:
            return self.dm_spawns
        if _team == Team.RED:
            return self.red_spawns
        if _team == Team.BLUE:
            return self.blue_spawns

    def get_bonus_regions_by_battle_mode_and_bonus_type(self, battle_mode, bonus_type):
        if not battle_mode in self.bonus_region_dictionarys_by_battle_mode: return []
        bonus_regions_by_bonus_type = self.bonus_region_dictionarys_by_battle_mode[battle_mode]
        if not bonus_type in bonus_regions_by_bonus_type: return []
        return bonus_regions_by_bonus_type[bonus_type]

class SpawnPoint:
    position = None
    rotation = None
    type = None

def bonus_type_string_to_enum(bonus_type_string):
    if bonus_type_string == "armorup":
        return BonusType.ARMOR_BOX

    if bonus_type_string == "crystal":
        return BonusType.CRYSTAL_BOX

    if bonus_type_string == "crystal_100":
        return BonusType.GOLD_BOX

    if bonus_type_string == "medkit":
        return BonusType.MED_BOX

    if bonus_type_string == "nitro":
        return BonusType.NOS_BOX

    if bonus_type_string == "damageup":
        return BonusType.POWER_BOX

class BonusType(IntEnum):
    ARMOR_BOX = 0
    CRYSTAL_BOX = 1
    GOLD_BOX = 2
    MED_BOX = 3
    NOS_BOX = 4
    POWER_BOX = 5

class BonusRegion:
    def __init__(self):
        self.min = None
        self.max = None
        self.free = True
        self.name = ""
        self.bonus_types = []

    def calculate_random_spawn_position(self):
        vector = Vec3()
        vector.x = random.uniform(self.min.x, self.max.x)
        vector.y = random.uniform(self.min.y, self.max.y)
        vector.z = random.uniform(self.min.z, self.max.z)
        return vector

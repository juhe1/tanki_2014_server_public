import math

class GarageItemData:
    def __init__(self): # we init, because we want to make new lists for each object
        self.id = 0
        self.name = ""
        self.description = ""

        self.position = 0
        self.min_rank = 0
        self.max_rank = 0
        self.preview_image = ""
        self.count = None

        self.discount = None
        self.discount_image = None

        self.modification_index = None
        self.base_item_id = None

        self.item_category = ""
        self.object_3ds = None
        self.price = None
        self.data_owner_id = None
        self.coloring = None

        self.properties = []
        self.upgradable_property_datas = []

        self.kit_image = ""
        self.kit_items = []
        self.kit_discount = 0

        self.temporary_item_life_time_in_sec = None
        self.temporary_item_remaining_time_in_sec = None

        self.sfx_data = None
        self.weapon_data = None
        self.lighting_effects = []
        self.bcsh_data = []
        self.color_transform_structs = []
        self.weapon_weakening_data = None
        self.discrete_shot_data = None
        self.stream_weapon_data = None
        self.tank_physics = None

    def get_upgradable_property_data_by_id(self, property_id):
        for upgradable_property_data in self.upgradable_property_datas:
            if upgradable_property_data.property_id == property_id:
                return upgradable_property_data

    def get_upgradable_property_data_by_property_name(self, property_name):
        for upgradable_property_data in self.upgradable_property_datas:
            if upgradable_property_data.property_name == property_name:
                return upgradable_property_data

    def get_property(self, property_name):
        for property in self.properties:
            if property.item_property == property_name:
                return property

    def get_all_property_names(self):
        return [property.item_property for property in self.properties]


class TankPhysics:
    hull_side_acceleration = 0
    hull_turn_acceleration = 0
    hull_reverse_turn_acceleration = 0
    hull_reverse_acceleration = 0
    hull_damping = 0
    hull_size = None

class FlameThrowingSfxModelData:
    fire_texture = None
    flame_sound = None
    muzzle_plane_texture = None

class FlameThrowerData:
    cone_angle = 0
    heating_rate = 0
    cooling_rate = 0
    burn_damage_max = 0
    burn_damage_min = 0

class FreezeData:
    cone_angle = 0
    freezing_speed = 0
    defrosting_speed = 0
    turret_max_freezing = 0
    body_max_freezing = 0
    min_temperature = 0

class FreezeSfxData:
    particle_speed = 0
    particle_texture = 0
    plane_texture = 0
    shot_sound = 0

class ShaftData:
    after_shot_pause = None
    fast_shot_energy = None
    initial_fov = None
    jitter_angle_max = None
    jitter_angle_min = None
    jitter_intencity_max = None
    jitter_intencity_min = None
    jitter_start_point = None
    max_energy = None
    minimum_fov = None
    reticle_image = None
    shrubs_hiding_radius_max = None
    shrubs_hiding_radius_min = None
    targeting_acceleration = None
    targeting_transition_time = None
    weakening_coeff = None

class ShaftSfxData:
    explosion_sound = None
    explosion_texture = None
    hit_mark_texture = None
    muzzle_flash_texture = None
    shot_sound = None
    targeting_sound = None
    trail_texture = None
    zoom_mode_sound = None

class SmokySfxData:
    critical_hit_size = 0
    critical_hit_texture = ""
    explosion_size = 0
    explosion_mark_texture = ""
    explosion_sound = ""
    explosion_texture = ""
    shot_sound = ""
    shot_texture = ""


class KitItem:
    def __init__(self):
        self.item = 0
        self.count = 0
        self.mount = False


class DiscountItem:
    def __init__(self):
        self.discount = 0
        self.item = 0


class Property:
    def __init__(self):
        self.final_value = 0
        self.initial_value = 0
        self.item_property = ""
        self.upgradable_property_id = None # this tells that what upgradable_property will affect this property


class UpgradablePropertyData:
    def __init__(self):
        self.id = 0
        self.cost = None
        self.importance = 0
        self.level = 0
        self.max_level = 0
        self.property_id = 0
        self.property_name = ""
        self.properties = None
        self.speed_up_discount = 0
        self.time_discount = 0
        self.time = None
        self.upgrade_discount = 0


class DiscreteShotData:
    auto_aiming_angle_down = 0
    auto_aiming_angle_up = 0


class StreamWeaponData:
    energy_capacity = 0
    weapon_tick_interval_msec = 0


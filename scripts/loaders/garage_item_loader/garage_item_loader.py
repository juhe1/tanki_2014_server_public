from client.layouts.garage.garage_utils import name_to_id
from loaders.garage_item_loader import garage_item_data
from utils.data_types import linear_param
from utils.log import console_out
from panda3d.core import Vec3

from loaders import loader_utils
from loaders import json_loader

items = {}
role_specific_items = {}
moddable_item_grouped_by_base_id = {}

def get_items_by_base_id(base_id):
    global moddable_item_grouped_by_base_id
    return moddable_item_grouped_by_base_id[base_id]

def get_item_by_id(item_id):
    global items
    return items[item_id]

def get_item_by_data_owner_id(data_owner_id):
    global items
    for item in items.values():
        if item.data_owner_id == data_owner_id:
            return item

def get_friend_items(item_id):
    global moddable_item_grouped_by_base_id
    item = get_item_by_id(item_id)
    item_base_id = item.base_item_id
    return moddable_item_grouped_by_base_id[item_base_id]

def get_item_by_base_id_and_mod_idx(base_id, modification_index):
    global moddable_item_grouped_by_base_id
    for modification_item in moddable_item_grouped_by_base_id[base_id]:
        if modification_item.modification_index == modification_index:
            return modification_item

def get_all_items_for_role(roles):
    global items
    global role_specific_items
    role_specific_items = []

    for role in roles:
        if role in role_specific_items:
            role_specific_items += list(role_specific_items[role].values())
    return list(items.values()) + role_specific_items

def dictionary_to_vec3(dict):
    return Vec3(dict["x"], dict["y"], dict["z"])

def item_json_to_item_object(item_dictionary):
    global moddable_item_grouped_by_base_id
    global role_specific_items
    global items

    item = garage_item_data.GarageItemData()
    item.id = item_dictionary["id"]
    if "description" in item_dictionary:
        item.name = item_dictionary["description"]["name"]
        item.description = item_dictionary["description"]["description"]

    if "item_info" in item_dictionary:
        item.position = item_dictionary["item_info"]["position"]
        item.min_rank = item_dictionary["item_info"]["min_rank"]
        item.max_rank = item_dictionary["item_info"]["max_rank"]
        item.preview_image = item_dictionary["item_info"]["preview_image"]

    if "discount" in item_dictionary:
        item.discount = item_dictionary["discount"]["discount"]
        item.discount_image = item_dictionary["discount"]["discount_image"]

    if "modification" in item_dictionary:
        item.modification_index = item_dictionary["modification"]["modification_index"]
        item.base_item_id = item_dictionary["modification"]["base_item_id"]
        if not item.base_item_id in moddable_item_grouped_by_base_id:
            moddable_item_grouped_by_base_id[item.base_item_id] = []
        moddable_item_grouped_by_base_id[item.base_item_id].append(item)

    if "temporary_data" in item_dictionary:
        item.temporary_item_life_time_in_sec = item_dictionary["temporary_data"]["life_time_in_sec"]
        item.temporary_item_remaining_time_in_sec = item_dictionary["temporary_data"]["remaining_time_in_sec"]

    if "item_category" in item_dictionary:
        item.item_category = item_dictionary["item_category"]

    if "object_3ds" in item_dictionary:
        item.object_3ds = item_dictionary["object_3ds"]

    if "price" in item_dictionary:
        item.price = item_dictionary["price"]

    if "data_owner_id" in item_dictionary:
        item.data_owner_id = item_dictionary["data_owner_id"]

    if "coloring" in item_dictionary:
        item.coloring = item_dictionary["coloring"]

    if "count" in item_dictionary:
        item.count = item_dictionary["count"]

    if "kit" in item_dictionary:
        item.kit_image = item_dictionary["kit"]["image"]
        item.kit_discount = item_dictionary["kit"]["discount"]
        for kit_item in item_dictionary["kit"]["kit_items"]:
            kit_item_object = garage_item_data.KitItem()
            kit_item_object.item = kit_item["item"]
            kit_item_object.count = kit_item["count"]
            kit_item_object.mount = kit_item["mount"]
            item.kit_items.append(kit_item_object)

    if "unlisted_properties" in item_dictionary:
        for property in item_dictionary["unlisted_properties"]:
            property_object = garage_item_data.Property()
            property_object.final_value = property["final_value"]
            property_object.initial_value = property["initial_value"]
            property_object.item_property = property["item_property"]
            item.unlisted_properties.append(property_object)

    if "properties" in item_dictionary:
        for property in item_dictionary["properties"]:
            property_object = garage_item_data.Property()
            property_object.final_value = property["final_value"]
            property_object.initial_value = property["initial_value"]
            property_object.item_property = property["item_property"]
            if "upgradable_property" in property:
                property_object.upgradable_property_id = name_to_id.item_garage_property_name_to_id(property["upgradable_property"])
            item.properties.append(property_object)

    if "upgradable_property_datas" in item_dictionary:
        for upgradable_property_data in item_dictionary["upgradable_property_datas"]:
            upgradable_property_data_object = garage_item_data.UpgradablePropertyData()
            upgradable_property_data_object.id = upgradable_property_data["id"]
            upgradable_property_data_object.importance = upgradable_property_data["importance"]
            upgradable_property_data_object.level = upgradable_property_data["level"]
            upgradable_property_data_object.max_level = upgradable_property_data["max_level"]
            upgradable_property_data_object.property_id = name_to_id.item_garage_property_name_to_id(upgradable_property_data["property"])
            upgradable_property_data_object.property_name = upgradable_property_data["property"]
            upgradable_property_data_object.speed_up_discount = upgradable_property_data["speed_up_discount"]
            upgradable_property_data_object.time_discount = upgradable_property_data["time_discount"]
            upgradable_property_data_object.upgrade_discount = upgradable_property_data["upgrade_discount"]

            if "properties" in upgradable_property_data:
                upgradable_property_data_object.properties = []
                for property in upgradable_property_data["properties"]:
                    upgradable_property_data_object.properties.append(item.get_property(property))

            upgradable_property_data_object.cost = linear_param.LinearParam()
            upgradable_property_data_object.cost.initial_number = upgradable_property_data["cost"]["initial_number"]
            upgradable_property_data_object.cost.step = upgradable_property_data["cost"]["step"]

            upgradable_property_data_object.time = linear_param.LinearParam()
            upgradable_property_data_object.time.initial_number = upgradable_property_data["time_params"]["initial_number"]
            upgradable_property_data_object.time.step = upgradable_property_data["time_params"]["step"]
            item.upgradable_property_datas.append(upgradable_property_data_object)

    if "role_specific_item" in item_dictionary:
        role = item_dictionary["role_specific_item"]
        if not role in role_specific_items:
            role_specific_items[role] = {}
        role_specific_items[role][item.id] = item
        return

    if "flame_thrower_sfx_data" in item_dictionary:
        flame_thrower_sfx_data_json = item_dictionary["flame_thrower_sfx_data"]
        item.sfx_data = garage_item_data.FlameThrowingSfxModelData()
        item.sfx_data.fire_texture = flame_thrower_sfx_data_json["fire_texture"]
        item.sfx_data.flame_sound = flame_thrower_sfx_data_json["flame_sound"]
        item.sfx_data.muzzle_plane_texture = flame_thrower_sfx_data_json["muzzle_plane_texture"]

    if "smoky_sfx_data" in item_dictionary:
        smoky_sfx_data_json = item_dictionary["smoky_sfx_data"]
        item.sfx_data = garage_item_data.SmokySfxData()
        item.sfx_data.critical_hit_size = smoky_sfx_data_json["critical_hit_size"]
        item.sfx_data.critical_hit_texture = smoky_sfx_data_json["critical_hit_texture"]
        item.sfx_data.explosion_size = smoky_sfx_data_json["explosion_size"]
        item.sfx_data.explosion_mark_texture = smoky_sfx_data_json["explosion_mark_texture"]
        item.sfx_data.explosion_sound = smoky_sfx_data_json["explosion_sound"]
        item.sfx_data.explosion_texture = smoky_sfx_data_json["explosion_texture"]
        item.sfx_data.shot_sound = smoky_sfx_data_json["shot_sound"]
        item.sfx_data.shot_texture = smoky_sfx_data_json["shot_texture"]

    if "shaft_sfx_data" in item_dictionary:
        shaft_sfx_data_json = item_dictionary["shaft_sfx_data"]
        item.sfx_data = garage_item_data.ShaftSfxData()
        item.sfx_data.explosion_sound = shaft_sfx_data_json["explosion_sound"]
        item.sfx_data.explosion_texture = shaft_sfx_data_json["explosion_texture"]
        item.sfx_data.hit_mark_texture = shaft_sfx_data_json["hit_mark_texture"]
        item.sfx_data.muzzle_flash_texture = shaft_sfx_data_json["muzzle_flash_texture"]
        item.sfx_data.shot_sound = shaft_sfx_data_json["shot_sound"]
        item.sfx_data.targeting_sound = shaft_sfx_data_json["targeting_sound"]
        item.sfx_data.trail_texture = shaft_sfx_data_json["trail_texture"]
        item.sfx_data.zoom_mode_sound = shaft_sfx_data_json["zoom_mode_sound"]

    if "shaft_data" in item_dictionary:
        shaft_data_json = item_dictionary["shaft_data"]
        item.weapon_data = garage_item_data.ShaftData()
        item.weapon_data.after_shot_pause = shaft_data_json["after_shot_pause"]
        item.weapon_data.fast_shot_energy = shaft_data_json["fast_shot_energy"]
        item.weapon_data.initial_fov = shaft_data_json["initial_fov"]
        item.weapon_data.jitter_angle_max = shaft_data_json["jitter_angle_max"]
        item.weapon_data.jitter_angle_min = shaft_data_json["jitter_angle_min"]
        item.weapon_data.jitter_intencity_max = shaft_data_json["jitter_intencity_max"]
        item.weapon_data.jitter_intencity_min = shaft_data_json["jitter_angle_max"]
        item.weapon_data.jitter_start_point = shaft_data_json["jitter_start_point"]
        item.weapon_data.max_energy = shaft_data_json["max_energy"]
        item.weapon_data.minimum_fov = shaft_data_json["minimum_fov"]
        item.weapon_data.reticle_image = shaft_data_json["reticle_image"]
        item.weapon_data.shrubs_hiding_radius_max = shaft_data_json["shrubs_hiding_radius_max"]
        item.weapon_data.shrubs_hiding_radius_min = shaft_data_json["shrubs_hiding_radius_min"]
        item.weapon_data.targeting_acceleration = shaft_data_json["targeting_acceleration"]
        item.weapon_data.targeting_transition_time = shaft_data_json["targeting_transition_time"]
        item.weapon_data.weakening_coeff = shaft_data_json["weakening_coeff"]

    if "freeze_sfx_data" in item_dictionary:
        freeze_sfx_data_json = item_dictionary["freeze_sfx_data"]
        item.sfx_data = garage_item_data.FreezeSfxData()
        item.sfx_data.particle_speed = freeze_sfx_data_json["particle_speed"]
        item.sfx_data.particle_texture = freeze_sfx_data_json["particle_texture"]
        item.sfx_data.plane_texture = freeze_sfx_data_json["plane_texture"]
        item.sfx_data.shot_sound = freeze_sfx_data_json["shot_sound"]

    if "freeze_data" in item_dictionary:
        freeze_data_json = item_dictionary["freeze_data"]
        item.weapon_data = garage_item_data.FreezeData()
        item.weapon_data.cone_angle = freeze_data_json["cone_angle"]
        item.weapon_data.freezing_speed = freeze_data_json["freezing_speed"]
        item.weapon_data.defrosting_speed = freeze_data_json["defrosting_speed"]
        item.weapon_data.turret_max_freezing = freeze_data_json["turret_max_freezing"]
        item.weapon_data.body_max_freezing = freeze_data_json["body_max_freezing"]
        item.weapon_data.min_temperature = freeze_data_json["min_temperature"]

    if "flame_thrower_data" in item_dictionary:
        flame_thrower_data_json = item_dictionary["flame_thrower_data"]
        item.weapon_data = garage_item_data.FlameThrowerData()
        item.weapon_data.cone_angle = flame_thrower_data_json["cone_angle"]
        item.weapon_data.heating_rate = flame_thrower_data_json["heating_rate"]
        item.weapon_data.cooling_rate = flame_thrower_data_json["cooling_rate"]
        item.weapon_data.burn_damage_min = flame_thrower_data_json["burn_damage_min"]
        item.weapon_data.burn_damage_max = flame_thrower_data_json["burn_damage_max"]

    if "tank_physics" in item_dictionary:
        tank_physics_json = item_dictionary["tank_physics"]
        item.tank_physics = garage_item_data.TankPhysics()
        item.tank_physics.hull_side_acceleration = tank_physics_json["hull_side_acceleration"]
        item.tank_physics.hull_turn_acceleration = tank_physics_json["hull_turn_acceleration"]
        item.tank_physics.hull_reverse_turn_acceleration = tank_physics_json["hull_reverse_turn_acceleration"]
        item.tank_physics.hull_reverse_acceleration = tank_physics_json["hull_reverse_acceleration"]
        item.tank_physics.hull_damping = tank_physics_json["hull_damping"]
        item.tank_physics.hull_size = dictionary_to_vec3(tank_physics_json["hull_size"])

    if "discrete_shot_data" in item_dictionary:
        discrete_shot_data_json = item_dictionary["discrete_shot_data"]
        item.discrete_shot_data = garage_item_data.DiscreteShotData()
        item.discrete_shot_data.auto_aiming_angle_down = discrete_shot_data_json["auto_aiming_angle_down"]
        item.discrete_shot_data.auto_aiming_angle_up = discrete_shot_data_json["auto_aiming_angle_up"]

    if "stream_weapon_data" in item_dictionary:
        stream_weapon_data_json = item_dictionary["stream_weapon_data"]
        item.stream_weapon_data = garage_item_data.StreamWeaponData()
        item.stream_weapon_data.energy_capacity = stream_weapon_data_json["energy_capacity"]
        item.stream_weapon_data.weapon_tick_interval_msec = stream_weapon_data_json["weapon_tick_interval_msec"]

    if "lighting" in item_dictionary:
        for lighting_effect_dic in item_dictionary["lighting"]:
            new_lighting_effect = loader_utils.dictionary_to_lighting_effect(lighting_effect_dic)
            item.lighting_effects.append(new_lighting_effect)

    if "bcsh" in item_dictionary:
        for bcsh_dic in item_dictionary["bcsh"]:
            new_bcsh_data = loader_utils.dictionary_to_bcsh_data(bcsh_dic)
            item.bcsh_data.append(new_bcsh_data)

    if "color_transform" in item_dictionary:
        for color_transform_dic in item_dictionary["color_transform"]:
            new_color_transform_struct = loader_utils.dictionary_to_color_transform_struct(color_transform_dic)
            item.color_transform_structs.append(new_color_transform_struct)

    items[item.id] = item

    mod_string = ""
    if item.modification_index != None:
        mod_string = "_m" + str(item.modification_index)
    console_out.color_print("[GARAGE_ITEM_LOADER] ITEM_LOADED: " + item.name + mod_string, "yellow")

def load_items_from_json(path):
    items_json_datas = json_loader.get_jsons_inside_folder(path)
    # this basicly loops all items that we want to convert to item object
    for items_json in items_json_datas:
        for item in list(items_json.values())[0]:
            if "modifications" in item:
                for modification_item in item["modifications"]:
                    item_json_to_item_object(modification_item)
                continue
            item_json_to_item_object(item)

    console_out.safe_print("")

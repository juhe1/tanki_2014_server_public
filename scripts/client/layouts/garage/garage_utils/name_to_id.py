# this file contains functions for convertting name to ids and ids to names that are found inside garage code.
from utils.log import console_out

def item_category_enum_name_to_id(name):
    if name == "weapon":
        return 0
    if name == "armor":
        return 1
    if name == "color":
        return 2
    if name == "inventory":
        return 3
    if name == "plugin":
        return 4
    if name == "kit":
        return 5
    if name == "emblem":
        return 6
    console_out.log_color_print("[ERROR] item_category_enum not found: " + str(name), "red")

###########################
#  UPGRADABLE_PROPERTIES  #
###########################

# in client code these propertyes are located in _codec.projects.tanks.client.garage.models.item.properties.CodecItemGarageProperty
garage_property_to_id_dic = {
    "hull_armor":1,
    "hull_speed":2,
    "hull_turn_speed":3,
    "hull_power":4,
    "hull_mass":5,
    "firebird_resistance":20,
    "smoky_resistance":21,
    "twins_resistance":22,
    "railgun_resistance":23,
    "isis_resistance":24,
    "mine_resistance":25,
    "thunder_resistance":26,
    "freeze_resistance":27,
    "ricochet_resistance":28,
    "shaft_resistance":29,
    "damage":40,
    "damage_per_second":41,
    "weapon_cooldown_time":42,
    "aiming_mode_cooldown_time":43,
    "critical_hit_chance":44,
    "critical_hit_damage":45,
    "shot_range":46,
    "turret_turn_speed":47,
    "aiming_error":48,
    "shot_area":49,
    "cone_angle":50,
    "charging_time":51,
    "fire_damage":52,
    "weapon_weakening_coeff":53,
    "isis_radius":54,
    "isis_damage":55,
    "isis_healing_per_second":56,
    "isis_self_healing_percent":57,
    "aiming_mode_damage":58,
    "aiming_weapon_discharge_rate":59,
    "shaft_aimed_shot_impact":60,
    "shaft_targeting_speed":61,
    "shaft_arcade_damage":62,
    "weapon_impact_force":63,
    "weapon_kickback":64,
    "weapon_reticle_speed":65,
    "weapon_charge_rate":66,
    "weapon_min_damage_percent":67,
    "thunder_min_splash_damage_percent":68
}

def item_garage_property_name_to_id(name):
    return garage_property_to_id_dic[name]

property_id_to_name = {v: k for k, v in garage_property_to_id_dic.items()} # this makes the dictionary look like this {51:"energy_per_shot"} instead {"energy_per_shot":51}

def item_garage_property_id_to_name(id):
    return property_id_to_name[id]


################
#  PROPERTIES  #
################

item_property_name_to_id_dic = {
    "hull_armor":0,
    "hull_speed":1,
    "hull_side_acceleration":2,
    "hull_turn_speed":3,
    "hull_turn_acceleration":4,
    "hull_reverse_turn_acceleration":5,
    "hull_acceleration":6,
    "hull_reverse_acceleration":7,
    "hull_mass":8,
    "turret_turn_speed":9,
    "turret_rotation_acceleration":10,
    "impact_force":11,
    "damage_from":12,
    "damage_to":13,
    "weapon_reload_time":14,
    "weapon_charging_time":15,
    "weapon_weakening_coeff":16,
    "firebird_resistance":17,
    "smoky_resistance":18,
    "twins_resistance":19,
    "railgun_resistance":20,
    "isis_resistance":21,
    "mine_resistance":22,
    "thunder_resistance":23,
    "freeze_resistance":24,
    "ricochet_resistance":25,
    "shaft_resistance":26,
    "shaft_aiming_mode_min_damage":27,
    "shaft_aiming_mode_max_damage":28,
    "shaft_vertical_targeting_speed":29,
    "shaft_horizontal_targeting_speed":30,
    "shaft_aiming_mode_charge_rate":31,
    "shaft_aimed_shot_impact":32,
    "shaft_rotation_deceleration_coeff":33,
    "weapon_charge_rate":34,
    "weapon_kickback":35,
    "weapon_min_damage_percent":36,
    "weapon_min_damage_radius":37,
    "weapon_max_damage_radius":38,
    "critical_hit_chance":39,
    "critical_hit_damage":40,
    "thunder_min_splash_damage_percent":41,
    "thunder_splash_damage_impact":42,
    "weapon_discharge_rate":43,
    "damage_per_period":44,
    "isis_healing_per_period":45,
    "isis_self_healing_percent":46,
    "isis_radius":47,
    "flame_temperature_limit":48,
    "weapon_reticle_speed":49,
    "weapon_reticle_radius":50,
    "energy_per_shot":51
}

def item_property_name_to_id(name):
    return item_property_name_to_id_dic[name]

item_property_id_to_name_dic = {v: k for k, v in item_property_name_to_id_dic.items()}

def item_property_id_to_name(id):
    return item_property_id_to_name_dic[id]

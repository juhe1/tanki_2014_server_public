from loaders.client_resource_loader import client_resource_loader
from . import graphics_settings

from utils.log import console_out
from loaders import json_loader

import binascii
import struct
import copy
import sys

graphics_settings_by_name = {}

def get_graphics_settings_by_name(name):
    global graphics_settings_by_name
    return graphics_settings_by_name[name]

def load_all_graphics_settings(path):
    global graphics_settings_by_name
    graphics_settings_by_name = {}
    graphics_settings_json_datas = json_loader.get_jsons_inside_folder(path)

    for graphics_settings_json in graphics_settings_json_datas:
        new_graphics_settings = graphics_settings.GraphicsSettings()
        new_graphics_settings.name = graphics_settings_json["name"]
        new_graphics_settings.ssao_color = int(graphics_settings_json["ssao_color"], 16)

        dust_params_json = graphics_settings_json["dust_params"]
        new_graphics_settings.dust_params.alpha = dust_params_json["alpha"]
        new_graphics_settings.dust_params.density = dust_params_json["density"]
        new_graphics_settings.dust_params.dust_far_distance = dust_params_json["dust_far_distance"]
        new_graphics_settings.dust_params.dust_near_distance = dust_params_json["dust_near_distance"]
        new_graphics_settings.dust_params.dust_particle = client_resource_loader.get_resource_id(dust_params_json["dust_particle"])
        new_graphics_settings.dust_params.dust_size = dust_params_json["dust_size"]

        dynamic_shadow_params_json = graphics_settings_json["dynamic_shadow_params"]
        new_graphics_settings.dynamic_shadow_params.angle_x = dynamic_shadow_params_json["angle_x"]
        new_graphics_settings.dynamic_shadow_params.angle_y = dynamic_shadow_params_json["angle_y"]
        new_graphics_settings.dynamic_shadow_params.light_color = int(dynamic_shadow_params_json["light_color"], 16)
        new_graphics_settings.dynamic_shadow_params.shadow_color = int(dynamic_shadow_params_json["shadow_color"], 16)

        fog_params_json = graphics_settings_json["fog_params"]
        new_graphics_settings.fog_params.alpha = fog_params_json["alpha"]
        new_graphics_settings.fog_params.color = int(fog_params_json["color"], 16)
        new_graphics_settings.fog_params.far_limit = fog_params_json["far_limit"]
        new_graphics_settings.fog_params.near_limit = fog_params_json["near_limit"]

        graphics_settings_by_name[new_graphics_settings.name] = new_graphics_settings
        console_out.color_print("[GRAPHICS_SETTINGS_LOADER] GRAPHICS_SETTING_LOADED: " + new_graphics_settings.name, "yellow")

    console_out.safe_print("")

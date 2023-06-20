from utils.collision.collision_geometry.collision_geometry import CollisionGeometry
from utils.collision.collision_geometry.collision_triangle import CollisionTriangle
from utils.collision.collision_geometry.collision_plane import CollisionPlane
from utils.collision.collision_geometry.collision_box import CollisionBox
from loaders.client_resource_loader import client_resource_loader
from client.layouts.battle_list.battle_data import battle_theme
from client.layouts.battle_list.battle_data import battle_mode
from global_models.battle.common.tank_global_model import team
from panda3d.core import Vec3
from utils.log import console_out
from loaders import json_loader
from . import map_info

from xml.dom import minidom

maps_by_id = {}
maps_by_name_and_theme = {}

def get_map_by_id(id):
    global maps_by_id
    return maps_by_id[id]

def get_all_maps():
    global maps_by_id
    return list( maps_by_id.values() )

def get_map_by_name_and_theme(name, theme):
    global maps_by_name_and_theme
    return maps_by_name_and_theme[(name, theme)]

def read_vector3_from_element(element):
    x = element.getElementsByTagName("x")
    y = element.getElementsByTagName("y")
    z = element.getElementsByTagName("z")
    vector = Vec3()

    if len(x) != 0:
        vector.x = float(x[0].childNodes[0].nodeValue)

    if len(y) != 0:
        vector.y = float(y[0].childNodes[0].nodeValue)

    if len(z) != 0:
        vector.z = float(z[0].childNodes[0].nodeValue)

    return vector

def parse_spawn_points(new_map_info, dom):
    spawn_points = dom.getElementsByTagName("spawn-point")

    for spawn_point in spawn_points:
        type = spawn_point.getAttribute("type")

        pos = spawn_point.getElementsByTagName("position")[0]
        rot = spawn_point.getElementsByTagName("rotation")[0]

        spawn_point = map_info.SpawnPoint()
        spawn_point.position = read_vector3_from_element(pos)
        spawn_point.position.z += 100
        spawn_point.rotation = read_vector3_from_element(rot)
        spawn_point.type = team.string_to_team(type)

        if spawn_point.type == team.Team.NONE:
            new_map_info.dm_spawns.append(spawn_point)
            continue
        if spawn_point.type == team.Team.RED:
            new_map_info.red_spawns.append(spawn_point)
            continue
        if spawn_point.type == team.Team.BLUE:
            new_map_info.blue_spawns.append(spawn_point)

def add_bonus_region_to_map_info(map_info, bonus_region, game_modes, bonus_types):
    for game_mode in game_modes:
        if not game_mode in map_info.bonus_region_dictionarys_by_battle_mode:
            map_info.bonus_region_dictionarys_by_battle_mode[game_mode] = {}

        bonus_regions_by_bonus_type = map_info.bonus_region_dictionarys_by_battle_mode[game_mode]

        for bonus_type in bonus_types:
            if not bonus_type in bonus_regions_by_bonus_type:
                bonus_regions_by_bonus_type[bonus_type] = []

            bonus_regions = bonus_regions_by_bonus_type[bonus_type]
            bonus_regions.append(bonus_region)

def parse_bonus_regions(new_map_info, dom):
    bonus_regions = dom.getElementsByTagName("bonus-region")

    for bonus_region in bonus_regions:
        bonus_region_object = map_info.BonusRegion()
        bonus_region_object.name = bonus_region.getAttribute("name")
        bonus_region_object.free = bonus_region.getAttribute("free")

        min_element = bonus_region.getElementsByTagName("min")[0]
        max_element = bonus_region.getElementsByTagName("max")[0]
        bonus_region_object.min = read_vector3_from_element(min_element)
        bonus_region_object.max = read_vector3_from_element(max_element)

        game_modes = [battle_mode.battle_mode_string_to_enum(game_mode.childNodes[0].nodeValue) for game_mode in bonus_region.getElementsByTagName("game-mode")]
        bonus_types = [map_info.bonus_type_string_to_enum(game_mode.childNodes[0].nodeValue) for game_mode in bonus_region.getElementsByTagName("bonus-type")]
        add_bonus_region_to_map_info(new_map_info, bonus_region_object, game_modes, bonus_types)

def parse_collision_boxes(collision_geometry_element):
    collision_box_elements = collision_geometry_element.getElementsByTagName("collision-box")
    collision_boxes = []

    for collision_box_element in collision_box_elements:
        collision_box_size_element = collision_box_element.getElementsByTagName("size")[0]
        collision_box_position_element = collision_box_element.getElementsByTagName("position")[0]
        collision_box_rotation_element = collision_box_element.getElementsByTagName("rotation")[0]

        size = read_vector3_from_element(collision_box_size_element)

        position = read_vector3_from_element(collision_box_position_element)
        rotation = read_vector3_from_element(collision_box_rotation_element)

        collision_box = CollisionBox(size, position, rotation)
        collision_boxes.append(collision_box)

    return collision_boxes


def parse_collision_planes(collision_geometry_element):
    collision_plane_elements = collision_geometry_element.getElementsByTagName("collision-plane")
    collision_planes = []

    for collision_plane_element in collision_plane_elements:
        collision_plane_rotation_element = collision_plane_element.getElementsByTagName("rotation")[0]
        collision_plane_position_element = collision_plane_element.getElementsByTagName("position")[0]

        width = float(collision_plane_element.getElementsByTagName("width")[0].childNodes[0].nodeValue)
        length = float(collision_plane_element.getElementsByTagName("length")[0].childNodes[0].nodeValue)
        position = read_vector3_from_element(collision_plane_position_element)
        rotation = read_vector3_from_element(collision_plane_rotation_element)

        collision_plane = CollisionPlane(width, length, position, rotation)
        collision_planes.append(collision_plane)

    return collision_planes

def parse_collision_triangles(collision_geometry_element):
    collision_triangle_elements = collision_geometry_element.getElementsByTagName("collision-triangle")
    collision_triangles = []

    for collision_triangle_element in collision_triangle_elements:
        vertex0_element = collision_triangle_element.getElementsByTagName("v0")[0]
        vertex1_element = collision_triangle_element.getElementsByTagName("v1")[0]
        vertex2_element = collision_triangle_element.getElementsByTagName("v2")[0]
        collision_triangle_position_element = collision_triangle_element.getElementsByTagName("position")[0]
        collision_triangle_rotation_element = collision_triangle_element.getElementsByTagName("rotation")[0]

        vertices = []
        vertices.append(read_vector3_from_element(vertex0_element))
        vertices.append(read_vector3_from_element(vertex1_element))
        vertices.append(read_vector3_from_element(vertex2_element))
        position = read_vector3_from_element(collision_triangle_position_element)
        rotation = read_vector3_from_element(collision_triangle_rotation_element)

        collision_triangle = CollisionTriangle(vertices, position, rotation)
        collision_triangles.append(collision_triangle)

    return collision_triangles

def parse_collision_geometry(new_map_info, dom):
    collision_geometry_element = dom.getElementsByTagName("collision-geometry")[0]

    collision_geometry = CollisionGeometry()
    collision_geometry.collision_boxes = parse_collision_boxes(collision_geometry_element)
    collision_geometry.collision_planes = parse_collision_planes(collision_geometry_element)
    collision_geometry.collision_triangles = parse_collision_triangles(collision_geometry_element)
    new_map_info.collision_geometry = collision_geometry
    collision_geometry.create_new_physics_word()

def load_all_maps():
    global maps_by_id, maps_by_name_and_theme

    maps_by_id = {}
    maps_by_name_and_theme = {}
    maps_json = json_loader.get_json_file_data("maps.json")

    for map_dictionary in maps_json["maps"]:
        new_map_info = map_info.MapInfo()
        new_map_info.map_id = map_dictionary["map_id"]
        new_map_info.name_en = map_dictionary["name_en"]
        new_map_info.name_ru = map_dictionary["name_ru"]
        new_map_info.max_people = map_dictionary["max_people"]
        new_map_info.preview_image = client_resource_loader.get_resource_id(map_dictionary["preview_image"])
        new_map_info.rank_limit_max = map_dictionary["rank_limit_max"]
        new_map_info.rank_limit_min = map_dictionary["rank_limit_min"]
        new_map_info.theme = battle_theme.battle_theme_string_to_enum(map_dictionary["theme"])
        new_map_info.supported_modes = [battle_mode.battle_mode_string_to_enum(mode) for mode in map_dictionary["supported_modes"]]
        new_map_info.sky_box = client_resource_loader.get_resource_id(map_dictionary["sky_box"])
        sky_box_revolution_axis_json = map_dictionary["sky_box_revolution_axis"]
        new_map_info.sky_box_revolution_axis = Vec3(sky_box_revolution_axis_json["x"], sky_box_revolution_axis_json["y"], sky_box_revolution_axis_json["z"])
        new_map_info.sky_box_revolution_speed = map_dictionary["sky_box_revolution_speed"]
        new_map_info.map_resource = client_resource_loader.get_resource_id(map_dictionary["map_resource"])
        new_map_info.map_resource_path = map_dictionary["map_resource"]
        new_map_info.environment_sound = client_resource_loader.get_resource_id(map_dictionary["environment_sound"])
        new_map_info.graphics_settings = map_dictionary["graphics_settings"]
        new_map_info.gravity = map_dictionary["gravity"]

        dom = minidom.parse("configs/maps/" + map_dictionary["map_xml"])
        parse_spawn_points(new_map_info, dom)
        parse_bonus_regions(new_map_info, dom)
        parse_collision_geometry(new_map_info, dom)

        maps_by_id[new_map_info.map_id] = new_map_info
        key = (new_map_info.name_en, new_map_info.map_theme)
        maps_by_name_and_theme[key] = new_map_info

        console_out.color_print("[MAP_LOADER] MAP_LOADED: " + new_map_info.name_en, "yellow")

    console_out.safe_print("")

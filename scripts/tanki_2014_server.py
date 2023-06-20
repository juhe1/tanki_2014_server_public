from global_models.battle_list.common.battle_select_global_model import battle_select_global_model
from global_models.lobby.rank_notifier_global_model import rank_notifier_global_model
from global_models.lobby.uid_notifier_global_model import uid_notifier_global_model
from loaders.graphics_settings_loader import graphics_settings_loader
from loaders.client_resource_loader import client_resource_loader
from loaders.garage_item_loader import garage_item_loader
from loaders.map_loader import map_loader
from space import global_space_registry
from utils.log import console_out
from loaders import json_loader
from database import database
import connection_handler
import server_properties
import game

def main():
    console_out.log_print('server is started')

    init_loaders()
    database.connect_to_database()
    create_spaces()
    connection_handler.init()
    create_global_game_objects()

    # this will run all panda3d stuff
    #run()

def init_loaders():
    json_loader.load_json_files(server_properties.CONFIG_DIRECTORY)
    client_resource_loader.init()
    garage_item_loader.load_items_from_json(server_properties.GARAGE_ITEMS_FOLDER)
    graphics_settings_loader.load_all_graphics_settings(server_properties.GRAPHICS_SETTINGS_FOLDER)
    map_loader.load_all_maps()

def create_spaces():
    global_space_registry.add_space(id=1, name="entrance")
    global_space_registry.add_space(id=2, name="lobby")
    global_space_registry.add_space(id=3, name="garage")
    global_space_registry.add_space(id=4, name="battle_select")

def create_global_game_objects():
    lobby_select_space = global_space_registry.get_space_by_name("lobby")
    default_global_game_object = lobby_select_space.add_global_game_object("panel")
    default_global_game_object.add_global_model(uid_notifier_global_model.UidNotifierGlobalModel)
    default_global_game_object.add_global_model(rank_notifier_global_model.RankNotifierGlobalModel)

    battle_select_space = global_space_registry.get_space_by_name("battle_select")
    default_global_game_object = battle_select_space.get_default_global_game_object()
    default_global_game_object.add_global_model(battle_select_global_model.BattleSelectGlobalModel)

main()

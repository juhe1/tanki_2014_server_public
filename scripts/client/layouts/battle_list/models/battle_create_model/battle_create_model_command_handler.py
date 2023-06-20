from global_models.battle_list.common.battle_select_global_model import battle_select_global_model
from client.layouts.battle_list import battle_list_codecs
from utils.binary.codecs import basic_codecs
from space import global_space_registry
from database import battles_table

class BattleCreateModelCommandHandler:
    def __init__(self, battle_create_model, battle_select_model, client_object):
        self.battle_select_model = battle_select_model
        self.battle_create_model = battle_create_model
        self.client_object = client_object

        self.CHECK_BATTLE_NAME_FOR_FORBIDDEN_WORDS_COMMAND_ID = 300090000
        self.CREATE_BATTLE_COMMAND_ID = 300090001

    def handle_command(self, binary_data, command_id):
        if command_id == self.CHECK_BATTLE_NAME_FOR_FORBIDDEN_WORDS_COMMAND_ID:
            self.check_battle_name_for_forbidden_words(binary_data)
            return True

        if command_id == self.CREATE_BATTLE_COMMAND_ID:
            self.create_battle(binary_data)
            return True

    def filter_battle_name(self, battle_name):
        # TODO: filter battle name
        return battle_name

    def check_battle_name_for_forbidden_words(self, binary_data):
        battle_name = basic_codecs.StringCodec.decode(binary_data)
        battle_name = self.filter_battle_name(battle_name)
        self.battle_create_model.commands.set_filtered_battle_name(battle_name)

    def create_battle(self, binary_data):
        if not self.battle_select_model.loaded:
            return

        battle_data = battle_list_codecs.BattleCreateCodec.decode(binary_data)
        battle_data.battle_creator_client_object = self.client_object

        # TODO: check battle data
        battle_data.name = self.filter_battle_name(battle_data.name)

        _battle_select_global_model = global_space_registry.get_global_model(battle_select_global_model.BattleSelectGlobalModel, global_game_object_name="default_game_object", global_space_name="battle_select")
        battle_item_global_game_object = _battle_select_global_model.create_new_battle(battle_data)
        battles_table.add_new_battle(battle_data)

        self.battle_select_model.show_battle(battle_item_global_game_object.id)

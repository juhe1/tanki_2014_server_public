from client.layouts.lobby.models.lobby_layout_model import lobby_layout_model
from utils.binary.codecs import basic_codecs
from global_models.battle.common.tank_global_model.team import Team

class BattleDmInfoModelCommandHandler:
    def __init__(self, client_object, battle_field_global_space):
        self.client_object = client_object
        self.battle_field_global_space = battle_field_global_space

        self.FIGHT_COMMAND_ID = 300090007

    def handle_command(self, binary_data, command_id):
        if command_id == self.FIGHT_COMMAND_ID:
            self.fight()
            return True

    def fight(self):
        _lobby_layout_model = self.client_object.client_space_registry.get_model(space_name="lobby", model=lobby_layout_model.LobbyLayoutModel, game_object_name="default_game_object")
        _lobby_layout_model.show_battle(self.battle_field_global_space, Team.NONE)

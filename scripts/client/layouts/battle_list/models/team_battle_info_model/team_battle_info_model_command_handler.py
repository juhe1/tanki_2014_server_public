from client.layouts.lobby.models.lobby_layout_model import lobby_layout_model
from client.layouts.battle_list import battle_list_codecs
from utils.binary.codecs import basic_codecs
from global_models.battle.common.tank_global_model.team import Team

class TeamBattleInfoModelCommandHandler:
    def __init__(self, client_object, battle_field_global_space):
        self.client_object = client_object
        self.battle_field_global_space = battle_field_global_space

        self.FIGHT_COMMAND_ID = 300090028

    def handle_command(self, binary_data, command_id):
        if command_id == self.FIGHT_COMMAND_ID:
            self.fight(binary_data)
            return True

    def fight(self, binary_data):
        team = battle_list_codecs.TeamCodec.decode(binary_data)

        _lobby_layout_model = self.client_object.client_space_registry.get_model(space_name="lobby", model=lobby_layout_model.LobbyLayoutModel, game_object_name="default_game_object")
        _lobby_layout_model.show_battle(self.battle_field_global_space, team)

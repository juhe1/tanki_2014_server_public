from utils.binary.codecs import basic_codecs

class BattleSelectModelCommandHandler:
    def __init__(self, battle_select_model):
        self.battle_select_model = battle_select_model

        self.ON_BATTLE_SELECT = 300090024

    def handle_command(self, binary_data, command_id):
        if command_id == self.ON_BATTLE_SELECT:
            self.on_battle_select(binary_data)
            return True

    def on_battle_select(self, binary_data):
        battle_game_object_id = basic_codecs.LongCodec.decode(binary_data)
        self.battle_select_model.show_battle(battle_game_object_id)

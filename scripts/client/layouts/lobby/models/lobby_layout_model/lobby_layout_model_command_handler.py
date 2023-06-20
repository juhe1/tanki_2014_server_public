class LobbyLayoutModelCommandHandler:
    def __init__(self, lobby_layout_model):
        self.lobby_layout_model = lobby_layout_model
        self.SHOW_GARAGE_COMMAND_ID = 300070009
        self.SHOW_BATTLE_SELECT_COMMAND_ID = 300070008

    def handle_command(self, binary_data, command_id):
        if command_id == self.SHOW_GARAGE_COMMAND_ID:
            self.lobby_layout_model.show_garage()
            return True

        if command_id == self.SHOW_BATTLE_SELECT_COMMAND_ID:
            self.lobby_layout_model.show_battle_select()
            return True

        return False

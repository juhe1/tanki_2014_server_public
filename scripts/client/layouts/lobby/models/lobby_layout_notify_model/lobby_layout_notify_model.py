from client.layouts.lobby.models.lobby_layout_notify_model import lobby_layout_notify_model_commands
from client.layouts.lobby.models.lobby_layout_model import lobby_layout_model
from client.space.model import Model

class LobbyLayoutNotifyModel(Model):
    model_id = 300070012

    def __init__(self, game_object, client_space, client_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

        self.model_data = None
        self.commands = lobby_layout_notify_model_commands.LobbyLayoutNotifyModelCommands(client_space, game_object)
        self.command_handler = None

        self._lobby_layout_model = game_object.get_model(lobby_layout_model.LobbyLayoutModel)

    def end_layout_switch(self):
        active_layout_enum = self._lobby_layout_model.get_active_layout_enum()
        self.commands.end_layout_switch(active_layout_enum)

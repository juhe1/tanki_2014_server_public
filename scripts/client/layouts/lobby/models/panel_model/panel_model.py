from client.layouts.lobby.models.user_email_and_password_model import user_email_and_password_model
from client.layouts.lobby.models.upgrading_items_model import upgrading_items_model
from client.layouts.lobby.models.user_property_model import user_property_model
from client.layouts.lobby.models.user_notifier_model import user_notifier_model
from client.layouts.lobby.models.uid_notifier_model import uid_notifier_model
from client.layouts.lobby.models.lobby_layout_model import lobby_layout_model
from client.layouts.lobby.models.settings_model import settings_model
from client.layouts.garage.models.garage_model import garage_model
from client.space.model import Model

class PanelModel(Model):
    model_id = 300050032

    def __init__(self, game_object, client_space, client_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)
        
        self.model_data = None
        self.commands = None
        self.command_handler = None

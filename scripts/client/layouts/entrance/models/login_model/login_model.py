from client.layouts.lobby.models.user_email_and_password_model import user_email_and_password_model
from global_models.battle_list.common.battle_select_global_model import battle_select_global_model
from client.layouts.lobby.models.lobby_layout_notify_model import lobby_layout_notify_model
from global_models.battle.common.battle_field_global_model import battle_field_global_model
from client.layouts.lobby.models.upgrading_items_model import upgrading_items_model
from client.layouts.entrance.models.login_model import login_model_command_handler
from client.layouts.lobby.models.user_property_model import user_property_model
from client.layouts.lobby.models.user_notifier_model import user_notifier_model
from client.layouts.lobby.models.uid_notifier_model import uid_notifier_model
from client.layouts.lobby.models.lobby_layout_model import lobby_layout_model
from client.layouts.lobby.models.gpu_detector_model import gpu_detector_model
from client.layouts.entrance.models.login_model import login_model_commands
from client.layouts.lobby.models.settings_model import settings_model
from client.layouts.lobby.models.panel_model import panel_model
from client.layouts.lobby.lobby_enums import Layout
from space import global_space_registry
from client.space.model import Model
from client.space import game_object
from client import ranks

import datetime
import time

class LoginModel(Model):
    model_id = 300020020

    def __init__(self, game_object, client_space, client_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

        self.lobby_layout_object = None

        self.model_data = None
        self.commands = login_model_commands.LoginModelCommands(client_space, game_object)
        self.command_handler = login_model_command_handler.LoginModelCommandHandler(self)

    def create_lobby_layout_game_object(self, lobby_space):
        lobby_layout_object = lobby_space.get_default_game_object()
        lobby_layout_object.add_model(lobby_layout_model.LobbyLayoutModel)
        lobby_layout_object.add_model(lobby_layout_notify_model.LobbyLayoutNotifyModel)
        lobby_layout_object.add_model(gpu_detector_model.GpuDetectorModel)

        lobby_space.load_unloaded_game_objects_from_client()
        return lobby_layout_object

    def unload_entrance(self, lobby_layout_object):
        lobby_layout_notify_model_commands = lobby_layout_object.get_model(lobby_layout_notify_model.LobbyLayoutNotifyModel).commands
        lobby_layout_notify_model_commands.begin_layout_switch(Layout.BATTLE_SELECT)
        self.client_object.client_space_registry.get_space_by_name("entrance").remove_space()

    def create_panel_game_object(self, lobby_space, username):
        panel_game_object = lobby_space.clone_game_object_from_global_space("panel")
        panel_game_object.add_model(panel_model.PanelModel)
        panel_game_object.add_model(user_property_model.UserPropertyModel, model_args=(username,))
        panel_game_object.add_model(user_notifier_model.UserNotifierModel)
        panel_game_object.add_model(settings_model.SettingsModel)
        panel_game_object.add_model(user_email_and_password_model.UserEmailAndPasswordModel)
        panel_game_object.add_model(upgrading_items_model.UpgradingItemsModel)
        panel_game_object.load_object_from_client()
        return panel_game_object

    def init_upgrading_items(self, panel_object):
        _upgrading_items_model = panel_object.get_model(upgrading_items_model.UpgradingItemsModel)
        _upgrading_items_model.init()

    def load_battle(self, team, battle_id):
        _lobby_layout_model = self.lobby_layout_object.get_model(lobby_layout_model.LobbyLayoutModel)
        battle_global_space = global_space_registry.get_space_by_name("battle_field_" + str(battle_id))
        _lobby_layout_model.show_battle(battle_global_space, team)

    def load_lobby(self):
        _lobby_layout_model = self.lobby_layout_object.get_model(lobby_layout_model.LobbyLayoutModel)
        _lobby_layout_model.show_battle_select()

    def load_next_layout(self):
        _battle_select_global_model = global_space_registry.get_global_model(battle_select_global_model.BattleSelectGlobalModel, global_game_object_name="default_game_object", global_space_name="battle_select")
        user_id = self.client_object.user_id
        placeholder_info = _battle_select_global_model.get_placeholder_info(user_id)

        if placeholder_info:
            self.load_battle(placeholder_info.team, placeholder_info.battle_id)
            return

        self.load_lobby()

    def login(self, username):
        lobby_space = self.client_object.basic_commands.open_space("lobby")
        self.lobby_layout_object = self.create_lobby_layout_game_object(lobby_space)
        self.unload_entrance(self.lobby_layout_object)
        panel_game_object = self.create_panel_game_object(lobby_space, username)
        self.init_upgrading_items(panel_game_object)
        self.load_next_layout()
        # TODO: update last visit date from database

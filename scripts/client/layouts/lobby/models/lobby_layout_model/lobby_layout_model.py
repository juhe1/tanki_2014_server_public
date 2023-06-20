from client.layouts.lobby.models.lobby_layout_model import lobby_layout_model_command_handler
from client.layouts.lobby.models.lobby_layout_notify_model import lobby_layout_notify_model
from client.layouts.battle_list.models.battle_select_model import battle_select_model
from global_models.battle.common.battle_field_global_model import battle_field_global_model
from client.layouts.lobby.models.lobby_layout_model import lobby_layout_model_data
from client.layouts.garage.models.garage_model import garage_model
from client.layouts.lobby.lobby_enums import Layout
from client.space.model import Model
from client.space import game_object

class LobbyLayoutModel(Model):
    model_id = 300070010

    def __init__(self, game_object, client_space, client_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

        self.command_handler = lobby_layout_model_command_handler.LobbyLayoutModelCommandHandler(self)
        self.model_data = lobby_layout_model_data.LobbyLayoutModelData(game_object)
        self.commands = None

        self.active_layout = None

    def get_active_layout_enum(self):
        return self.active_layout

    def unload_battle_layout(self):
        battle_global_space = self.client_object.current_battle_global_space
        _battle_field_global_model = battle_global_space.get_global_model(battle_field_global_model.BattleFieldGlobalModel, global_game_object_name="default_game_object")
        _battle_field_global_model.leave_battle(self.client_object.user_id)
        self.client_object.client_space_registry.get_space_by_id(battle_global_space.id).remove_space()

    def unload_current_layout(self):
        if self.active_layout == Layout.GARAGE:
            self.client_object.client_space_registry.get_space_by_name("garage").remove_space()

        if self.active_layout == Layout.BATTLE_SELECT:
            self.client_object.client_space_registry.get_space_by_name("battle_select").remove_space()

        if self.active_layout == Layout.BATTLE:
            self.unload_battle_layout()

    def show_garage(self):
        self.unload_current_layout()

        self.active_layout = Layout.GARAGE
         # connect client to garge space
        self.client_object.basic_commands.open_space("garage")

        garage_space = self.client_object.client_space_registry.get_space_by_name("garage")
        garage_object = garage_space.get_default_game_object()
        garage_object.add_model(garage_model.GarageModel)
        self.garage_model = garage_object.get_model(garage_model.GarageModel)

    def show_battle_select(self):
        self.unload_current_layout()
        self.active_layout = Layout.BATTLE_SELECT

        # load battle_list
        self.client_object.basic_commands.open_space("battle_select") # connect client to battle_list space
        battle_list_space = self.client_object.client_space_registry.get_space_by_name("battle_select")
        battle_list_space.clone_game_object_from_global_space("default_game_object")

    def show_battle(self, battle_field_global_space, team):
        lobby_layout_notify_model_commands = self.game_object.get_model(lobby_layout_notify_model.LobbyLayoutNotifyModel).commands
        lobby_layout_notify_model_commands.begin_layout_switch(Layout.BATTLE)
        self.unload_current_layout()
        self.active_layout = Layout.BATTLE

        # add user to battle
        battle_field_model = battle_field_global_space.get_global_model(battle_field_global_model.BattleFieldGlobalModel, global_game_object_name="default_game_object")
        if battle_field_model.try_join(team, self.client_object) == False:
            return

        # load battle
        battle_field_client_space = self.client_object.client_space_registry.add_global_space(battle_field_global_space)
        self.client_object.current_battle_global_space = battle_field_global_space

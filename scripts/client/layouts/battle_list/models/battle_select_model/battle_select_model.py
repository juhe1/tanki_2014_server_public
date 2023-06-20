from client.layouts.lobby.models.lobby_layout_notify_model import lobby_layout_notify_model
from client.layouts.battle_list.models.pro_battle_info_model import pro_battle_info_model
from global_models.battle_list.common.battle_item_global_model import battle_item_global_model
from client.layouts.battle_list.models.battle_create_model import battle_create_model
from client.layouts.lobby.models.user_property_model import user_property_model
from client.layouts.lobby.lobby_enums import UserRole
from . import battle_select_model_command_handler
from . import battle_select_model_commands
from space import global_space_registry
from client.space.model import Model

class BattleSelectModel(Model):
    model_id = 300090011

    def __init__(self, game_object, client_space, client_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

        self.loaded = False
        self.showing_battle = None
        self.user_property_model_data = self.client_object.client_space_registry.get_model(space_name="lobby", game_object_name="panel", model=user_property_model.UserPropertyModel).model_data

        self.model_data = None
        self.commands = battle_select_model_commands.BattleSelectModelCommands(client_space, game_object)
        self.command_handler = battle_select_model_command_handler.BattleSelectModelCommandHandler(self)

    def init_done(self):
        self.client_object.resource_loader.load_resource("battle_list\\", language=self.client_object.language)
        self.load_maps()
        self.load_battle_create()
        self.load_battles()
        self.end_layout_switch()

    def load_battle_create(self):
        self.game_object.add_model(battle_create_model.BattleCreateModel)
        self.game_object.load_object_from_client()

    def end_layout_switch(self):
        self.loaded = True
        self.lobby_layout_notify_model = self.client_object.client_space_registry.get_model(space_name="lobby", game_object_name="default_game_object", model=lobby_layout_notify_model.LobbyLayoutNotifyModel)
        self.lobby_layout_notify_model.end_layout_switch()

    def load_maps(self):
        map_global_game_objects = self.global_model.get_all_map_global_game_objects()

        for map_global_game_object in map_global_game_objects:
            map_game_object = self.client_space.add_global_game_object(map_global_game_object)
            map_game_object.load_object_from_client()

    def load_battles(self):
        battle_item_global_game_objects = self.global_model.get_all_battle_item_global_game_objects()
        self.add_battle_items(battle_item_global_game_objects)

    def add_battle_items(self, battle_item_global_game_objects):
        for battle_item_global_game_object in battle_item_global_game_objects:
            _battle_item_global_model = battle_item_global_game_object.get_global_model(battle_item_global_model.BattleItemGlobalModel)

            if (not self.user_property_model_data.user_owns_role(UserRole.ADMIN)) and (not _battle_item_global_model.is_user_allowed_to_join(self.client_object.username)):
                continue

            battle_item_game_object = self.client_space.add_global_game_object(battle_item_global_game_object)
            battle_item_game_object.load_object_from_client()

        self.commands.battle_items_packet_join_success_id()

    def unload_showing_battle(self):
        if self.showing_battle:
            self.client_space.get_game_object_by_id(self.showing_battle).remove_game_object()

    def show_battle(self, battle_item_game_object_id):
        self.unload_showing_battle()
        _battle_item_global_model = global_space_registry.get_global_model(battle_item_global_model.BattleItemGlobalModel, global_game_object_id=battle_item_game_object_id, global_space_name="battle_select")

        # TODO: send message to player that battle doesnt exist any more
        if _battle_item_global_model == None:
            return

        battle_info_game_object = self.client_space.add_global_game_object(_battle_item_global_model.battle_info_global_game_object)
        battle_info_game_object.add_model(pro_battle_info_model.ProBattleInfoModel)
        battle_info_game_object.load_object_from_client()
        self.showing_battle = battle_info_game_object.id

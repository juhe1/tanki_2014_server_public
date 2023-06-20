from client.layouts.battle_list.models.clan_info_model import clan_info_model_data
from client.space.model import Model

class ClanInfoModel(Model):
    model_id = 300090014

    def __init__(self, game_object, client_space, client_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

        self.model_data = clan_info_model_data.ClanInfoModelData(game_object, global_model.get_model_data())
        self.commands = None
        self.command_handler = None

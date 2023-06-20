from client.layouts.battle_list.models.pro_battle_info_model import pro_battle_info_model_data
from client.space.model import Model

class ProBattleInfoModel(Model):
    model_id = 300090023

    def __init__(self, game_object, client_space, client_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

        self.model_data = pro_battle_info_model_data.ProBattleInfoModelData(game_object, client_object)
        self.commands = None
        self.command_handler = None

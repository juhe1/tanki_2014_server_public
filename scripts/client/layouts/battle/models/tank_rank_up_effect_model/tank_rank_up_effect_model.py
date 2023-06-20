from . import tank_rank_up_effect_model_data
from client.space.model import Model

class TankRankUpEffectModel(Model):
    model_id = 300100079

    def __init__(self, game_object, client_space, client_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

        self.model_data = tank_rank_up_effect_model_data.TankRankUpEffectModelData(game_object, global_model.get_model_data())
        self.commands = None
        self.command_handler = None

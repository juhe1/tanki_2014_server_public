from . import bonus_postpone_model_commands
from client.space.model import Model

class BonusPostponeModel(Model):
    model_id = 300100017

    def __init__(self, game_object, client_space, client_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

        self.commands = bonus_postpone_model_commands.BonusPostponeModelCommands(client_space, game_object)

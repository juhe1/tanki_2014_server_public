from . import tank_model_command_handler
from . import tank_model_commands
from . import tank_model_data
from client.space.model import Model

class TankModel(Model):
    model_id = 300100078

    def __init__(self, game_object, client_space, client_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

        tank_model_cc = global_model.get_model_data()
        local = global_model.is_owner(client_object.user_id)

        self.model_data = tank_model_data.TankModelData(game_object, tank_model_cc, local)
        self.commands = tank_model_commands.TankModelCommands(client_space, game_object)

        if local:
            self.command_handler = tank_model_command_handler.TankModelCommandHandler(global_model)

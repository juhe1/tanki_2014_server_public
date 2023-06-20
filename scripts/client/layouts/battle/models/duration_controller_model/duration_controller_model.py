from . import duration_controller_model_data
from client.space.model import Model

class DurationControllerModel(Model):
    model_id = 300100033

    def __init__(self, game_object, client_space, client_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

        time_left_in_ms = global_model.get_time_left_in_ms()
        self.model_data = duration_controller_model_data.DurationControllerModelData(time_left_in_ms)

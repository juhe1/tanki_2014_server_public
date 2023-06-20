from . import color_transform_model_data
from client.space.model import Model

class ColorTransformModel(Model):
    model_id = 300100025

    def __init__(self, game_object, client_space, client_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

        self.model_data = color_transform_model_data.ColorTransformModelData(global_model.get_model_data())

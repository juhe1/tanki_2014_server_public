from client.layouts.aaaaaa.models.example_model import example_model
from space.global_model import GlobalModel
from . import example_model_cc

class ExampleGlobalModel(GlobalModel):

    CLIENT_MODEL = example_model.ExampleModel

    def __init__(self, global_game_object, global_space, owner_id=None):
        super().__init__(global_game_object, global_space, owner_id)

    def get_model_data(self):
        _example_model_cc = example_model_cc.ExampleModelCC()
        return _example_model_cc

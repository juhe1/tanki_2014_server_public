from client.layouts.aaaaaa.models.isis_sfx_model import isis_sfx_model
from space.global_model import GlobalModel
from . import isis_sfx_model_cc

class IsisSfxGlobalModel(GlobalModel):

    CLIENT_MODEL = isis_sfx_model.IsisSfxModel

    def __init__(self, global_game_object, global_space, owner_id=None):
        super().__init__(global_game_object, global_space, owner_id)

    def get_model_data(self):
        _isis_sfx_model_cc = isis_sfx_model_cc.IsisSfxModelCC()
        return _isis_sfx_model_cc

from client.space.model import Model

class BattleTdmModel(Model):
    model_id = 300080012

    def __init__(self, game_object, client_space, client_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

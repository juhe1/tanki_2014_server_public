from . import gpu_detector_model_command_handler
from client.space.model import Model

class GpuDetectorModel(Model):
    model_id = 300070008

    def __init__(self, game_object, client_space, client_object, global_model=None):
        super().__init__(game_object, client_space, client_object, global_model)

        self.model_data = None
        self.commands = None
        self.command_handler = gpu_detector_model_command_handler.GpuDetectorModelCommandHandler()

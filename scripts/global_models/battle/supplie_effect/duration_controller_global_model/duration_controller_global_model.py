from client.layouts.battle.models.duration_controller_model import duration_controller_model
from space.global_model import GlobalModel
from utils.time.timer import Timer

class DurationControllerGlobalModel(GlobalModel):

    CLIENT_MODEL = duration_controller_model.DurationControllerModel

    def __init__(self, global_game_object, global_space, time_in_sec, callback=None, owner_id=None):
        super().__init__(global_game_object, global_space, owner_id)

        self.time_in_sec = time_in_sec
        self.callback = callback
        self.timer = Timer(time_in_sec)
        self.timer.add_event_listener(self.time_end)
        self.timer.start()

    def destroy(self):
        self.timer.destroy()
        self.global_game_object.remove_global_game_object()

    def time_end(self):
        self.timer.destroy()
        self.global_game_object.remove_global_game_object()

        if self.callback == None: return
        self.callback()

    def get_time_left_in_ms(self):
        return int(self.timer.get_time_left_in_seconds() * 1000)

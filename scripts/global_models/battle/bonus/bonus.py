from utils.time.timer import Timer

class Bonus:
    def __init__(self, bonus_id, bonus_common_global_model, remove_function):
        self.bonus_id = bonus_id
        self.bonus_game_object_id = bonus_common_global_model.global_game_object.id
        self.spawn_position = bonus_common_global_model.generate_new_bonus_spawn_position()
        self.remove_function = remove_function
        self.timer = self.create_timer(bonus_common_global_model.get_life_time(), self.remove_bonus)
        self.destroyed = False
        self.bonus_type = bonus_common_global_model.bonus_type

    def destroy(self):
        self.destroyed = True

    def remove_bonus(self):
        if self.destroyed: return
        self.remove_function(self.bonus_id)

    def create_timer(self, life_time, remove_function):
        _timer = Timer(life_time)
        _timer.add_event_listener(remove_function)
        _timer.start()
        return _timer

    def get_time(self):
        return int(self.timer.get_time_left_in_seconds())

class TeamKickModelCC:
    def __init__(self):
        self.allys = []
        self.current_user = None
        self.disabled = False
        self.duration_immunity_affter_enter_in_sec = 0
        self.enter_time_diff_in_sec = 0
        self.immunity_stay_in_battle_in_sec = 0

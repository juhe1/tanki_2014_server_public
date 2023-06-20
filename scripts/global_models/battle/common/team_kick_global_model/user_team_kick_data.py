import datetime

class UserTeamKickData:
    def __init__(self):
        self.battle_join_time = datetime.datetime.now()
        self.excluded = False
        self.user_id = 0

    def get_battle_time_in_sec(self):
        now = datetime.datetime.now()
        return int((now - self.battle_join_time).total_seconds())


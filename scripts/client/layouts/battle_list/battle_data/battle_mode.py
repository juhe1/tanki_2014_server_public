from enum import IntEnum

def battle_mode_string_to_enum(battle_mode_string):
    if battle_mode_string == "dm":
        return BattleMode.DM
    if battle_mode_string == "tdm":
        return BattleMode.TDM
    if battle_mode_string == "ctf":
        return BattleMode.CTF
    if battle_mode_string in ["cp", "dom"]:
        return BattleMode.CP

def battle_mode_int_to_enum(battle_mode_int):
    if battle_mode_int == 0:
        return BattleMode.DM
    if battle_mode_int == 1:
        return BattleMode.TDM
    if battle_mode_int == 2:
        return BattleMode.CTF
    if battle_mode_int == 3:
        return BattleMode.CP

class BattleMode(IntEnum):
    DM = 0
    TDM = 1
    CTF = 2
    CP = 3

    def is_team_battle(self):
        return self in [BattleMode.TDM, BattleMode.CTF, BattleMode.CP]

from enum import IntEnum

def battle_theme_string_to_enum(battle_theme_string):
    if battle_theme_string == "summer":
        return BattleTheme.SUMMER
    if battle_theme_string == "winter":
        return BattleTheme.WINTER
    if battle_theme_string == "space":
        return BattleTheme.SPACE

def battle_theme_int_to_enum(battle_theme_int):
    if battle_theme_int == 0:
        return BattleTheme.SUMMER
    if battle_theme_int == 1:
        return BattleTheme.WINTER
    if battle_theme_int == 2:
        return BattleTheme.SPACE

class BattleTheme(IntEnum):
    SUMMER = 0
    WINTER = 1
    SPACE = 2

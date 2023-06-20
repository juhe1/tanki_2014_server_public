from utils.log import console_out
from enum import IntEnum

def string_to_team(team_string):
    if team_string in ["dm", "none"]:
        return Team.NONE
    if team_string == "red":
        return Team.RED
    if team_string == "blue":
        return Team.BLUE
    console_out.color_print("[TEAM][STRING_TO_TEAM][ERROR] " + team_string + " is not valid team!", "red")

def int_to_team(team_int):
    if team_int == 0:
        return Team.NONE
    if team_int == 1:
        return Team.RED
    if team_int == 2:
        return Team.BLUE
    console_out.color_print("[TEAM][INT_TO_TEAM][ERROR] " + str(team_int) + " is not valid team!", "red")

class Team(IntEnum):
    NONE = 0
    RED = 1
    BLUE = 2

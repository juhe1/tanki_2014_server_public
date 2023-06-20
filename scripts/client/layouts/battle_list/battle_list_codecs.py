from client.layouts.battle_list.battle_data.battle_theme import BattleTheme
from client.layouts.battle_list.battle_data.battle_mode import BattleMode
from client.layouts.battle_list.battle_data import battle_limits
from client.layouts.battle_list.battle_data import battle_data
from global_models.battle.common.tank_global_model.team import Team
from utils.binary.codecs import basic_codecs

class BattleLimitsCodec:
    def encode(battle_limits_in, buffer):
        basic_codecs.IntCodec.encode(battle_limits_in.score_limit, buffer)
        basic_codecs.IntCodec.encode(battle_limits_in.time_limit_in_sec, buffer)

    def decode(stream):
        new_battle_limits = battle_limits.BattleLimits()
        new_battle_limits.score_limit = basic_codecs.IntCodec.decode(stream)
        new_battle_limits.time_limit_in_sec = basic_codecs.IntCodec.decode(stream)
        return new_battle_limits


class BattleModeCodec:
    def encode(battle_mode_in, buffer):
        if battle_mode_in == BattleMode.DM:
            basic_codecs.IntCodec.encode(0, buffer)
            return
        if battle_mode_in == BattleMode.TDM:
            basic_codecs.IntCodec.encode(1, buffer)
            return
        if battle_mode_in == BattleMode.CTF:
            basic_codecs.IntCodec.encode(2, buffer)
            return
        if battle_mode_in == BattleMode.CP:
            basic_codecs.IntCodec.encode(3, buffer)
            return

    def decode(stream):
        mode = basic_codecs.IntCodec.decode(stream)
        if mode == 0:
            return BattleMode.DM
        if mode == 1:
            return BattleMode.TDM
        if mode == 2:
            return BattleMode.CTF
        if mode == 3:
            return BattleMode.CP


class MapThemeCodec:
    def encode(map_theme, buffer):
        if map_theme == BattleTheme.SUMMER:
            basic_codecs.IntCodec.encode(0, buffer)
            return
        if map_theme == BattleTheme.WINTER:
            basic_codecs.IntCodec.encode(1, buffer)
            return
        if map_theme == BattleTheme.SPACE:
            basic_codecs.IntCodec.encode(2, buffer)
            return

    def decode(stream):
        theme = basic_codecs.IntCodec.decode(stream)
        if theme == 0:
            return BattleTheme.SUMMER
        if theme == 1:
            return BattleTheme.WINTER
        if theme == 2:
            return BattleTheme.SPACE


class BattleInfoUserCodec:
    def encode(user, buffer):
        basic_codecs.IntCodec.encode(user.kills, buffer)
        basic_codecs.IntCodec.encode(user.score, buffer)
        basic_codecs.BooleanCodec.encode(user.suspicious, buffer)
        basic_codecs.LongCodec.encode(user.user_id, buffer)


class BattleCreateCodec:
    def decode(stream):
        new_battle_data = battle_data.BattleData()
        new_battle_data.auto_balance = basic_codecs.BooleanCodec.decode(stream)
        new_battle_data.battle_mode = BattleModeCodec.decode(stream)
        new_battle_data.friendly_fire = basic_codecs.BooleanCodec.decode(stream)
        new_battle_data.limits = BattleLimitsCodec.decode(stream)
        new_battle_data.map_id = basic_codecs.LongCodec.decode(stream)
        new_battle_data.max_people_count = basic_codecs.ByteCodec.decode(stream)
        new_battle_data.name = basic_codecs.StringCodec.decode(stream)
        new_battle_data.private_battle = basic_codecs.BooleanCodec.decode(stream)
        new_battle_data.pro_battle = basic_codecs.BooleanCodec.decode(stream)
        new_battle_data.rank_range = basic_codecs.RangeCodec.decode(stream)
        new_battle_data.theme = MapThemeCodec.decode(stream)
        new_battle_data.without_bonuses = basic_codecs.BooleanCodec.decode(stream)
        new_battle_data.without_crystals = basic_codecs.BooleanCodec.decode(stream)
        new_battle_data.without_supplies = basic_codecs.BooleanCodec.decode(stream)
        new_battle_data.without_upgrades = basic_codecs.BooleanCodec.decode(stream)
        return new_battle_data


class TeamCodec:
    def decode(stream):
        _team = basic_codecs.IntCodec.decode(stream)
        if _team == 0:
            return Team.RED
        if _team == 1:
            return Team.BLUE
        if _team == 2:
            return Team.NONE

    def encode(_team, buffer):
        if _team == Team.RED:
            basic_codecs.IntCodec.encode(0, buffer)
            return
        if _team == Team.BLUE:
            basic_codecs.IntCodec.encode(1, buffer)
            return
        if _team == Team.NONE:
            basic_codecs.IntCodec.encode(2, buffer)
            return
        console_out.color_print("[BATTLE_LIST_CODECS][TEAM_CODEC] not valid team!", "red")

from global_models.battle.common.tank_global_model.tank_state import LogicStateEnum
from client.layouts.battle.tank.movement import rotate_turret_command
from client.layouts.battle.tank.movement import move_command
from client.layouts.battle_list import battle_list_codecs
from client.layouts.battle.tank.enums import DeathReason
from utils.binary.codecs import basic_codecs
from utils.binary.bit_area import BitArea
from panda3d.core import Vec3
from utils.log import console_out

import math

class ColorTransformStructCodec:
    def encode(params, buffer):
        basic_codecs.FloatCodec.encode(params.alpha_multiplier, buffer)
        basic_codecs.ShortCodec.encode(params.alpha_offset, buffer)
        basic_codecs.FloatCodec.encode(params.blue_multiplier, buffer)
        basic_codecs.ShortCodec.encode(params.blue_offset, buffer)
        basic_codecs.FloatCodec.encode(params.green_multiplier, buffer)
        basic_codecs.ShortCodec.encode(params.green_offset, buffer)
        basic_codecs.FloatCodec.encode(params.red_multiplier, buffer)
        basic_codecs.ShortCodec.encode(params.red_offset, buffer)
        basic_codecs.FloatCodec.encode(params.t, buffer)

class BCSHStructCodec:
    def encode(params, buffer):
        basic_codecs.FloatCodec.encode(params.brightness, buffer)
        basic_codecs.FloatCodec.encode(params.contrast, buffer)
        basic_codecs.FloatCodec.encode(params.hue, buffer)
        basic_codecs.StringCodec.encode(params.key, buffer)
        basic_codecs.FloatCodec.encode(params.saturation, buffer)

class UserTeamKickDataCodec:
    def encode(params, buffer):
        basic_codecs.IntCodec.encode(params.get_battle_time_in_sec(), buffer)
        basic_codecs.BooleanCodec.encode(params.excluded, buffer)
        basic_codecs.LongCodec.encode(params.user_id, buffer)


class BattleFieldSoundsCodec:
    def encode(params, buffer):
        basic_codecs.LongCodec.encode(params.battle_finish_sound, buffer)
        basic_codecs.LongCodec.encode(params.kill_sound, buffer)


class DustParamsCodec:
    def encode(params, buffer):
        basic_codecs.FloatCodec.encode(params.alpha, buffer)
        basic_codecs.FloatCodec.encode(params.density, buffer)
        basic_codecs.FloatCodec.encode(params.dust_far_distance, buffer)
        basic_codecs.FloatCodec.encode(params.dust_near_distance, buffer)
        basic_codecs.LongCodec.encode(params.dust_particle, buffer)
        basic_codecs.FloatCodec.encode(params.dust_size, buffer)


class DynamicShadowParamsCodec:
    def encode(params, buffer):
        basic_codecs.FloatCodec.encode(params.angle_x, buffer)
        basic_codecs.FloatCodec.encode(params.angle_y, buffer)
        basic_codecs.UintCodec.encode(params.light_color, buffer)
        basic_codecs.IntCodec.encode(params.shadow_color, buffer)


class FogParamsCodec:
    def encode(params, buffer):
        basic_codecs.FloatCodec.encode(params.alpha, buffer)
        basic_codecs.IntCodec.encode(params.color, buffer)
        basic_codecs.FloatCodec.encode(params.far_limit, buffer)
        basic_codecs.FloatCodec.encode(params.near_limit, buffer)


class BattleFieldBonusCodec:
    def encode(params, buffer):
        basic_codecs.LongCodec.encode(params.bonus_id, buffer)
        basic_codecs.LongCodec.encode(params.bonus_game_object_id, buffer)
        basic_codecs.IntCodec.encode(params.get_time(), buffer)
        basic_codecs.Vector3DCodec.encode(params.spawn_position, buffer)


class BattleFieldBonusSpawnCodec:
    def encode(params, buffer):
        basic_codecs.LongCodec.encode(params.bonus_id, buffer)
        basic_codecs.LongCodec.encode(params.bonus_game_object_id, buffer)
        basic_codecs.Vector3DCodec.encode(params.spawn_position, buffer)


class LightingEffectRecordCodec:
    def encode(params, buffer):
        basic_codecs.FloatCodec.encode(params.attenuation_begin, buffer)
        basic_codecs.FloatCodec.encode(params.attenuation_end, buffer)
        basic_codecs.StringCodec.encode(params.color, buffer)
        basic_codecs.FloatCodec.encode(params.intensity, buffer)
        basic_codecs.IntCodec.encode(params.time, buffer)


class LightingEffectCodec:
    def encode(params, buffer):
        basic_codecs.StringCodec.encode(params.name, buffer)
        basic_codecs.VectorLevel1Codec.encode(params.records, LightingEffectRecordCodec, buffer)


class TankSoundsCodec:
    def encode(params, buffer):
        basic_codecs.LongCodec.encode(params.engine_idle_sound, buffer)
        basic_codecs.LongCodec.encode(params.engine_moving_sound, buffer)
        basic_codecs.LongCodec.encode(params.engine_start_moving_sound, buffer)
        basic_codecs.LongCodec.encode(params.engine_start_sound, buffer)
        basic_codecs.LongCodec.encode(params.engine_stop_moving_sound, buffer)
        basic_codecs.LongCodec.encode(params.turret_rotation_sound, buffer)


class TankLogicStateCodec:
    def encode(logic_state, buffer):
        if logic_state == LogicStateEnum.OUT_OF_GAME:
            basic_codecs.IntCodec.encode(0, buffer)
            return
        if logic_state == LogicStateEnum.ACTIVATING:
            basic_codecs.IntCodec.encode(1, buffer)
            return
        if logic_state == LogicStateEnum.ACTIVE:
            basic_codecs.IntCodec.encode(2, buffer)
            return
        if logic_state == LogicStateEnum.DEAD:
            basic_codecs.IntCodec.encode(3, buffer)
            return
        console_out.color_print("[ERROR][battle_codecs][tank_logic_state_codec] not valid state!", "red")


class TankStateCodec:
    def encode(params, buffer):
        basic_codecs.Vector3DCodec.encode(params.angular_velocity, buffer)
        basic_codecs.ByteCodec.encode(params.chassis_control, buffer)
        basic_codecs.Vector3DCodec.encode(params.linear_velocity, buffer)
        basic_codecs.Vector3DCodec.encode(params.orientation, buffer)
        basic_codecs.Vector3DCodec.encode(params.position, buffer)
        basic_codecs.FloatCodec.encode(params.turret_angle, buffer)
        basic_codecs.ByteCodec.encode(params.turret_control, buffer)


class TankInitializationDataCodec:
    def encode(params, buffer):
        basic_codecs.FloatCodec.encode(params.acceleration, buffer)
        basic_codecs.ShortCodec.encode(params.health, buffer)
        basic_codecs.OptionalCodec.encode((params.incarnation_id, buffer), buffer, basic_codecs.ShortCodec)
        basic_codecs.OptionalCodec.encode((params.logic_state, buffer), buffer, TankLogicStateCodec)
        basic_codecs.FloatCodec.encode(params.reverse_acceleration, buffer)
        basic_codecs.FloatCodec.encode(params.reverse_turn_acceleration, buffer)
        basic_codecs.FloatCodec.encode(params.side_acceleration, buffer)
        basic_codecs.FloatCodec.encode(params.speed, buffer)
        basic_codecs.OptionalCodec.encode((params.tank_state, buffer), buffer, TankStateCodec)
        basic_codecs.OptionalCodec.encode((params.team, buffer), buffer, battle_list_codecs.TeamCodec)
        basic_codecs.FloatCodec.encode(params.turn_acceleration, buffer)
        basic_codecs.FloatCodec.encode(params.turn_speed, buffer)
        basic_codecs.FloatCodec.encode(params.turret_rotation_speed, buffer)


class TankPartsCodec:
    def encode(params, buffer):
        basic_codecs.LongCodec.encode(params.color_id, buffer)
        basic_codecs.LongCodec.encode(params.hull_id, buffer)
        basic_codecs.LongCodec.encode(params.weapon_id, buffer)


class TankResourcesCodec:
    def encode(params, buffer):
        basic_codecs.LongCodec.encode(params.dead_color, buffer)
        basic_codecs.LongCodec.encode(params.death_sound, buffer)


class UserInfoCodec:
    def encode(params, buffer):
        basic_codecs.ShortCodec.encode(params.deaths, buffer)
        basic_codecs.ShortCodec.encode(params.kills, buffer)
        basic_codecs.ByteCodec.encode(params.rank, buffer)
        basic_codecs.IntCodec.encode(params.score, buffer)
        basic_codecs.StringCodec.encode(params.uid, buffer)
        basic_codecs.LongCodec.encode(params.user_id, buffer)


class UserStatCodec:
    def encode(params, buffer):
        basic_codecs.ShortCodec.encode(params.deaths, buffer)
        basic_codecs.ShortCodec.encode(params.kills, buffer)
        basic_codecs.IntCodec.encode(params.score, buffer)
        basic_codecs.LongCodec.encode(params.user_id, buffer)


class BattleMineCodec:
    def encode(params, buffer):
        basic_codecs.BooleanCodec.encode(params.activated, buffer)
        basic_codecs.LongCodec.encode(params.mine_id, buffer)
        basic_codecs.LongCodec.encode(params.owner_id, buffer)
        basic_codecs.Vector3DCodec.encode(params.position, buffer)


BIT_AREA_SIZE = 21
POSITION_COMPONENT_BITSIZE = 17
ANGLE_FACTOR = math.pi / 4096
ANGULAR_VELOCITY_FACTOR = 0.005
ORIENTATION_COMPONENT_BITSIZE = 13
LINEAR_VELOCITY_COMPONENT_BITSIZE = 13
ANGULAR_VELOCITY_COMPONENT_BITSIZE = 13

# some code in this class is ported from decompiled tanki online client source
class MoveCommandCodec:
    def encode(params, buffer):
        basic_codecs.ByteCodec.encode(params.control, buffer)

        new_bit_area = BitArea([0] * BIT_AREA_SIZE, BIT_AREA_SIZE)
        MoveCommandCodec.write_vector_3d(new_bit_area, params.position, POSITION_COMPONENT_BITSIZE, 1)
        MoveCommandCodec.write_vector_3d(new_bit_area, params.orientation, ORIENTATION_COMPONENT_BITSIZE, ANGLE_FACTOR)
        MoveCommandCodec.write_vector_3d(new_bit_area, params.linear_velocity, LINEAR_VELOCITY_COMPONENT_BITSIZE, 1)
        MoveCommandCodec.write_vector_3d(new_bit_area, params.angular_velocity, ANGULAR_VELOCITY_COMPONENT_BITSIZE, ANGULAR_VELOCITY_FACTOR)

        buffer.write_bytes(new_bit_area.get_data())

    def decode(binary_data):
        new_move_command = move_command.MoveCommand()
        new_move_command.control = basic_codecs.ByteCodec.decode(binary_data)

        bytes = binary_data.read_last_bytes()
        new_bit_area = BitArea(MoveCommandCodec.bytes_to_list(bytes), BIT_AREA_SIZE)

        new_move_command.position = MoveCommandCodec.read_vector_3d(new_bit_area, POSITION_COMPONENT_BITSIZE, 1)
        new_move_command.orientation = MoveCommandCodec.read_vector_3d(new_bit_area, ORIENTATION_COMPONENT_BITSIZE, ANGLE_FACTOR)
        new_move_command.linear_velocity = MoveCommandCodec.read_vector_3d(new_bit_area, LINEAR_VELOCITY_COMPONENT_BITSIZE, 1)
        new_move_command.angular_velocity = MoveCommandCodec.read_vector_3d(new_bit_area, ANGULAR_VELOCITY_COMPONENT_BITSIZE, ANGULAR_VELOCITY_FACTOR)

        return new_move_command

    def bytes_to_list(bytes):
        return [b for b in bytes]

    def read_vector_3d(_bit_area, bit_size, factor):
        _loc4_ = (_bit_area.read(bit_size) - (1 << bit_size - 1)) * factor;
        _loc5_ = (_bit_area.read(bit_size) - (1 << bit_size - 1)) * factor;
        _loc6_ = (_bit_area.read(bit_size) - (1 << bit_size - 1)) * factor;
        return Vec3(_loc4_,_loc5_,_loc6_);

    def write_vector_3d(_bit_area, _vector_3d, bit_size, factor):
        _loc5_ = 1 << bit_size - 1
        _bit_area.write(bit_size, MoveCommandCodec.prepare_value(_vector_3d.x, _loc5_, factor))
        _bit_area.write(bit_size, MoveCommandCodec.prepare_value(_vector_3d.y, _loc5_, factor))
        _bit_area.write(bit_size, MoveCommandCodec.prepare_value(_vector_3d.z, _loc5_, factor))

    def prepare_value(param1, param2, param3):
        _loc4_ = int(param1 / param3)
        _loc5_ = 0
        if _loc4_ >= -param2:
            _loc5_ = int(_loc4_ - param2)
        return int(min(param2,_loc5_))


class RotateTurretCommandCodec:
    def encode(params, buffer):
        basic_codecs.FloatCodec.encode(params.angle, buffer)
        basic_codecs.ByteCodec.encode(params.control, buffer)

    def decode(binary_data):
        new_rotate_turret_command = rotate_turret_command.RotateTurretCommand()
        new_rotate_turret_command.angle = basic_codecs.FloatCodec.decode(binary_data)
        new_rotate_turret_command.control = basic_codecs.ByteCodec.decode(binary_data)
        return new_rotate_turret_command

class DeathReasonCodec:
    def encode(enum, buffer):
        if enum == DeathReason.KILLED_IN_BATTLE:
            basic_codecs.IntCodec.encode(0, buffer)
            return
        if enum == DeathReason.SUICIDE:
            basic_codecs.IntCodec.encode(1, buffer)
            return
        if enum == DeathReason.BURNT_DOWN:
            basic_codecs.IntCodec.encode(2, buffer)
            return
        if enum == DeathReason.DROWNED:
            basic_codecs.IntCodec.encode(3, buffer)


class UserRewardCodec:
    def encode(user_info, buffer):
        basic_codecs.IntCodec.encode(user_info.fund, buffer)
        basic_codecs.LongCodec.encode(user_info.user_id, buffer)

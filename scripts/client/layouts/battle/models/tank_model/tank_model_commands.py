from client.layouts.battle_list import battle_list_codecs
from client.layouts.battle import battle_codecs
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer

class TankModelCommands:
    def __init__(self, space, game_object):
        self.space = space
        self.game_object = game_object
        self.PREPARE_TO_SPAWN_COMMAND_ID = 300100094
        self.SPAWN_COMMAND_ID = 300100099
        self.ACTIVATE_TANK_COMMAND_ID = 300100089
        self.MOVE_COMMAND_ID = 300100092
        self.MOVEMENT_CONTROL_COMMAND_ID = 300100093
        self.ROTATE_TURRET_COMMAND_ID = 300100095
        self.SET_HEALTH_COMMAND_ID = 300100096
        self.DEATH_CONFIRMED_COMMAND_ID = 300100090
        self.KILL_COMMAND_ID = 300100091
        self.SET_SPECIFICATION_COMMAND_ID = 300100097
        self.SET_TEMPERATURE_COMMAND_ID = 300100098

    def prepare_to_spawn(self, position, orientation):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.PREPARE_TO_SPAWN_COMMAND_ID, buffer)
        basic_codecs.Vector3DCodec.encode(position, buffer)
        basic_codecs.Vector3DCodec.encode(orientation, buffer)
        self.space.send_command(self.game_object.id, buffer, "PREPARE_TO_SPAWN")

    def spawn(self, team, position, orientation, health, incarnation_id):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.SPAWN_COMMAND_ID, buffer)
        battle_list_codecs.TeamCodec.encode(team, buffer)
        basic_codecs.Vector3DCodec.encode(position, buffer)
        basic_codecs.Vector3DCodec.encode(orientation, buffer)
        basic_codecs.ShortCodec.encode(health, buffer)
        basic_codecs.ShortCodec.encode(incarnation_id, buffer)
        self.space.send_command(self.game_object.id, buffer, "SPAWN")

    def activate_tank(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.ACTIVATE_TANK_COMMAND_ID, buffer)
        self.space.send_command(self.game_object.id, buffer, "ACTIVATE_TANK")

    def move(self, move_command):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.MOVE_COMMAND_ID, buffer)
        battle_codecs.MoveCommandCodec.encode(move_command, buffer)
        self.space.send_command(self.game_object.id, buffer, "MOVE")

    def update_movement_control(self, control):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.MOVEMENT_CONTROL_COMMAND_ID, buffer)
        basic_codecs.ByteCodec.encode(control, buffer)
        self.space.send_command(self.game_object.id, buffer, "UPDATE_MOVEMENT_CONTROL")

    def rotate_turret(self, rotate_turret_command):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.ROTATE_TURRET_COMMAND_ID, buffer)
        battle_codecs.RotateTurretCommandCodec.encode(rotate_turret_command, buffer)
        self.space.send_command(self.game_object.id, buffer, "ROTATE_TURRET")

    def set_health(self, health):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.SET_HEALTH_COMMAND_ID, buffer)
        basic_codecs.FloatCodec.encode(health, buffer)
        self.space.send_command(self.game_object.id, buffer, "SET_HEALTH")

    def death_confirmed(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.DEATH_CONFIRMED_COMMAND_ID, buffer)
        self.space.send_command(self.game_object.id, buffer, "DEATH_CONFIRMED")

    def kill(self, reason, killer_id, respawn_delay):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.KILL_COMMAND_ID, buffer)
        battle_codecs.DeathReasonCodec.encode(reason, buffer)
        basic_codecs.OptionalCodec.encode((killer_id, buffer), buffer, basic_codecs.LongCodec)
        basic_codecs.IntCodec.encode(respawn_delay, buffer)
        self.space.send_command(self.game_object.id, buffer, "KILL")

    def set_specification(self, speed, turn_speed, turret_rotation_speed, acceleration, specification_id):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.SET_SPECIFICATION_COMMAND_ID, buffer)
        basic_codecs.FloatCodec.encode(speed, buffer)
        basic_codecs.FloatCodec.encode(turn_speed, buffer)
        basic_codecs.FloatCodec.encode(turret_rotation_speed, buffer)
        basic_codecs.FloatCodec.encode(acceleration, buffer)
        basic_codecs.ShortCodec.encode(specification_id, buffer)
        self.space.send_command(self.game_object.id, buffer, "SET_SPECIFICATION")

    def set_temperature(self, temperature):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.SET_TEMPERATURE_COMMAND_ID, buffer)
        basic_codecs.FloatCodec.encode(temperature, buffer)
        self.space.send_command(self.game_object.id, buffer, "SET_TEMPERATURE")


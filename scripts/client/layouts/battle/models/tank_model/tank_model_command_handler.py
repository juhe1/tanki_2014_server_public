from client.layouts.battle import battle_codecs
from utils.binary.codecs import basic_codecs

class TankModelCommandHandler:
    def __init__(self, global_model):
        self.READY_TO_SPAWN_COMMAND_ID = 300100086
        self.ACTIVATE_TANK_COMMAND_ID = 300100081
        self.MOVE_COMMAND_ID = 300100084
        self.MOVEMENT_CONTROL_COMMAND_ID = 300100085
        self.ROTATE_TURRET_COMMAND_ID = 300100087
        self.CONFIRM_SPAWN_COMMAND_ID = 300100082
        self.DEATH_CONFIRMATION_COMMAND_ID = 300100083

        self.global_model = global_model

    def handle_command(self, binary_data, command_id):
        if command_id == self.READY_TO_SPAWN_COMMAND_ID:
            self.global_model.prepare_to_spawn()
            return True

        if command_id == self.ACTIVATE_TANK_COMMAND_ID:
            self.global_model.activate()
            return True

        if command_id == self.MOVE_COMMAND_ID:
            self.move(binary_data)
            return True

        if command_id == self.MOVEMENT_CONTROL_COMMAND_ID:
            self.movement_control(binary_data)
            return True

        if command_id == self.ROTATE_TURRET_COMMAND_ID:
            self.rotate_turret(binary_data)
            return True

        if command_id == self.CONFIRM_SPAWN_COMMAND_ID:
            self.confirm_spawn(binary_data)
            return True

        if command_id == self.DEATH_CONFIRMATION_COMMAND_ID:
            self.global_model.confirm_death()
            return True

    def move(self, binary_data):
        client_time = basic_codecs.IntCodec.decode(binary_data)
        specification_id = basic_codecs.ShortCodec.decode(binary_data)
        move_command = battle_codecs.MoveCommandCodec.decode(binary_data)
        self.global_model.move(move_command, specification_id, client_time)

    def movement_control(self, binary_data):
        client_time = basic_codecs.IntCodec.decode(binary_data)
        specification_id = basic_codecs.ShortCodec.decode(binary_data)
        movement_control = basic_codecs.ByteCodec.decode(binary_data)
        self.global_model.update_movement_control(client_time, specification_id, movement_control)

    def rotate_turret(self, binary_data):
        client_time = basic_codecs.IntCodec.decode(binary_data)
        rotate_turret_command = battle_codecs.RotateTurretCommandCodec.decode(binary_data)
        incarnation_id = basic_codecs.ShortCodec.decode(binary_data)
        self.global_model.rotate_turret(client_time, rotate_turret_command, incarnation_id)

    def confirm_spawn(self, binary_data):
        incarnation_id = basic_codecs.ShortCodec.decode(binary_data)
        return
        # NOTE: this doesnt do anything yet

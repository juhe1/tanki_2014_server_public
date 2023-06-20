from utils.binary.codecs import basic_codecs

class SmokyModelCommandHandler:
    def __init__(self, global_model):
        self.global_model = global_model
        self.FIRE_COMMAND_COMMAND_ID = 300100074
        self.FIRE_STATIC_COMMAND_COMMAND_ID = 300100075
        self.FIRE_TARGET_COMMAND_COMMAND_ID = 300100076

    def handle_command(self, binary_data, command_id):
        if command_id == self.FIRE_COMMAND_COMMAND_ID:
            self.fire(binary_data)
            return True
        if command_id == self.FIRE_STATIC_COMMAND_COMMAND_ID:
            self.fire_static(binary_data)
            return True
        if command_id == self.FIRE_TARGET_COMMAND_COMMAND_ID:
            self.fire_target(binary_data)
            return True

    def fire(self, binary_data):
        client_time = basic_codecs.IntCodec.decode(binary_data)
        self.global_model.fire(client_time)

    def fire_static(self, binary_data):
        client_time = basic_codecs.IntCodec.decode(binary_data)
        hit_point = basic_codecs.Vector3DCodec.decode(binary_data)
        self.global_model.fire_static(client_time, hit_point)

    def fire_target(self, binary_data):
        client_time = basic_codecs.IntCodec.decode(binary_data)
        target_id = basic_codecs.LongCodec.decode(binary_data)
        target_incarnation = basic_codecs.ShortCodec.decode(binary_data)
        target_pos = basic_codecs.Vector3DCodec.decode(binary_data)
        hit_point = basic_codecs.Vector3DCodec.decode(binary_data)
        hit_point_word = basic_codecs.Vector3DCodec.decode(binary_data)
        self.global_model.fire_target(client_time, target_id, target_incarnation, target_pos, hit_point, hit_point_word)

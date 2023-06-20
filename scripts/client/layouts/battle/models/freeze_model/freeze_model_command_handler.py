from utils.binary.codecs import basic_codecs

class FreezeModelCommandHandler:
    def __init__(self, global_model):
        self.global_model = global_model

        self.HIT_COMMAND_ID = 300100043
        self.START_FIRE_COMMAND_ID = 300100044
        self.STOP_FIRE_COMMAND_ID = 300100045

    def handle_command(self, binary_data, command_id):
        if command_id == self.HIT_COMMAND_ID:
            self.hit(binary_data)
            return True

        if command_id == self.START_FIRE_COMMAND_ID:
            self.start_fire(binary_data)
            return True

        if command_id == self.STOP_FIRE_COMMAND_ID:
            self.stop_fire(binary_data)
            return True

    def hit(self, binary_data):
        time = basic_codecs.IntCodec.decode(binary_data)
        targets = basic_codecs.VectorLevel1Codec.decode(binary_data, basic_codecs.LongCodec)
        incarnations = basic_codecs.VectorLevel1Codec.decode(binary_data, basic_codecs.ShortCodec)
        target_positions = basic_codecs.VectorLevel1Codec.decode(binary_data, basic_codecs.Vector3DCodec)
        hit_points_world = basic_codecs.VectorLevel1Codec.decode(binary_data, basic_codecs.Vector3DCodec)
        self.global_model.hit(time, targets, incarnations, target_positions, hit_points_world)

    def start_fire(self, binary_data):
        time = basic_codecs.IntCodec.decode(binary_data)
        self.global_model.start_fire(time)

    def stop_fire(self, binary_data):
        time = basic_codecs.IntCodec.decode(binary_data)
        self.global_model.stop_fire(time)


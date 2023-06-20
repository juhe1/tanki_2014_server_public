from client.dispatcher.dispatcher_model import model_data
from client.layouts.battle import battle_codecs
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer
from . import color_transform_model

class ColorTransformModelData:
    def __init__(self, color_transform_model_cc):
        self.color_transform_model_cc = color_transform_model_cc

    def get_model_data(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.VectorLevel1Codec.encode(self.color_transform_model_cc.color_transforms, battle_codecs.ColorTransformStructCodec, buffer)

        _model_data = model_data.ModelData()
        _model_data.data = buffer
        _model_data.id = color_transform_model.ColorTransformModel.model_id
        return _model_data

from loaders.client_resource_loader import client_resource_loader
from client.dispatcher.dispatcher_model import model_data
from utils.binary.codecs import basic_codecs
from utils.binary import binary_buffer
from . import billboards_model
import server_properties

class BillboardsModelData:
    def __init__(self, game_object, billboards_model_cc):
        self.game_object = game_object

        self.bill_image = billboards_model_cc.bill_image

    def get_model_data(self):
        buffer = binary_buffer.BinaryBuffer()
        basic_codecs.LongCodec.encode(self.bill_image, buffer)

        _model_data = model_data.ModelData()
        _model_data.data = buffer
        _model_data.id = self.game_object.get_model(billboards_model.BillboardsModel).model_id
        return _model_data

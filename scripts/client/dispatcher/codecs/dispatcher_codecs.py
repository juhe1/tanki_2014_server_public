from client.dispatcher.dispatcher_model import load_object_struct
from loaders.client_resource_loader import resource_types
from utils.binary.codecs import basic_codecs
from utils.log import console_out

class ClassDispatcherItemCodec:
    def encode(class_dispatcher_item, buffer):
        basic_codecs.ByteCodec.encode(1, buffer) # item id
        basic_codecs.LongCodec.encode(class_dispatcher_item.class_id, buffer)
        basic_codecs.OptionalCodec.encode((class_dispatcher_item.parent_id, buffer), buffer, basic_codecs.LongCodec)
        basic_codecs.IntCodec.encode(len(class_dispatcher_item.game_model_ids), buffer)
        for model_id in class_dispatcher_item.game_model_ids:
            basic_codecs.LongCodec.encode(model_id, buffer)
        basic_codecs.IntCodec.encode(len(class_dispatcher_item.model_datas.get_binary_data()), buffer) # model datas lenght
        basic_codecs.ShortCodec.encode(0, buffer) # read offset for model datas
        buffer.merge_buffer(class_dispatcher_item.model_datas) # marge model datas to buffer


class ResourceDispatcherItemCodec:
    def encode(resource_dispatcher_item, buffer):
        basic_codecs.ByteCodec.encode(2, buffer) # item id
        basic_codecs.LongCodec.encode(resource_dispatcher_item.id, buffer)
        basic_codecs.ShortCodec.encode(resource_dispatcher_item.type, buffer)
        basic_codecs.LongCodec.encode(resource_dispatcher_item.version, buffer)
        basic_codecs.BooleanCodec.encode(resource_dispatcher_item.is_lazy, buffer)
        basic_codecs.ShortCodec.encode(resource_dispatcher_item.hash_calculation_method_id, buffer)
        basic_codecs.ByteCodec.encode(len(resource_dispatcher_item.locales), buffer)
        for locale in resource_dispatcher_item.locales:
            basic_codecs.SimpleStringCodec.encode(locale, buffer)
        basic_codecs.ShortCodec.encode(len(resource_dispatcher_item.file_infos), buffer)
        for file_info in resource_dispatcher_item.file_infos:
            basic_codecs.SimpleStringCodec.encode(file_info.file_name, buffer)
            basic_codecs.IntCodec.encode(file_info.file_size, buffer)
        resource_types.get_codec(resource_dispatcher_item.type).encode(resource_dispatcher_item.params, buffer)


class DispatcherItemCodec:
    def encode(dispatcher_item, buffer):
        if dispatcher_item.item_type == "class":
            ClassDispatcherItemCodec.encode(dispatcher_item, buffer)
            return
        if dispatcher_item.item_type == "resource":
            ResourceDispatcherItemCodec.encode(dispatcher_item, buffer)
            return
        if dispatcher_item.item_type == "level_separator":
            basic_codecs.ByteCodec.encode(3, buffer) # item id
            return
        console_out.color_print("[DSIPATCHER_CODECS][ERROR] we dont have codec for type: " + str(dispatcher_item.item_type), "red")


class ModelDataCodec:
    def encode(model_data, buffer):
        basic_codecs.LongCodec.encode(model_data.id, buffer)
        buffer.merge_buffer(model_data.data)


class LoadObjectStructCodec:
    def encode(load_object_struct, buffer):
        basic_codecs.VectorLevel1Codec.encode(load_object_struct.data, ModelDataCodec, buffer)
        basic_codecs.LongCodec.encode(load_object_struct.id, buffer)
        basic_codecs.LongCodec.encode(load_object_struct.parent, buffer)


class ImageParamsCodec:
    def encode(params, buffer):
        basic_codecs.BooleanCodec.encode(params["alpha"], buffer)


class SwfParamsCodec:
    def encode(params, buffer):
        basic_codecs.VectorLevel1Codec.encode( params.keys(), basic_codecs.StringCodec, buffer)
        basic_codecs.VectorLevel1Codec.encode( params.values(), basic_codecs.StringCodec, buffer)


class Tanks3DSResource:
    def encode(params, buffer):
        buffer.write_bytes(b"")

class ImageFrameParams:
    def encode(params, buffer):
        basic_codecs.FloatCodec.encode(params["fps"], buffer)
        basic_codecs.IntCodec.encode(params["frame_height"], buffer)
        basic_codecs.IntCodec.encode(params["frame_width"], buffer)
        basic_codecs.ShortCodec.encode(params["num_frames"], buffer)


# TODO: delete this because it is not needet
class MapParamsCodec:
    def encode(params, buffer):
        pass


class Empty:
    def encode(empty, buffer):
        buffer.write_bytes(b"")

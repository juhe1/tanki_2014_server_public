from client.layouts.garage.garage_utils import name_to_id
from utils.binary.codecs import basic_codecs
from utils.log import console_out

class ItemCategoryEnum:
    def encode(item_type, buffer):
        id = name_to_id.item_category_enum_name_to_id(item_type)
        basic_codecs.IntCodec.encode(id, buffer)


class ItemGarageProperty:
    def encode(property_name, buffer):
        property_id = name_to_id.item_garage_property_name_to_id(property_name)
        basic_codecs.IntCodec.encode(property_id, buffer)

    def decode(binary_data):
        item_property_id = basic_codecs.IntCodec.decode(binary_data)
        return name_to_id.item_garage_property_id_to_name(item_property_id)


class ItemProperty:
    def encode(item_property, buffer):
        item_property_id = name_to_id.item_property_name_to_id(item_property)
        basic_codecs.IntCodec.encode(item_property_id, buffer)

    def decode(binary_data):
        item_property_id = basic_codecs.IntCodec.decode(binary_data)
        return name_to_id.item_property_id_to_name(item_property_id)


class PropertyData:
    def encode(property, buffer):
        basic_codecs.FloatCodec.encode(property.final_value, buffer)
        basic_codecs.FloatCodec.encode(property.initial_value, buffer)
        ItemProperty.encode(property.item_property, buffer)


class GaragePropertyData:
    def encode(upgradable_property_data, buffer):
        basic_codecs.OptionalCodec.encode((upgradable_property_data.cost, buffer), buffer, basic_codecs.LinearParamCodec)
        basic_codecs.FloatCodec.encode(upgradable_property_data.importance, buffer)
        basic_codecs.IntCodec.encode(upgradable_property_data.level, buffer)
        basic_codecs.IntCodec.encode(upgradable_property_data.max_level, buffer)
        basic_codecs.OptionalCodec.encode((upgradable_property_data.properties, PropertyData, buffer), buffer, basic_codecs.VectorLevel1Codec)
        basic_codecs.IntCodec.encode(upgradable_property_data.property_id, buffer)
        basic_codecs.IntCodec.encode(upgradable_property_data.speed_up_discount, buffer)
        basic_codecs.IntCodec.encode(upgradable_property_data.time_discount, buffer)
        basic_codecs.OptionalCodec.encode((upgradable_property_data.time, buffer), buffer, basic_codecs.LinearParamCodec)
        basic_codecs.IntCodec.encode(upgradable_property_data.upgrade_discount, buffer)


class ItemGaragePropertyData:
    def encode(params, buffer):
        ItemGarageProperty.encode(params.property, buffer)
        basic_codecs.StringCodec.encode(params.value, buffer)


class DiscountItem:
    def encode(discount_item, buffer):
        basic_codecs.IntCodec.encode(discount_item.discount, buffer)
        basic_codecs.LongCodec.encode(discount_item.item, buffer)


class KitItem:
    def encode(kit_item, buffer):
        basic_codecs.IntCodec.encode(kit_item.count, buffer)
        basic_codecs.LongCodec.encode(kit_item.item, buffer)
        basic_codecs.BooleanCodec.encode(kit_item.mount, buffer)


class UpgradingPropertyInfo:
    def encode(params, buffer):
        basic_codecs.IntCodec.encode(params.property_id, buffer)
        basic_codecs.IntCodec.encode(params.remaining_time_in_ms, buffer)


class GarageItemInfo:
    def encode(params, buffer):
        ItemCategoryEnum.encode(params.category, buffer)
        basic_codecs.LongCodec.encode(params.item, buffer)
        basic_codecs.IntCodec.encode(params.modification_index, buffer)
        basic_codecs.BooleanCodec.encode(params.mounted, buffer)
        basic_codecs.StringCodec.encode(params.name, buffer)
        basic_codecs.ShortCodec.encode(params.position, buffer)
        basic_codecs.LongCodec.encode(params.preview, buffer)
        basic_codecs.IntCodec.encode(params.remaining_time_in_ms, buffer)

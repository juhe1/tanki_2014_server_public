from global_models.battle.common.color_transform_global_model.color_transform_struct import ColorTransformStruct
from client.layouts.battle.structs import lighting_effect
from client.layouts.battle.structs import bcsh

def dictionary_to_lighting_effect(dictionary):
    new_lighting_effect = lighting_effect.LightingEffect()
    new_lighting_effect.name = dictionary["name"]

    # loop all records
    for record in dictionary["records"]:
        new_record = lighting_effect.LightingEffectRecord()
        new_record.attenuation_begin = record["attenuation_begin"]
        new_record.attenuation_end = record["attenuation_end"]
        new_record.color = record["color"]
        new_record.intensity = record["intensity"]
        new_record.time = record["time"]
        new_lighting_effect.records.append(new_record)

    return new_lighting_effect

def dictionary_to_bcsh_data(dictionary):
    new_bcsh_data = bcsh.BCSHStruct()
    new_bcsh_data.brightness = dictionary["brightness"]
    new_bcsh_data.contrast = dictionary["contrast"]
    new_bcsh_data.hue = dictionary["hue"]
    new_bcsh_data.key = dictionary["key"]
    new_bcsh_data.saturation = dictionary["saturation"]

    return new_bcsh_data

def dictionary_to_color_transform_struct(dictionary):
    new_color_transform_struct = ColorTransformStruct()
    new_color_transform_struct.alpha_multiplier = dictionary["alphaMultiplier"]
    new_color_transform_struct.alpha_offset = dictionary["alphaOffset"]
    new_color_transform_struct.blue_multiplier = dictionary["blueMultiplier"]
    new_color_transform_struct.blue_offset = dictionary["blueOffset"]
    new_color_transform_struct.green_multiplier = dictionary["greenMultiplier"]
    new_color_transform_struct.green_offset = dictionary["greenOffset"]
    new_color_transform_struct.red_multiplier = dictionary["redMultiplier"]
    new_color_transform_struct.red_offset = dictionary["redOffset"]
    new_color_transform_struct.t = dictionary["t"]

    return new_color_transform_struct

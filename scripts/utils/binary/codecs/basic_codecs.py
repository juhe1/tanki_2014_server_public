from utils.data_types import range_data
from utils.binary import binary_stream
from panda3d.core import Vec3
from utils.log import console_out
from bitstring import BitArray
import struct

import hexdump
import zlib

class SimpleStringCodec:
    def encode(string, buffer):
        ByteCodec.encode(len(string), buffer)
        string = bytes(string, 'ascii')
        buffer.write_bytes(string)
        buffer.add_type([console_out.BACKGROUND_COLORS["blue"], len(string)])


class BooleanCodec:
    def decode(binary_data):
        boolean_byte = binary_data.read_bytes(1)
        boolean_number =  int.from_bytes(boolean_byte, byteorder='big', signed=True)
        return boolean_number == 1

    def encode(boolean, buffer):
        if boolean:
            ByteCodec.encode(1, buffer)
            return
        ByteCodec.encode(0, buffer)


class StringCodec:
    def decode(data):
        string_lenght = LenghtCodec.decode(data)
        return data.read_bytes(string_lenght).decode("utf-8", errors="ignore")

    def encode(string, buffer):
        encoded_string = string.encode()
        LenghtCodec.encode(len(encoded_string), buffer)
        buffer.write_bytes( encoded_string )
        buffer.add_type([console_out.BACKGROUND_COLORS["blue"], len(encoded_string)])


class LenghtCodec:
    def decode(lenght_binary):
        byte1 = lenght_binary.read_bytes(1)
        byte1 =  int.from_bytes(byte1, byteorder='big', signed=True)

        if (byte1 & 128) == 0:
            return byte1

        byte2 = lenght_binary.read_bytes(1)
        byte2 = int.from_bytes(byte2, byteorder='big', signed=True)

        if (byte2 & 64) == 0:
            lenght = ((byte1 & 63) << 8) + (byte2 & 255)
            return lenght

        byte3 = lenght_binary.read_bytes(1)
        byte3 = int.from_bytes(byte3, byteorder='big', signed=True)

        lenght = ((byte1 & 63) << 16) + ((byte2 & 255) << 8) + (byte3 & 255)
        return lenght


    def encode(lenght, buffer):
        if lenght < 128:
            ByteCodec.encode((lenght & 127), buffer)
            return
        if lenght < 16384:
            x = (lenght &  16383) + 32768
            part_1 = (x & 65280) >> 8
            part_2 = x & 255
            ByteCodec.encode(part_1, buffer)
            ByteCodec.encode(part_2, buffer)
            return

        x = (lenght & 4194303) + 12582912
        part_1 = (x & 16711680) >> 16
        part_2 = (x & 65280) >> 8
        part_3 = x & 255

        ByteCodec.encode(part_1, buffer)
        ByteCodec.encode(part_2, buffer)
        ByteCodec.encode(part_3, buffer)


# this codec doesnt support long packages(more than 16384 bytes) yet
class PackageCodec:
    def decode(binary_data):
        BIG_LENGTH_FLAG = 128
        ZIPPED_FLAG = 64
        binary_datas = []

        while binary_data.bytes_awaible():
            first_byte = ByteCodec.decode(binary_data);
            is_long_package = (first_byte & BIG_LENGTH_FLAG) != 0;
            is_package_zipped = False

            if is_long_package:
                lenght_part_1 = (first_byte ^ BIG_LENGTH_FLAG) << 24
                lenght_part_2 = (ByteCodec.decode(binary_data) & 255) << 16
                lenght_part_3 = (ByteCodec.decode(binary_data) & 255) << 8
                lenght_part_4 = ByteCodec.decode(binary_data) & 255
                package_length = lenght_part_1 + lenght_part_2 + lenght_part_3 + lenght_part_4
                is_package_zipped = True
            else:
                is_package_zipped = (first_byte & ZIPPED_FLAG) != 0;

                lenght_first_part = (first_byte & 63) << 8;
                lenght_second_part = ByteCodec.decode(binary_data) & 255
                package_length = lenght_first_part + lenght_second_part

            new_binary_data = binary_data.read_bytes(package_length)

            if is_package_zipped:
                new_binary_data = zlib.compress(new_binary_data)

            new_stream = binary_stream.BinaryStream(new_binary_data)
            OptionalMapCodec.decode(new_stream)
            binary_datas.append(new_stream)

        return binary_datas

    def encode(buffer):
        MAXIMUM_DATA_LENGTH = 2147483647
        LONG_SIZE_DELIMITER = 16384
        LENGTH_FLAG = 0x80

        binary_data = buffer.get_binary_data()

        optional_map = OptionalMapCodec.encode(buffer)

        size = len(binary_data) + len(optional_map)
        long_package = size >= LONG_SIZE_DELIMITER

        # we compress the package if it is long size
        if long_package:
            #console_out.safe_print("optional_map without zipping:")
            #console_out.hexdump(optional_map)
            #console_out.safe_print("package without zipping:")
            #console_out.hexdump(buffer.get_binary_data(), buffer.get_types())

            binary_data = optional_map + binary_data # write optional map
            binary_data = zlib.compress(binary_data)
            buffer.clear_types() # we clear types because we zip the package
            buffer.replace_original_binary_data(binary_data)
            size = len(binary_data) # we need to calculate size again after compression

        if size > MAXIMUM_DATA_LENGTH:
            console_out.color_print("[PACKAGE_CODEC][ERROR] package is too long!", "red")
        if long_package:
            out = (size >> 24 | LENGTH_FLAG).to_bytes(1, 'big')
            out += ((size & 0xFF0000) >> 16).to_bytes(1, 'big')
            out += ((size & 0xFF00) >> 8).to_bytes(1, 'big')
            out += (size & 0xFF).to_bytes(1, 'big')
        else:
            size_byte1 = (size & 65280) >> 8
            size_byte2 = size & 255
            out  = size_byte1.to_bytes(1, 'big')
            out += size_byte2.to_bytes(1, 'big')
            out += optional_map

        buffer.add_type_with_index([console_out.BACKGROUND_COLORS["black"], len(out)], 0)
        return buffer.write_bytes_with_index(out, 0)


class OptionalMapCodec:
    def encode(buffer):
        ONE_BYTE_FLAG = 32
        TWO_BYTES_FLAG = 64
        THREE_BYTES_FLAG = 96
        LENGTH_1_BYTE_FLAG = 128
        LENGTH_3_BYTE_FLAG = 12582912

        optional_map = buffer.get_optional_map()
        optional_map_size = buffer.optional_map_bit_count
        out = b""

        bits = BitArray(bytes=optional_map)

        if optional_map_size == 0:
            return (0).to_bytes(1, 'big', signed=True)
        if optional_map_size <= 5:
            out += ((optional_map[0] & 255) >> 3).to_bytes(1, 'big', signed=True)
            return out
        if optional_map_size <= 13:
            out += (((optional_map[0] & 255) >> 3) + ONE_BYTE_FLAG).to_bytes(1, 'big', signed=False)
            out += (((optional_map[1] & 255) >> 3) + (optional_map[0] << 5) & 255).to_bytes(1, 'big', signed=False)
            return out
        if optional_map_size <= 21:
            out += (((optional_map[0] & 255) >> 3) + TWO_BYTES_FLAG).to_bytes(1, 'big', signed=False)
            out += (((optional_map[1] & 255) >> 3) + (optional_map[0] << 5) & 255).to_bytes(1, 'big', signed=False)
            out += (((optional_map[2] & 255) >> 3) + (optional_map[1] << 5) & 255).to_bytes(1, 'big', signed=False)
            return out
        if optional_map_size <= 29:
            out += (((optional_map[0] & 255) >> 3) + THREE_BYTES_FLAG).to_bytes(1, 'big', signed=False)
            out += (((optional_map[1] & 255) >> 3) + (optional_map[0] << 5) & 255).to_bytes(1, 'big', signed=False)
            out += (((optional_map[2] & 255) >> 3) + (optional_map[1] << 5) & 255).to_bytes(1, 'big', signed=False)
            out += (((optional_map[3] & 255) >> 3) + (optional_map[2] << 5) & 255).to_bytes(1, 'big', signed=False)
            return out
        if optional_map_size <= 504:
            if (optional_map_size & 7) == 0:
                optional_map_byte_count = (optional_map_size >> 3)
            else:
                optional_map_byte_count = (optional_map_size >> 3) + 1
            optional_map_lenght_byte = (optional_map_byte_count & 255) + LENGTH_1_BYTE_FLAG
            out += optional_map_lenght_byte.to_bytes(1, 'big', signed=False)
            out += optional_map[:-1] # we delete last byte
            return out
        if optional_map_size <= 33554432:
            if (optional_map_size & 7) == 0:
                optional_map_byte_count = (optional_map_size >> 3)
            else:
                optional_map_byte_count = (optional_map_size >> 3) + 1
            lenght = optional_map_byte_count + LENGTH_3_BYTE_FLAG;
            lengh_part1 = ((lenght & 16711680) >> 16) & 255
            lengh_part2 = ((lenght & 65280) >> 8) & 255
            lengh_part3 = lenght & 255
            out += lengh_part1.to_bytes(1, 'big', signed=False)
            out += lengh_part2.to_bytes(1, 'big', signed=False)
            out += lengh_part3.to_bytes(1, 'big', signed=False)
            out += optional_map[:-1]
            return out

    def decode(binary_data):
        INPLACE_MASK_FLAG = 0x80
        MASK_LENGTH_2_BYTES_FLAG = 0x40

        first_byte = ByteCodec.decode(binary_data)

        is_long_optional_map = (first_byte & INPLACE_MASK_FLAG) != 0
        if is_long_optional_map:
            first_byte_value = first_byte & 0x3F
            is_lenght_22_bit = (first_byte & MASK_LENGTH_2_BYTES_FLAG) != 0

            mask_length = None
            if is_lenght_22_bit:
                second_byte = ByteCodec.decode(binary_data)
                third_byte = ByteCodec.decode(binary_data)
                mask_length = (first_byte_value << 16) + ((second_byte & 0xFF) << 8) + (third_byte & 0xFF)
            else:
                mask_length = first_byte_value

            # add bytes to optional_map
            for x in range(mask_length):
                byte = ByteCodec.decode(binary_data)
                binary_data.add_byte_to_optional_map(byte)
            return
        else:
            first_byte_value = first_byte << 3

            mask_length = (first_byte & 0x60) >> 5

            if mask_length == 0:
                binary_data.add_byte_to_optional_map(first_byte_value)
                return
            if mask_length == 1:
                second_byte = ByteCodec.decode(binary_data)
                binary_data.add_byte_to_optional_map(first_byte_value + ((second_byte & 0xFF) >> 5))
                binary_data.add_byte_to_optional_map(second_byte << 3)
                return
            if mask_length == 2:
                second_byte = ByteCodec.decode(binary_data)
                third_byte = ByteCodec.decode(binary_data)
                binary_data.add_byte_to_optional_map(first_byte_value + ((second_byte & 0xFF) >> 5))
                binary_data.add_byte_to_optional_map((second_byte << 3) + ((third_byte & 0xFF) >> 5))
                binary_data.add_byte_to_optional_map(third_byte << 3)
                return
            if mask_length == 3:
                second_byte = ByteCodec.decode(binary_data)
                third_byte = ByteCodec.decode(binary_data)
                fourth_byte = ByteCodec.decode(binary_data)
                binary_data.add_byte_to_optional_map(first_byte_value + ((second_byte & 0xFF) >> 5))
                binary_data.add_byte_to_optional_map((second_byte << 3) + ((third_byte & 0xFF) >> 5))
                binary_data.add_byte_to_optional_map((third_byte << 3) + ((fourth_byte & 0xFF) >> 5))
                binary_data.add_byte_to_optional_map(fourth_byte << 3)
                return


class OptionalCodec:
    def encode(params, buffer, codec):
        if params[0]:
            buffer.write_optional_bit(0)
            codec.encode(*params)
            return
        buffer.write_optional_bit(1)
        return

    def decode(params, binary_data, codec):
        if binary_data.read_optional_bit():
            return None
        return codec.decode(*params)


class VectorLevel1Codec:
    def encode(_list, codec, buffer):
        LenghtCodec.encode(len(_list), buffer)
        for item in _list:
            codec.encode(item, buffer)

    def decode(binary_data, codec):
        out_list = []
        vector_lenght = LenghtCodec.decode(binary_data)
        for x in range(vector_lenght):
            item = codec.decode(binary_data)
            out_list.append(item)
        return out_list


class LinearParamCodec:
    def encode(linear_param, buffer):
        DoubleCodec.encode(linear_param.initial_number, buffer)
        DoubleCodec.encode(linear_param.step, buffer)


class RangeCodec:
    def encode(range_in, buffer):
        IntCodec.encode(range_in.max, buffer)
        IntCodec.encode(range_in.min, buffer)

    def decode(stream):
        range_out = range_data.Range()
        range_out.max = IntCodec.decode(stream)
        range_out.min = IntCodec.decode(stream)
        return range_out


class Vector3DCodec:
    def encode(vector, buffer):
        FloatCodec.encode(vector.x, buffer)
        FloatCodec.encode(vector.y, buffer)
        FloatCodec.encode(vector.z, buffer)

    def decode(binary_data):
        vector = Vec3()
        vector.x = FloatCodec.decode(binary_data)
        vector.y = FloatCodec.decode(binary_data)
        vector.z = FloatCodec.decode(binary_data)
        return vector


class LongCodec:
    def encode(number, buffer):
        buffer.write_bytes( number.to_bytes(8, 'big', signed=True) )
        buffer.add_type(console_out.TYPE_TO_COLOR_AND_LENGTH["long"])

    def decode(binary_data):
        bytes = binary_data.read_bytes(8)
        return int.from_bytes(bytes, byteorder='big', signed=True)


class IntCodec:
    def encode(number, buffer):
        buffer.write_bytes( number.to_bytes(4, 'big', signed=True) )
        buffer.add_type(console_out.TYPE_TO_COLOR_AND_LENGTH["int"])

    def decode(binary_data):
        bytes = binary_data.read_bytes(4)
        return int.from_bytes(bytes, byteorder='big', signed=True)


class UintCodec:
    def encode(number, buffer):
        buffer.write_bytes( number.to_bytes(4, 'big', signed=False) )
        buffer.add_type(console_out.TYPE_TO_COLOR_AND_LENGTH["int"])

    def decode(binary_data):
        bytes = binary_data.read_bytes(4)
        return int.from_bytes(bytes, byteorder='big', signed=True)


class ShortCodec:
    def encode(number, buffer):
        buffer.write_bytes( number.to_bytes(2, 'big', signed=True) )
        buffer.add_type(console_out.TYPE_TO_COLOR_AND_LENGTH["short"])

    def decode(binary_data):
        bytes = binary_data.read_bytes(2)
        return int.from_bytes(bytes, byteorder='big', signed=True)


class ByteCodec:
    def encode(number, buffer):
        buffer.write_bytes( number.to_bytes(1, 'big', signed=True) )
        buffer.add_type(console_out.TYPE_TO_COLOR_AND_LENGTH["byte"])

    def decode(binary_data):
        bytes = binary_data.read_bytes(1)
        return int.from_bytes(bytes, byteorder='big', signed=True)


class FloatCodec:
    def encode(number, buffer):
        buffer.write_bytes( struct.pack(">f", number) )
        buffer.add_type(console_out.TYPE_TO_COLOR_AND_LENGTH["float"])

    def decode(binary_data):
        bytes = binary_data.read_bytes(4)
        return struct.unpack(">f", bytes)[0]

class DoubleCodec:
    def encode(number, buffer):
        buffer.write_bytes( struct.pack(">d", number) )
        buffer.add_type(console_out.TYPE_TO_COLOR_AND_LENGTH["double"])

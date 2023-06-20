class BinaryBuffer:
    def __init__(self):
        self.binary_data = bytearray(b"")

        self.optional_map_bit_count = 0
        self.optional_map = bytearray(b"")
        self.optional_map_bits = []
        self.types = []

    def write_bytes_with_index(self, _bytes, position):
        self.binary_data[position:position] = _bytes

    def write_bytes(self, _bytes):
        self.binary_data += _bytes

    def replace_original_binary_data(self, bytes):
        self.binary_data = bytearray(bytes)

    def get_binary_data(self):
        return bytes(self.binary_data)

    def write_optional_bit(self, bit):
        self.optional_map_bits.append(bit)

    # this function will convert optional map to bytes and return the bytes
    def get_optional_map(self):
        for bit in self.optional_map_bits:
            filled_bytes_count = self.optional_map_bit_count >> 3
            if filled_bytes_count + 1 >= len(self.optional_map):
                self.optional_map.append(0)

            bit_index = self.optional_map_bit_count - filled_bytes_count * 8
            if bit == 1:
                self.optional_map[filled_bytes_count] = self.optional_map[filled_bytes_count] | 128 >> bit_index
            self.optional_map_bit_count += 1
        return bytes(self.optional_map)

    def add_type(self, _type):
        self.types.append(_type)

    def add_type_with_index(self, _type, position):
        self.types.insert(position, _type)

    def get_types(self):
        return self.types

    def clear_types(self):
        self.types = []

    def merge_buffer(self, buffer):
        self.binary_data += buffer.binary_data
        self.optional_map_bits += buffer.optional_map_bits
        self.types += buffer.types

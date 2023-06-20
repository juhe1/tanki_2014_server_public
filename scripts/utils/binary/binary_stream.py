class BinaryStream:
    def __init__(self, binary_data):
        self.binary_data = binary_data
        self.position = 0
        self.optional_bits = []
        self.optional_map_position = 0

    def read_all_bytes(self):
        return self.binary_data

    def read_last_bytes(self):
        last_bytes_len = len(self.binary_data[self.position:])
        return self.read_bytes(last_bytes_len)

    def read_bytes(self, count):
        out = self.binary_data[self.position:self.position + count]
        self.position += count
        return out

    def bytes_awaible(self):
        return self.position < len(self.binary_data)

    def read_optional_bit(self):
        self.optional_map_position += 1
        return self.optional_bits[self.optional_map_position - 1]

    def add_byte_to_optional_map(self, byte):
        bit_list = []
        for x in range(8):
            bit_list.insert(0, (byte>>x)&1 == 1)
        self.optional_bits += bit_list

    def seek(self, count):
        self.position += count

    def read_with_index(self, index):
        return self.binary_data[index]

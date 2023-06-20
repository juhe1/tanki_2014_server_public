from utils.log import console_out

#
# this code is ported from decompiled tanki online client source. thats why there is things like _loc4_
#

class BitArea:
    def __init__(self, data, lenght):
        self.data = data
        self.position = 0
        self.length = lenght * 8

    def reset(self):
        self.position = 0

    def read(self, read_len):
        if read_len > 32:
            console_out.color_print("Cannot read more than 32 bit at once (requested " + str(read_len) + ")", "red")
            return
        if self.position + read_len > self.length:
            console_out.color_print("BitArea is out of data: requesed " + str(read_len) + " bits, avaliable:" + str(self.length - self.position), "red")
            return

        out = 0
        i = read_len - 1

        while i >= 0:
            if self.get_bit(self.position):
                out += 1 << i

            self.position += 1
            i -= 1
        return out

    def write(self, write_len, value):
        _loc4_ = False

        if write_len > 32:
            console_out.color_print("Cannot write more that 32 bit at once (requested " + str(write_len) + ")", "red")
            return
        if self.position + write_len > self.length:
            console_out.color_print("BitArea overflow attempt to write " + str(write_len) + " bits, space avaliable:" + str(self.length - self.position), "red")
            return

        write_pos = write_len - 1;
        while write_pos >= 0:
            _loc4_ = (value & 1 << write_pos) != 0
            self.set_bit(self.position,_loc4_)
            self.position += 1
            write_pos -= 1

    def get_bit(self, bit_pos):
        _loc2_ = bit_pos >> 3
        _loc3_ = 7 ^ bit_pos & 7
        return (self.data[_loc2_] & 1 << _loc3_) != 0

    def set_bit(self, bit_pos, bit):
        _loc5_ = 0
        _loc3_ = bit_pos >> 3
        _loc4_ = 7 ^ bit_pos & 7

        if bit:
            self.data[_loc3_] = int(self.data[_loc3_] | 1 << _loc4_);
        else:
            _loc5_ = int(255 ^ 1 << _loc4_);
            self.data[_loc3_] = int(self.data[_loc3_] & _loc5_);

    def get_length(self):
        return self.length

    def get_data(self):
        out = b""
        for number in self.data:
            out += number.to_bytes(1, 'big')
        return out

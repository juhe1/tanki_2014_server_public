# function is from https://stackoverflow.com/questions/2267362/how-to-convert-an-integer-to-a-string-in-any-base
def number_to_base(number, base):
    if number == 0:
        return "0"
    digits = ""
    while number:
        digits = str(number % base) + digits
        number //= base
    return digits

def to_oct(value):
    result = number_to_base(value, 8)
    if len(result) < 2:
        return "0" + result
    else:
        return result
        
def trim_leading_zeros(string):
    i = 0
    while(i < len(string) and string[i] == "0"):
        i += 1
    return string[i:]

def long_to_oct(number):
    number_bytes = number.to_bytes(8, 'big', signed=True)
    high = int.from_bytes( number_bytes[:4] , byteorder='big', signed=False)
    low = int.from_bytes( number_bytes[-4:] , byteorder='big', signed=False)
    
    number1 = 0
    number2 = 0
    version_oct1 = ""
    version_oct2 = ""
    offset = 0
    
    for i in range(5):
        number1 = (high & 63 << 4 + offset) >> offset + 4
        number2 = (low & 63 << offset) >> offset
        version_oct1 = to_oct(number1) + version_oct1
        version_oct2 = to_oct(number2) + version_oct2
        offset += 6
    
    version = version_oct1 + to_oct(((high & 15) << 2) + (low >> 30)) + version_oct2
    return trim_leading_zeros(version)
    
def version_id_to_path(_id, version):
    version_oct = long_to_oct(version)
    id_bytes = _id.to_bytes(8, 'big', signed=False)
    id_int = int.from_bytes(id_bytes[:4], byteorder='big', signed=False)
    id_short = int.from_bytes(id_bytes[4:][:2], byteorder='big', signed=False)
    id_byte1 = int.from_bytes(id_bytes[6:][:1], byteorder='big', signed=False)
    id_byte2 = int.from_bytes(id_bytes[7:][:1], byteorder='big', signed=False)
    
    return number_to_base(id_int, 8) + "/" + number_to_base(id_short, 8) + "/" + number_to_base(id_byte1, 8) + "/" + number_to_base(id_byte2, 8)  + "/" + version_oct + "/"

if __name__ == '__main__':
    while True:
        try:
            _id = int( input("id: ") )
            version = int( input("version: ") )
            print("path:", version_id_to_path(_id, version), "\n")
        except:
            continue
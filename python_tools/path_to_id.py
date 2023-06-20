def path_to_id(path):
    path_splitted = path.split("/")

    _int = int(path_splitted[0] ,base = 8)
    short = int(path_splitted[1] ,base = 8)
    byte1 = int(path_splitted[2] ,base = 8)
    byte2 = int(path_splitted[3] ,base = 8)
    id_bytes = _int.to_bytes(4, 'big', signed=False) + short.to_bytes(2, 'big', signed=False) + byte1.to_bytes(1, 'big', signed=False) + byte2.to_bytes(1, 'big', signed=False)
    return int.from_bytes( id_bytes , byteorder='big', signed=False)
    
while True:
    try:
        path = input("path: ")
        print("id:", path_to_id(path), "\n")
    except:
        continue
    
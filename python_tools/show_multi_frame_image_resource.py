from PIL import Image
import sys
import io

def get_files_from_tara(file_path):
    file_meta_datas = {}
    files = {}
    
    with open(file_path, "rb") as f:
        _bytes = f.read(4)
        file_count = int.from_bytes(_bytes, byteorder="big")
        
        # read files meta data
        for file_id in range(file_count):
            _bytes = f.read(2)
            char_count = int.from_bytes(_bytes, byteorder="big")
            
            _bytes = f.read(char_count)
            file_name = _bytes.decode("utf-8")
            
            _bytes = f.read(4)
            file_len = int.from_bytes(_bytes, byteorder="big")
            
            file_meta_datas[file_name] = file_len
            
        # read files
        for file_name, file_len in file_meta_datas.items():
            files[file_name] = f.read(file_len)
    
    return files
    
def show_images(files):
    for file_name, file_bytes in files.items():
        if file_name in ["i", "a"]:
            image = Image.open(io.BytesIO(file_bytes))
            image.show()
   
def main():   
    if len(sys.argv) > 1:
        files = get_files_from_tara(sys.argv[1])
        show_images(files)
        return
        
    while True:
        path = input("tara path: ")
        files = get_files_from_tara(path)
        show_images(files)
        
main()
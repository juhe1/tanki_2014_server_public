from PIL import Image
import os

def extract_png_alpha(image_path):
    img = Image.open(image_path).convert("RGBA")
    pix = img.load()

    image_size_x, image_size_y = img.size

    new_alpha_img = Image.new( mode="RGB", size=(image_size_x, image_size_y))
    new_alpha_pix = new_alpha_img.load()

    new_img = Image.new( mode="RGB", size=(image_size_x, image_size_y))
    new_pix = new_img.load()

    for y in range(image_size_y):
        for x in range(image_size_x):
            r = pix[x,y][0]
            g = pix[x,y][1]
            b = pix[x,y][2]
            a = pix[x,y][3]
            new_alpha_pix[x,y] = (a, a, a)
            new_pix[x,y] = (r, g, b)
            
    #new_image_name = os.path.basename(image_path).split(".")[0] + ".jpg"
    image_dir = os.path.dirname(image_path)

    new_img.save( os.path.join(image_dir, "image.jpg"), subsampling=0, quality=100 )
    new_alpha_img.save( os.path.join(image_dir, "alpha.jpg"), subsampling=0, quality=100 )
    
while True:
    try:
        extract_png_alpha( input("image path: ") )
    except:
        continue
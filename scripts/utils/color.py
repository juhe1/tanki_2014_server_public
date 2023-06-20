def hex_color_to_rgb(hex_color):
    return (((hex_color & 0xff0000) >> 2*8) / 255, ((hex_color & 0x00ff00) >> 8) / 255, (hex_color & 0x0000ff) / 255)

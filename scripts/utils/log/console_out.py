from utils.log import logger
from termcolor import colored
import server_properties

import time
import colorama
colorama.init()

BACKGROUND_COLORS = {"bright_red":"\033[1;41m", "bright_blue":"\033[1;44m", "bright_magenta":"\033[1;45m", "bright_cyan":"\033[1;46m", "bright_yellow":"\033[1;43m",
                     "blue":"\033[22;44m", "white":"\033[22;47m", "black":"\033[22;40m", "reset":"\033[22;49m"}
FOREGROUND = {"bright_green":"\033[1;32m", "reset":"\033[1;39m"}
TYPE_TO_COLOR_AND_LENGTH = {"byte":[BACKGROUND_COLORS["white"], 1],
                            "short":[BACKGROUND_COLORS["bright_red"], 2],
                            "int":[BACKGROUND_COLORS["bright_blue"], 4],
                            "long":[BACKGROUND_COLORS["bright_magenta"], 8],
                            "float":[BACKGROUND_COLORS["bright_cyan"], 4],
                            "double":[BACKGROUND_COLORS["bright_cyan"], 8]}

is_free = True
def wait_until_free():
    global is_free
    while not is_free:
        time.sleep(0.1)

def print_command(data, command_name):
    console_out.color_print("RECIVED FROM " + command_name + "_space:", "green")
    console_out.hexdump(data)

def safe_print(text, end="\n"):
    global is_free
    wait_until_free()
    is_free = False
    print(text, end=end)
    is_free = True

def log_print(string):
    safe_print(string)
    logger.write_to_log(string)

def color_print(string, color, back=""):
    if back == "":
        safe_print(colored(string, color))
        return

    safe_print(colored(string, color, back))

def log_color_print(string,color, back=""):
    logger.write_to_log(string)

    if back == "":
        safe_print(colored(string, color))
        return

    safe_print(colored(string, color, back))

def print_server_package(buffer, name):
    global is_free
    # write package to cmd
    color_print(name + ":", "green")

    hexdump(buffer.get_binary_data(), buffer.get_types())

def print_package(data):
    if server_properties.DEBUG_ENABLED and server_properties.PRINT_PACKAGES_ENABLED:
        # write client package to console
        console_out.color_print("RECIVED FROM " + channel_id + ":", "green")
        console_out.hexdump(data)

def hexdump(_bytes, types=[]):
    if server_properties.DISABLE_HEX_DUMP or not server_properties.DEBUG_ENABLED: return
    hex_string = _bytes.hex()
    string = ""
    for byte in _bytes:
        try:
            if byte < 33 or byte > 126:
                string += "."
                continue
            byte = byte.to_bytes(1, 'big', signed=True)
            string += byte.decode("ascii")
        except:
            string += "."

    DEFAULT_BACK_COLOR = BACKGROUND_COLORS["black"]
    current_color = None
    color_count = 0

    for line_number in range(len(hex_string)):
        offset_hex = hex(line_number).split("x")[1]
        safe_print("0" * (8 - len(offset_hex)) + offset_hex + ":  ", end="")

        for x in range(16):
            if types == [] and color_count == 0:
                current_color = BACKGROUND_COLORS["reset"]
            elif color_count == 0:
                current_color = types[0][0]
                color_count = types[0][1]
                del types[0]
            color_count -= 1


            hex_byte = hex_string[:2]
            if hex_byte == "": hex_byte = "  "
            hex_string = hex_string[2:]
            if color_count == 0:
                safe_print(current_color + hex_byte + DEFAULT_BACK_COLOR + " ", end="")
            else:
                safe_print(current_color + hex_byte + " ", end="")

        string_part = string[line_number * 16:][:16]
        safe_print(BACKGROUND_COLORS["reset"] + " " + string_part)
        if hex_string == "": return

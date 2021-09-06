# https://github.com/ddxtanx/GoveeAPI/blob/master/controller.py

import subprocess

def check_muted():
    result = subprocess.run(['amixer cget name="Capture Switch"'], stdout=subprocess.PIPE, shell=True)

    if (result.stdout.split()[-1].decode('UTF-8') == "values=off"):
        return True
    else: # could probably check for an on in case its different? idk idc 
        return False




def int_to_hex(intv):
    h = hex(intv).replace("0x", "")
    while len(h) < 2:
        h = "0" + h
    return h
def get_rgb_hex(r,g,b):
    sig = (3*16 + 1) ^ r ^ g ^ b
    bins = [51, 5, 2, r, g, b, 0, 255, 174, 84, 0, 0, 0, 0, 0, 0, 0, 0, 0, sig]
    bins_str = map(int_to_hex, bins)
    return "".join(bins_str)
def get_brightness_hex(bright):
    sig = (3*16 + 3) ^ (4) ^ bright
    bins = [51, 4, bright, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, sig]
    bins_str = map(int_to_hex, bins)
    return "".join(bins_str)



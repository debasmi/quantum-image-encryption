from block import applyEncryptionByBlocks
import numpy as np
from image_utils import generateControlledImagematrix
from threeBitColour import convert_to_3bit_values, convert_from_3bit_values
from math import log2
from constants import *

from analysis import keySenstivityANalysis

def create_random_image(n, x):
    # Generate a random image with shape (n, n, 3) and values between 0 and x
    image = np.random.randint(0, x + 1, size=(n, n, 3), dtype=np.uint8)
    return image

def encryptImage(image_array:np.ndarray, control_array:np.ndarray, blocks_size:int = 2, color_size:int = 3):
    x = image_array.shape[0]
    y = image_array.shape[1]
    z = image_array.shape[2]
    L = int(log2(x)) + int(log2(y))
    
    enc_channels = []

    for k in range(z):
        channel = [[image_array[i][j][k] for j in range(y)] for i in range(x)]  # This channel
        channel = np.array(channel)
        control_channel = control_array[k]

        print(f"Encrypting channel {k+1} of {z}")
        enc_channel = applyEncryptionByBlocks(channel, control_channel, L, blocks_size=blocks_size, mode="enc", color_size=color_size)
        enc_channels.append(enc_channel)
        
    recombined_array = [[[enc_channels[c][i][j] for c in range(z)] for j in range(y)] for i in range(x)]
    return np.array(recombined_array)

if __name__ == "__main__":
    # array = convert_to_3bit_values(IMAGE)
    # convert_from_3bit_values(array, RESULT_PATH+"input.png")

    array = convert_to_3bit_values(IMAGE)
    convert_from_3bit_values(array, RESULT_PATH+"input.png")

    control_image = generateControlledImagematrix(row=array.shape[0], col=array.shape[1], channel=array.shape[2], k0=K_0, psi=PSI, COLORSIZE=COLOR_SIZE)
    enc_image = encryptImage(array, control_image, blocks_size=BLOCK_SIZE, color_size=COLOR_SIZE)
    convert_from_3bit_values(enc_image, RESULT_PATH+"encrypted.png")
    
    keySenstivityANalysis(convert_to_3bit_values(RESULT_PATH+"encrypted.png"))
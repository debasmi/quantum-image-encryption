from constants import PSI, K_0, ANALYSIS_PATH, KEY_DELTA, BLOCK_SIZE, COLOR_SIZE
from image_utils import generateControlledImagematrix
from block import applyEncryptionByBlocks
from threeBitColour import convert_from_3bit_values
import numpy as np
from math import log2


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

def keySenstivityANalysis(enc_matrix:np.ndarray, blocks_size:int = BLOCK_SIZE, color_size:int = COLOR_SIZE, psi:int = PSI, k_0:int = K_0, key_delta:int = KEY_DELTA):

    control_image = generateControlledImagematrix(row=enc_matrix.shape[0], col=enc_matrix.shape[1], channel=enc_matrix.shape[2], k0=K_0, psi=PSI, COLORSIZE=COLOR_SIZE)
    enc_image = encryptImage(enc_matrix, control_image, blocks_size=blocks_size, color_size=color_size)
    convert_from_3bit_values(enc_image, ANALYSIS_PATH+"decrypted.png")

    
    '''control_image = generateControlledImagematrix(row=enc_matrix.shape[0], col=enc_matrix.shape[1], channel=enc_matrix.shape[2], psi=psi+key_delta, k0=k_0, COLORSIZE=COLOR_SIZE)
    enc_image = encryptImage(enc_matrix, control_image, blocks_size=blocks_size, color_size=color_size)
    convert_from_3bit_values(enc_image, ANALYSIS_PATH+"psiPlus.png")
    
    
    control_image = generateControlledImagematrix(row=enc_matrix.shape[0], col=enc_matrix.shape[1], channel=enc_matrix.shape[2], psi=psi, k0=k_0+key_delta, COLORSIZE=COLOR_SIZE)
    enc_image = encryptImage(enc_matrix, control_image, blocks_size=blocks_size, color_size=color_size)
    convert_from_3bit_values(enc_image, ANALYSIS_PATH+"initialPlus.png")
    
    
    control_image = generateControlledImagematrix(row=enc_matrix.shape[0], col=enc_matrix.shape[1], channel=enc_matrix.shape[2], psi=psi+key_delta, k0=k_0+key_delta, COLORSIZE=COLOR_SIZE)
    enc_image = encryptImage(enc_matrix, control_image, blocks_size=blocks_size, color_size=color_size)
    convert_from_3bit_values(enc_image, ANALYSIS_PATH+"plusPlus.png")'''

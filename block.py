import numpy as np
from encrypt import encrypt
from utils import progress_bar
from threeBitColour import convert_from_3bit_values
from constants import RESULT_PATH
from math import log2

def padMatrix(M:np.ndarray, blocks_size:int):
    n, m = M.shape
    
    # Pad matrices to make them divisible by blocks_size (if necessary)
    pad_n = (blocks_size - n % blocks_size) % blocks_size  # Number of rows to pad
    pad_m = (blocks_size - m % blocks_size) % blocks_size  # Number of columns to pad
    padded_M = np.pad(M, ((0, pad_n), (0, pad_m)), mode='constant', constant_values=0)
    return padded_M

def applyEncryptionByBlocks(matrix1:np.ndarray, matrix2:np.ndarray, l:int, blocks_size:int = 2, mode:str="enc", color_size:int = 8):
    # Ensure both matrices have the same shape
    assert matrix1.shape == matrix2.shape, "Both matrices must have the same shape. Matrix1: {}, Matrix2: {}".format(matrix1.shape, matrix2.shape)
    matrix1 = padMatrix(matrix1, blocks_size)
    matrix2 = padMatrix(matrix2, blocks_size)
    

    # Get the dimensions of the matrices
    n, m = matrix1.shape

    # Prepare the output matrix
    output_matrix = np.zeros_like(matrix1)
    
    # Iterate over 2x2 blocks
    update = progress_bar(n, prefix='Progress', length=40)
    for i in range(0, n, blocks_size):
        for j in range(0, m, blocks_size):
            # Extract 2x2 blocks from both matrices
            block1 = matrix1[i:i+blocks_size, j:j+blocks_size]
            block2 = matrix2[i:i+blocks_size, j:j+blocks_size]
            if mode == "enc":
                # Apply the operation to the bxb blocks
                # try:
                result_block = encrypt(block1, block2, COLOR_SIZE=color_size, l = 2 * int(log2(blocks_size)) )#
                # except:
                #     print(block1, block2, blocks_size)
                # print("Here", i, j)
            update(i + blocks_size + j/m)
            # Place the result in the output matrix
            output_matrix[i:i+blocks_size, j:j+blocks_size] = result_block
        update(i+blocks_size)
        # compressedMatrixToImage(output_matrix, output_path="./result/temp.png")
    print() #Adding newline after progressbar

    # Return the output matrix with possible padding
    return output_matrix

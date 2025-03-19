import numpy as np
from PIL import Image

def imageToGrayscaleMatrix(image_path:str):    
    image = Image.open(image_path)
    grayscale_image = image.convert("L")
    grayscale_array = np.array(grayscale_image)
    return grayscale_array

def grayScaleMatrixToImage(m: np.ndarray, output_path:str=None):
    image = Image.fromarray(m.astype(np.uint8))
    if output_path:
        image.save(output_path)  # Save the image to a file

def generateControlledImagematrix(row:int, col:int, channel:int=1, psi:float = 2, k0:float = 0.5, COLORSIZE:int = 8)-> np.ndarray:
    M:list[list[list[int]]] = []
    k_i = k0
    for k in range (channel):
        channel_M:list[list[int]] = []
        for i in range (row):
            row_M:list[int] = []
            for j in range(col):
                temp = (psi * (k_i - k_i**2) + (4-psi) * np.sin(np.pi * k_i) /4 ) %1
                temp2 = ( (np.floor( temp*10**8 ) ) %256 ) % 2**COLORSIZE
                row_M.append(int(temp2))
                k_i = temp
            channel_M.append(row_M)
        M.append(channel_M)

    return np.array(M)
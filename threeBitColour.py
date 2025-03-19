import numpy as np
from PIL import Image
import sys

def convert_to_3bit_values(image_path)  -> np.ndarray:
    """
    Convert an image from 8-bit per channel to raw 3-bit values (0-7 per channel).
    
    Parameters:
    image_path (str): Path to the input image
    
    Returns:
    np.ndarray: Array of raw 3-bit values (0-7) for each channel
    """
    # Open the image
    img = Image.open(image_path)
    
    # Convert to RGB if it's not already
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Convert to numpy array for easier manipulation
    img_array = np.array(img)
    
    # Quantize each channel to 3-bit (values 0-7)
    r_channel_raw = img_array[:, :, 0] // 32
    g_channel_raw = img_array[:, :, 1] // 32
    b_channel_raw = img_array[:, :, 2] // 32
    
    # Create raw output array with values 0-7
    raw_output = np.stack([r_channel_raw, g_channel_raw, b_channel_raw], axis=2)
    
    return raw_output

def convert_from_3bit_values(raw_array, output_path=None):
    """
    Convert a raw 3-bit array (values 0-7) back to 8-bit and save as an image.
    
    Parameters:
    raw_array (np.ndarray): Array with values 0-7 for each channel
    output_path (str, optional): Path to save the output image. If None, will save as 'output_3bit.jpg'
    
    Returns:
    PIL.Image: The converted image
    """
    # Make sure array is the right type
    raw_array = raw_array.astype(np.uint8)
    
    # Scale back to 8-bit range (0-255)
    r_channel = (raw_array[:, :, 0] * 36).clip(0, 255).astype(np.uint8)
    g_channel = (raw_array[:, :, 1] * 36).clip(0, 255).astype(np.uint8)
    b_channel = (raw_array[:, :, 2] * 36).clip(0, 255).astype(np.uint8)
    
    # Combine channels for the 8-bit representation
    result_array = np.stack([r_channel, g_channel, b_channel], axis=2)
    result_img = Image.fromarray(result_array)
    
    # Save the result if output_path is provided
    if output_path is not None:
        result_img.save(output_path)
        print(f"Image saved as {output_path}")
    else:
        default_output = "output_3bit.jpg"
        result_img.save(default_output)
        print(f"Image saved as {default_output}")
    
    return result_img

def main():
    if len(sys.argv) < 2:
        print("Usage: python 3bitColour.py <input_image_path> [output_image_path]")
        sys.exit(1)
    
    input_image_path = sys.argv[1]
    output_image_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Example workflow using both functions
    print("Converting to 3-bit values...")
    raw_values = convert_to_3bit_values(input_image_path)
    print("Raw 3-bit values shape:", raw_values.shape)
    print(raw_values)
    
    # Here you could process or modify the raw_values array
    
    # print("Converting back to image and saving...")
    # result_img = convert_from_3bit_values(raw_values, output_image_path)
    
    # print("Process complete!")

if __name__ == "__main__":
    main()
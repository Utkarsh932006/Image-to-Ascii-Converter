"""
Image to ASCII Art Converter

This script converts an image from a local file or a URL into ASCII art.

Dependencies:
    - Pillow (PIL)
    - NumPy
    - requests

Install them using pip or uv:
    pip install Pillow numpy requests
    uv add Pillow numpy requests

Usage:
    python image_to_ascii.py <path_or_url_to_image> --width <width_in_chars> --output <output_file_path>

Example:
    # From a local file
    python image_to_ascii.py pictures/python.jpg --width 80

    # From a URL
    python image_to_ascii.py https://i.postimg.cc/t4Cmn7wC/py.png --width 100 --output custom_art.txt

Author: Utkarsh Mishra
Date: 2025-07-25
License: MIT License
"""

import argparse
import numpy as np
import requests
import os
from PIL import Image
import io

# Characters sorted from darkest to lightest. Using more characters gives better gradients.
# In my results on a generic LED screen, the following characters provide a good balance
# between detail and readability.
ASCII_CHARS = '##@@MMBB88NNHHOOGGPPEEXXFFVVYY22ZZCC77LLjjll11rrii;;;:::....  '

def preprocess_image(image_source):
    """
    Handles image loading, transparency removal, and conversion to grayscale.

    Args:
        image_source (str or bytes): A file path, URL, or image data in bytes.

    Returns:
        PIL.Image.Image: The preprocessed, grayscale image object, or None on failure.
    """
    try:
        # Handle image from a URL
        if isinstance(image_source, str) and image_source.startswith('http'):
            response = requests.get(image_source)
            response.raise_for_status()  # Raise an exception for bad status codes
            image_data = io.BytesIO(response.content)
            img = Image.open(image_data)
        # Handle image from a local file path
        elif isinstance(image_source, str):
            img = Image.open(image_source)
        # Handle image from bytes
        else:
            img = Image.open(image_source)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching image from URL: {e}")
        return None
    except FileNotFoundError:
        print(f"Error: Image file not found at '{image_source}'")
        return None
    except Exception as e:
        print(f"An error occurred while opening the image: {e}")
        return None

    # Remove transparency by pasting it onto a white background
    if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
        alpha = img.convert('RGBA').split()[-1]
        bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
        bg.paste(img, mask=alpha)
        img = bg

    return img.convert('L') # Convert to grayscale

def image_to_ascii(img, width):
    """
    Converts a grayscale image to an ASCII string.

    Args:
        img (PIL.Image.Image): The grayscale image object.
        width (int): The desired width of the ASCII art in characters.

    Returns:
        str: The generated ASCII art as a single string.
    """
    img_width, img_height = img.size

    # Adjust height to account for character aspect ratio (characters are ~2x taller than wide)
    aspect_ratio = img_height / img_width
    height = max(1, int(width * aspect_ratio * 0.5))

    # Resize the image to match the ASCII art dimensions
    resized_img = img.resize((width, height))

    # Convert image to numpy array for easier manipulation
    pixels = np.array(resized_img)

    # Map each pixel's brightness (0-255) to an ASCII character
    brightness_step = 255 / (len(ASCII_CHARS) - 1)
    indices = (pixels / brightness_step).astype(int)

    # Create the ASCII string
    ascii_rows = ["".join(ASCII_CHARS[i] for i in row) for row in indices]
    return "\n".join(ascii_rows)

def save_output(text, filepath):
    """Saves the given text to a file, creating directories if needed."""
    try:
        # Ensure the directory for the output file exists
        output_dir = os.path.dirname(filepath)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"ASCII art saved to '{filepath}'")
    except Exception as e:
        print(f"Error saving file: {e}")

def main():
    """Main function to parse arguments and run the converter."""
    parser = argparse.ArgumentParser(description="Convert an image to ASCII art.")
    parser.add_argument("image_source", help="The path or URL to the input image.")
    parser.add_argument("--width", type=int, default=100, help="The width of the output ASCII art in characters.")
    parser.add_argument("--output", default="output/art.txt", help="The path to save the output text file.")

    args = parser.parse_args()

    image = preprocess_image(args.image_source)

    if image:
        ascii_art = image_to_ascii(image, args.width)
        print(ascii_art)
        save_output(ascii_art, args.output)

if __name__ == '__main__':
    main()

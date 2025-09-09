
import unittest
from unittest.mock import patch, MagicMock
import numpy as np
from PIL import Image
import io
import requests

from main import preprocess_image, image_to_ascii, ASCII_CHARS

class TestImageToAsciiConverter(unittest.TestCase):

    def test_image_to_ascii_conversion(self):
        """Tests the core ASCII conversion logic with a predictable image."""
        # Create a simple 2x1 image: one black pixel, one white pixel.
        img = Image.new('L', (2, 1))
        img.putpixel((0, 0), 0)    # Black
        img.putpixel((1, 0), 255)  # White

        # The expected output should be the first and last characters of ASCII_CHARS
        expected_ascii = ASCII_CHARS[0] + ASCII_CHARS[-1]
        
        img_square = Image.new('L', (2, 2))
        pixels = img_square.load()
        pixels[0, 0] = 0      # Top-left: Black
        pixels[1, 0] = 255    # Top-right: White
        pixels[0, 1] = 0      # Bottom-left: Black
        pixels[1, 1] = 255    # Bottom-right: White

        # The function's aspect ratio correction will turn a 2x2 image into a 2x1 output.
        expected_square_ascii = (ASCII_CHARS[0] + ASCII_CHARS[-1])

        result = image_to_ascii(img_square, width=2)
        self.assertEqual(result, expected_square_ascii)

    @patch('main.requests.get')
    def test_preprocess_image_from_url_success(self, mock_get):
        """Tests successful image fetching from a URL using a mock request."""
        # Create a fake image in memory
        fake_image_bytes = io.BytesIO()
        Image.new('RGB', (10, 10), color = 'red').save(fake_image_bytes, 'PNG')
        fake_image_bytes.seek(0)

        # Configure the mock to return a successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = fake_image_bytes.read()
        mock_get.return_value = mock_response

        # Call the function with a fake URL
        image = preprocess_image('http://fake-url.com/image.png')
        
        # Assert that we got a valid, grayscale image object back
        self.assertIsInstance(image, Image.Image)
        self.assertEqual(image.mode, 'L')

    @patch('main.requests.get')
    def test_preprocess_image_from_url_failure(self, mock_get):
        """Tests how preprocess_image handles a request failure."""
        # Configure the mock to raise a connection error
        mock_get.side_effect = requests.exceptions.RequestException("Failed to connect")

        # Call the function
        image = preprocess_image('http://unreachable-url.com/image.png')

        # Assert that the function returns None on failure
        self.assertIsNone(image)

if __name__ == '__main__':
    unittest.main()

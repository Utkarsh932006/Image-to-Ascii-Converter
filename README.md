# Image to ASCII Converter

A Python command-line tool to convert images from local files or URLs into ASCII art.

## Features

- Convert images from local file paths.
- Convert images directly from URLs.
- Adjustable output width to control detail level.
- Handles transparency in images by applying a white background.
- Saves the generated ASCII art to a text file.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Utkarsh932006/Image-to-Ascii-Converter.git
    cd image-to-ascii
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install the dependencies:**
    The project uses `numpy`, `Pillow`, and `requests`. You can install them directly from the `pyproject.toml` file.
    ```bash
    pip install .
    ```
    or
    '''bash
    uv sync --all-packages
    '''

## Usage

The script is run from the command line and accepts an image source (file path or URL) and optional arguments for width and output file path.

### Command-Line Options

To see all available options, use the `--help` flag:
```bash
python main.py --help
```
```
usage: main.py [-h] [--width WIDTH] [--output OUTPUT] image_source

Convert an image to ASCII art.

positional arguments:
  image_source   The path or URL to the input image.

options:
  -h, --help       show this help message and exit
  --width WIDTH    The width of the output ASCII art in characters.
  --output OUTPUT  The path to save the output text file.
```

### Examples

1.  **Convert a local image with a specific width:**
    ```bash
    python main.py path/to/your/image.jpg --width 120
    ```

2.  **Convert an image from a URL and save to a custom file:**
    ```bash
    python main.py https://www.python.org/static/community_logos/python-logo-master-v3-TM.png --width 80 --output custom_art.txt
    ```
    This will print the art to the console and save it in `custom_art.txt`.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

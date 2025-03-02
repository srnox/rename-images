# Image Renamer

A simple Python script to rename image files based on a list of item names.

## Description

This script reads a list of item names from a text file and renames a set of images accordingly. It's useful for batch renaming image files to match product names, inventory items, or any other naming scheme you need.

## Features

- Reads item names from a text file in two formats:
  - Simple list (one name per line)
  - Format with `item = "name"` syntax
- Supports various image extensions (default: .png)
- Creates a new directory with renamed copies (preserves originals)
- Provides detailed progress information

## Requirements

- Python 3.x
- No external dependencies required (uses only standard library modules)

## Setup

1. Clone this repository or download the script
2. Create the following directory structure:
   ```
   project_folder/
   ├── rename_images.py
   ├── paste.txt (or items.txt, item_names.txt)
   └── original_images/
       ├── image1.png
       ├── image2.png
       └── ...
   ```

## Usage

1. Place your images in the "original_images" folder
2. Create a text file with your item names (one per line)
3. Run the script:
   ```
   python rename_images.py
   ```
4. Find your renamed images in the "renamed_images" folder

## Text File Format

The script supports two formats for the item names text file:

### Simple List
```
Item Name 1
Item Name 2
Item Name 3
```

### Alternative Format
```
item = "Item Name 1"
item = "Item Name 2"
item = "Item Name 3"
```

## Customization

You can modify the following variables in the `main()` function:

- `text_file`: Path to your text file with item names
- `source_dir`: Directory containing the original images
- `output_dir`: Directory where renamed images will be saved
- `image_extension`: File extension of your images (e.g., ".jpg", ".png")

## License

[MIT License](LICENSE)

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.
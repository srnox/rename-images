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
   ├── original_images/     (create this folder and place images here)
   │   ├── image1.png
   │   ├── image2.png
   │   └── ...
   └── renamed_images/      (this folder will be created automatically for output)
   ```

   **Important:**
   - You MUST create the "original_images" folder and place all your images there
   - The "renamed_images" folder will be created automatically when the script runs
   - All renamed images will be saved to the "renamed_images" folder (original files remain untouched)

## Usage

1. Create the "original_images" folder if it doesn't exist
2. Place all your images that need to be renamed in the "original_images" folder
3. Create a text file with your item names (one per line)
4. Run the script:
   ```
   python rename_images.py
   ```
5. Find your renamed images in the "renamed_images" folder
   - This folder will be created automatically
   - Your original images will remain unchanged in the "original_images" folder

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
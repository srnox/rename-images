# Image Renamer

A Python utility for efficiently renaming multiple image files based on item names from a text file.

## Features

- **Multi-threaded processing** for faster renaming of large image sets
- **Multiple text file formats** supported:
  - Simple list (one name per line)
  - Format with `item = "name"` syntax
- **Command-line interface** with configurable options
- **Proper logging system** with adjustable verbosity levels
- **Error handling** with detailed error messages
- **Filename sanitization** to avoid invalid characters
- **UTF-8 support** for international character sets
- **Original files preservation** (creates copies with new names)

## Requirements

- Python 3.6 or newer
- No external dependencies (uses only standard library)

## Installation

1. Clone this repository or download the script
2. Ensure you have Python 3.6+ installed

## Directory Structure

```
project_folder/
├── image_renamer.py
├── paste.txt (or items.txt, item_names.txt)
├── original_images/     (place your images here)
│   ├── image1.png
│   ├── image2.png
│   └── ...
└── renamed_images/      (output folder, created automatically)
```

## Basic Usage

1. Place your images in the `original_images` folder
2. Create a text file named `paste.txt` with your item names
3. Run the script:
   ```
   python image_renamer.py
   ```
4. Find your renamed images in the `renamed_images` folder

## Advanced Usage

The script supports various command-line arguments for customization:

```
python image_renamer.py --text-file items.txt --source-dir my_images --output-dir renamed --extension .jpg --workers 8 --verbose
```

### Command-line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--text-file` | Path to text file with item names | Auto-detected* |
| `--source-dir` | Directory with original images | `original_images` |
| `--output-dir` | Directory for renamed images | `renamed_images` |
| `--extension` | Image file extension | `.png` |
| `--workers` | Number of worker threads | `4` |
| `--verbose` | Enable verbose logging | `False` |

*Auto-detection tries these files in order: `paste.txt`, `paste`, `item_names.txt`, `items.txt`

## Text File Formats

### Simple List
```
First Item
Second Item
Third Item
```

### Alternative Format
```
item = "First Item"
item = "Second Item"
item = "Third Item"
```

## How It Works

1. The script reads item names from your text file
2. It finds all images with the specified extension in the source directory
3. It creates the output directory if it doesn't exist
4. It copies each image to the output directory with a new name based on the corresponding item name
5. Original images remain unchanged in the source directory

## Error Handling

- If there are more images than item names, only the first N images (matching the number of item names) will be renamed
- If there are more item names than images, only the first N item names will be used
- Invalid characters in item names are automatically replaced with underscores
- Detailed error messages are provided if files cannot be read or processed

## Examples

### Basic Example
```bash
python image_renamer.py
```

### Custom Paths and Extension
```bash
python image_renamer.py --text-file products.txt --source-dir raw_photos --output-dir processed --extension .jpg
```

### Maximum Performance
```bash
python image_renamer.py --workers 12
```

### Debugging Issues
```bash
python image_renamer.py --verbose
```

## License

[MIT License](LICENSE)

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.
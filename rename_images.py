import os
import re
import shutil
from pathlib import Path

def extract_item_names(text_file):
    """Extract item names from the text file."""
    item_names = []
    
    # Try both formats - plain list and {item = "name"} format
    with open(text_file, 'r') as file:
        content = file.read()
        
        # Try the {item = "name"} format first
        pattern = r'item = "(.*?)"'
        matches = re.findall(pattern, content)
        
        if matches:
            item_names = matches
        else:
            # If no matches, assume it's a plain list with one name per line
            item_names = [line.strip() for line in content.split('\n') if line.strip()]
    
    print(f"Found {len(item_names)} item names in the text file.")
    return item_names

def rename_images(source_dir, output_dir, item_names, image_extension='.png'):
    """Rename images based on the item names."""
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Get all image files in the source directory
    image_files = sorted([f for f in os.listdir(source_dir) 
                         if f.lower().endswith(image_extension)])
    
    print(f"Found {len(image_files)} images in the source directory.")
    
    # Check if we have enough item names for images
    if len(image_files) < len(item_names):
        print(f"Warning: Only {len(image_files)} images found, but {len(item_names)} item names provided.")
        item_names = item_names[:len(image_files)]
    elif len(image_files) > len(item_names):
        print(f"Warning: {len(image_files)} images found, but only {len(item_names)} item names provided.")
        print(f"The last {len(image_files) - len(item_names)} images will not be renamed.")
        image_files = image_files[:len(item_names)]
    
    # Rename and copy images
    for i, (image_file, item_name) in enumerate(zip(image_files, item_names)):
        source_path = os.path.join(source_dir, image_file)
        new_filename = f"{item_name}{image_extension}"
        destination_path = os.path.join(output_dir, new_filename)
        
        # Copy the file with the new name
        shutil.copy2(source_path, destination_path)
        print(f"Renamed {image_file} to {new_filename} ({i+1}/{len(item_names)})")

def main():
    # Configuration - MODIFY THESE VALUES
    text_file = "paste.txt"  # Path to your text file with item names
    
    # Try alternative filenames if paste.txt doesn't exist
    if not os.path.exists(text_file):
        alternatives = ["paste", "item_names.txt", "items.txt"]
        for alt in alternatives:
            if os.path.exists(alt):
                text_file = alt
                print(f"Using {text_file} instead of paste.txt")
                break
    
    source_dir = "original_images"  # Directory containing the original images
    output_dir = "renamed_images"  # Directory where renamed images will be saved
    image_extension = ".png"  # Change this if your images have a different extension
    
    # Extract item names
    item_names = extract_item_names(text_file)
    
    if not item_names:
        print("No item names found. Please check your text file.")
        return
    
    # Rename images
    rename_images(source_dir, output_dir, item_names, image_extension)
    print("Image renaming complete!")

if __name__ == "__main__":
    main()
import os
import re
import shutil
import argparse
import logging
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import List, Optional, Tuple


def setup_logging(verbose: bool = False) -> None:
    """Configure logging based on verbosity level."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def extract_item_names(text_file: str) -> List[str]:
    """
    Extract item names from the text file.
    
    Args:
        text_file: Path to the text file containing item names
        
    Returns:
        List of extracted item names
    """
    try:
        with open(text_file, 'r', encoding='utf-8') as file:
            content = file.read()
            
            # Try the {item = "name"} format first
            pattern = r'item\s*=\s*"(.*?)"'
            matches = re.findall(pattern, content)
            
            if matches:
                logging.info(f"Found {len(matches)} item names in {item = 'name'} format")
                return matches
            
            # If no matches, try plain list with one name per line
            lines = [line.strip() for line in content.split('\n') if line.strip()]
            if lines:
                logging.info(f"Found {len(lines)} item names in plain list format")
                return lines
            
            logging.warning("No item names found in the text file")
            return []
            
    except Exception as e:
        logging.error(f"Error reading text file: {e}")
        return []


def find_text_file() -> Optional[str]:
    """
    Find a valid text file with item names from several possible options.
    
    Returns:
        Path to the found text file or None if no file was found
    """
    candidates = ["paste.txt", "paste", "item_names.txt", "items.txt"]
    
    for candidate in candidates:
        if os.path.exists(candidate):
            logging.info(f"Using text file: {candidate}")
            return candidate
    
    logging.error("No valid text file found")
    return None


def process_image(args: Tuple[str, str, str, str]) -> Optional[str]:
    """
    Process a single image (copy and rename).
    
    Args:
        args: Tuple containing (source_path, destination_path, original_name, new_name)
        
    Returns:
        New filename if successful, None otherwise
    """
    source_path, destination_path, original_name, new_name = args
    
    try:
        shutil.copy2(source_path, destination_path)
        return new_name
    except Exception as e:
        logging.error(f"Error processing {original_name}: {e}")
        return None


def rename_images(source_dir: str, output_dir: str, item_names: List[str], 
                 image_extension: str = '.png', max_workers: int = 4) -> int:
    """
    Rename images based on the item names using parallel processing.
    
    Args:
        source_dir: Directory containing original images
        output_dir: Directory where renamed images will be saved
        item_names: List of new item names
        image_extension: File extension of the images
        max_workers: Maximum number of threads for parallel processing
        
    Returns:
        Number of successfully renamed images
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Get all image files in the source directory
    source_path = Path(source_dir)
    image_files = sorted([f for f in source_path.iterdir() 
                         if f.suffix.lower() == image_extension.lower()])
    
    logging.info(f"Found {len(image_files)} images in the source directory")
    
    # Check if we have enough item names for images
    if len(image_files) < len(item_names):
        logging.warning(f"Only {len(image_files)} images found, but {len(item_names)} item names provided")
        item_names = item_names[:len(image_files)]
    elif len(image_files) > len(item_names):
        logging.warning(f"{len(image_files)} images found, but only {len(item_names)} item names provided")
        logging.warning(f"The last {len(image_files) - len(item_names)} images will not be renamed")
        image_files = image_files[:len(item_names)]
    
    # Prepare the arguments for parallel processing
    tasks = []
    for image_file, item_name in zip(image_files, item_names):
        # Sanitize filename to remove invalid characters
        safe_name = re.sub(r'[\\/*?:"<>|]', '_', item_name)
        
        source_path = str(image_file)
        new_filename = f"{safe_name}{image_extension}"
        destination_path = os.path.join(output_dir, new_filename)
        
        tasks.append((source_path, destination_path, image_file.name, new_filename))
    
    # Process images in parallel
    successful_renames = 0
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for i, result in enumerate(executor.map(process_image, tasks)):
            if result:
                successful_renames += 1
                logging.debug(f"Renamed image {i+1}/{len(tasks)}: {result}")
    
    logging.info(f"Successfully renamed {successful_renames} out of {len(tasks)} images")
    return successful_renames


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Rename images based on item names in a text file')
    parser.add_argument('--text-file', type=str, help='Path to text file with item names')
    parser.add_argument('--source-dir', type=str, default='original_images', help='Directory with original images')
    parser.add_argument('--output-dir', type=str, default='renamed_images', help='Directory for renamed images')
    parser.add_argument('--extension', type=str, default='.png', help='Image file extension')
    parser.add_argument('--workers', type=int, default=4, help='Number of worker threads')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose logging')
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.verbose)
    
    # Find text file if not specified
    text_file = args.text_file or find_text_file()
    if not text_file:
        logging.error("No text file specified or found. Exiting.")
        return 1
    
    # Extract item names
    item_names = extract_item_names(text_file)
    if not item_names:
        logging.error("No item names found. Please check your text file.")
        return 1
    
    # Rename images
    successful_renames = rename_images(
        args.source_dir, 
        args.output_dir, 
        item_names, 
        args.extension,
        args.workers
    )
    
    if successful_renames > 0:
        logging.info(f"Image renaming complete! {successful_renames} images renamed.")
        return 0
    else:
        logging.error("No images were successfully renamed.")
        return 1


if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)
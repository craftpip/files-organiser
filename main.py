import os
import shutil
import logging
import sys
from PIL import Image
from moviepy.editor import VideoFileClip

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Define file categories and formats
VIDEO_FORMATS = (".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv")
IMAGE_FORMATS = (".jpg", ".jpeg", ".png", ".bmp", ".tiff")
GIF_FORMATS = (".gif",)

# Function to create a directory if it doesn't exist
def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)
        logging.info(f"Created folder: {path}")


# Function to classify videos as portrait or landscape
def classify_video(filepath):
    try:
        clip = VideoFileClip(filepath)
        width, height = clip.size
        clip.reader.close()
        if height > width:
            return "Video_Portrait"
        else:
            return "Video_Landscape"
    except Exception as e:
        logging.error(f"Error processing video {filepath}: {e}")
        return None


# Function to classify images
def classify_image(filepath):
    try:
        with Image.open(filepath) as img:
            if img.format == "GIF":
                return "GIF"
            return "Pictures"
    except Exception as e:
        logging.error(f"Error processing image {filepath}: {e}")
        return None


# Function to remove empty directories
def remove_empty_dirs(src_folder):
    # Walk the directory tree from the bottom up
    for root, dirs, _ in os.walk(src_folder, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            # Remove directory if it's empty
            if not os.listdir(dir_path):
                os.rmdir(dir_path)
                logging.info(f"Removed empty directory: {dir_path}")


# Function to organize files in a folder recursively
def organize_files(src_folder):
    # Define destination folder names
    folders = ["Video_Portrait", "Video_Landscape", "Pictures", "GIF", "Others"]

    # Create required folders
    for folder in folders:
        create_folder(os.path.join(src_folder, folder))

    for root, _, files in os.walk(src_folder):
        for file in files:
            file_path = os.path.join(root, file)
            _, ext = os.path.splitext(file.lower())

            # Ignore hidden files (macOS or otherwise)
            if file.startswith("._") or file.startswith("."):
                logging.info(f"Ignoring hidden file: {file}")
                continue

            # Skip files if they are already inside one of the target folders
            if any(folder in root for folder in folders):
                continue

            # Categorize the file based on its format
            if ext in VIDEO_FORMATS:
                category = classify_video(file_path)
            elif ext in IMAGE_FORMATS:
                category = classify_image(file_path)
            elif ext in GIF_FORMATS:
                category = "GIF"
            else:
                category = "Others"  # Move unmatched files to Others folder

            # Move file if a category is determined
            if category:
                destination = os.path.join(src_folder, category, file)
                try:
                    logging.info(f"Moving {file} to {category}")
                    shutil.move(file_path, destination)
                except PermissionError as e:
                    logging.warning(
                        f"PermissionError: Could not move {file}. File is in use by another process. Skipping..."
                    )
                except FileNotFoundError as e:
                    logging.warning(
                        f"FileNotFoundError: {file_path} does not exist. Skipping..."
                    )
                except Exception as e:
                    logging.error(f"Error moving {file}: {e}")

    # Remove empty directories after processing
    remove_empty_dirs(src_folder)


if __name__ == "__main__":
    # Check if a directory is provided via command line
    if len(sys.argv) > 1:
        source_folder = sys.argv[1]
    else:
        source_folder = input("Enter the path to the folder you want to organize: ")

    organize_files(source_folder)


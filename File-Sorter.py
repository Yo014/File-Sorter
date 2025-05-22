"/Users/santomukiza/Downloads"
"/Users/santomukiza/Desktop"
import os
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# --- Configuration ---
DOWNLOAD_DIR = "/Users/santomukiza/Downloads"  # IMPORTANT: Change this to your actual downloads directory
DESTINATION_BASE_DIR = "/Users/santomukiza/Desktop" # IMPORTANT: Change this to your desired base directory for sorted files

# Define categories and their corresponding file extensions
# You can customize and add more categories as needed
FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".xls", ".xlsx", ".ppt", ".pptx"],
    "Videos": [".mp4", ".mov", ".avi", ".mkv", ".flv", ".wmv"],
    "Audio": [".mp3", ".wav", ".aac", ".flac", ".ogg"],
    "books":[".epub", ".mobi", ".azw3"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Executables": [".exe", ".dmg", ".app", ".msi"],
    "Code": [".py", ".js", ".html", ".css", ".java", ".c", ".cpp", ".h", ".json", ".xml"],
    "Spreadsheets": [".csv", ".xlsx", ".xls"], # Specific for spreadsheets, can be merged with Documents
    "Presentations": [".pptx", ".ppt"], # Specific for presentations, can be merged with Documents
    "Torrents": [".torrent"]
}

# List of temporary file extensions to ignore
# Add any other temporary file patterns you observe
IGNORED_EXTENSIONS = [
    ".crdownload",  # Chrome/Chromium incomplete downloads
    ".tmp",         # Temporary files
    ".part",        # Partial downloads (Firefox, etc.)
    ".download",    # Safari incomplete downloads
    ".company.thebrowser.Browser", # Specific temporary files observed in your output
    ".DS_Store"     # macOS specific metadata file
]

# --- Helper Functions ---

def create_directory_if_not_exists(directory_path):
    """Creates a directory if it doesn't already exist."""
    os.makedirs(directory_path, exist_ok=True)
    print(f"Ensured directory exists: {directory_path}")

def get_file_category(filename):
    """Determines the category of a file based on its extension."""
    _, file_extension = os.path.splitext(filename)
    file_extension = file_extension.lower()

    for category, extensions in FILE_CATEGORIES.items():
        if file_extension in extensions:
            return category
    return "Others" # Default category for unknown file types

def move_file(source_path, destination_dir):
    """Moves a file from source_path to destination_dir."""
    try:
        create_directory_if_not_exists(destination_dir)
        destination_path = os.path.join(destination_dir, os.path.basename(source_path))

        # Handle potential file name conflicts
        counter = 1
        original_destination_path = destination_path
        while os.path.exists(destination_path):
            name, ext = os.path.splitext(os.path.basename(original_destination_path))
            destination_path = os.path.join(destination_dir, f"{name}_{counter}{ext}")
            counter += 1

        shutil.move(source_path, destination_path)
        print(f"Moved: '{os.path.basename(source_path)}' to '{destination_dir}'")
    except Exception as e:
        print(f"Error moving file {source_path}: {e}")

# --- Event Handler Class ---

class FileSorterHandler(FileSystemEventHandler):
    """Handles file system events (like file creation)."""

    def on_created(self, event):
        """Called when a file or directory is created."""
        if not event.is_directory:
            file_path = event.src_path
            filename = os.path.basename(file_path)
            _, file_extension = os.path.splitext(filename)
            file_extension = file_extension.lower()

            # Ignore temporary/incomplete download files
            if file_extension in IGNORED_EXTENSIONS or filename.startswith('.'):
                print(f"Ignoring temporary or hidden file: {filename}")
                return

            print(f"Detected new file: {filename}")

            # Give the file a moment to be fully written to disk
            # This delay is still useful for large files even if not temporary
            time.sleep(1)

            if os.path.exists(file_path): # Check if the file still exists after the delay
                category = get_file_category(filename)
                destination_dir = os.path.join(DESTINATION_BASE_DIR, category)
                move_file(file_path, destination_dir)
            else:
                print(f"File {filename} disappeared before it could be processed.")

# --- Main Script Execution ---

if __name__ == "__main__":
    # Ensure the base destination directory exists
    create_directory_if_not_exists(DESTINATION_BASE_DIR)

    # Initialize the observer and event handler
    event_handler = FileSorterHandler()
    observer = Observer()

    # Schedule the observer to watch the download directory
    observer.schedule(event_handler, DOWNLOAD_DIR, recursive=False) # recursive=True if you want to watch subdirectories

    print(f"Starting file sorter. Monitoring '{DOWNLOAD_DIR}' for new files...")
    print("Press Ctrl+C to stop.")

    try:
        observer.start()
        while True:
            time.sleep(20) # Keep the main thread alive
    except KeyboardInterrupt:
        observer.stop()
        print("File sorter stopped.")
    observer.join()

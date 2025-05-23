"/Users/santomukiza/Downloads"
"/Users/santomukiza/Desktop"
import os
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

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

class FileHandler(FileSystemEventHandler):

    FILE_CATEGORIES = {
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
        "Documents": [".pdf", ".doc", ".docx", ".txt"],
        "Videos": [".mp4", ".mov", ".avi", ".mkv"],
        "Audio": [".mp3", ".wav", ".aac"],
        "Archives": [".zip", ".rar", ".tar", ".gz", ".7z"],
        "Executables": [".exe", ".msi", ".bin", ".app"],
        "Code": [".py", ".js", ".html", ".css", ".java"],
        "Books": [".epub", ".mobi"],
        "Spreadsheets": [".xls", ".xlsx", ".csv"],
        "Presentations": [".ppt", ".pptx"],
        "Torrents": [".torrent"]
    }

    def __init__(self, destination_folder):
        self.destination_folder = destination_folder

    def ensure_directory(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"Ensured directory exists: {path}")

    def is_temporary_file(self, filename):
        return any(filename.endswith(ext) for ext in IGNORED_EXTENSIONS)

    def move_file(self, src):
        """
        Move a file from `src` to its corresponding category folder.

        Files are renamed if a file with the same name already exists in the destination folder.
        The new name is created by appending a counter to the original filename (e.g., `document_1.pdf`).
        """
        file_ext = os.path.splitext(src)[1].lower()
        destination_category = next((category for category, extensions in self.FILE_CATEGORIES.items() if file_ext in extensions), "Others")
        destination_path = os.path.join(self.destination_folder, destination_category)

        self.ensure_directory(destination_path)

        filename = os.path.basename(src)
        final_destination = os.path.join(destination_path, filename)

        counter = 1
        while os.path.exists(final_destination):
            base, extension = os.path.splitext(filename)
            new_filename = f"{base}_{counter}{extension}"
            final_destination = os.path.join(destination_path, new_filename)
            counter += 1

        try:
            shutil.move(src, final_destination)
            print(f"Moved: '{filename}' to '{final_destination}'")
        except shutil.Error as e:
            print(f"Error moving file {src}: {e}")

    def on_created(self, event):
        if event.is_directory:
            return

        filename = os.path.basename(event.src_path)

        if self.is_temporary_file(filename) or filename.startswith('.'):
            print(f"Ignoring temporary or hidden file: {filename}")
            return

        time.sleep(1)  # Wait to ensure the file is completely written
        if os.path.exists(event.src_path):
            print(f"Detected new file: {filename}")
            self.move_file(event.src_path)
        else:
            print(f"File {filename} disappeared before it could be processed.")

def main():
    downloads_folder = os.path.expanduser("~/Downloads")# Adjust this path if necessary
    destination_folder = os.path.expanduser("~/Desktop")# Adjust this path if necessary

    event_handler = FileHandler(destination_folder)
    observer = Observer()
    observer.schedule(event_handler, downloads_folder, recursive=False)
    observer.start()

    print(f"Starting file sorter. Monitoring '{downloads_folder}' for new files...")
    print("Press Ctrl+C to stop.")

    try:
        while True:
            time.sleep(30)
    except KeyboardInterrupt:
        observer.stop()
        print("File sorter stopped.")

    observer.join()

if __name__ == "__main__":
    main()

# Automatic File Sorter

This Python script automatically sorts new files downloaded to a specified directory into categorized folders on your desktop. It uses `watchdog` to monitor the download directory in real-time and `shutil` to move files.

## Features

- **Real-time Monitoring**: Continuously watches your downloads folder for new files.
- **Category-based Sorting**: Organizes files into predefined categories:
  - Images
  - Documents
  - Videos
  - Audio
  - Archives
  - Executables
  - Code
  - Books
  - Spreadsheets
  - Presentations
  - Torrents
- **Customizable Categories**: Easily modify existing categories or add new ones based on file extensions.
- **Conflict Resolution**: Handles files with the same name by appending a counter (e.g., `document_1.pdf`).
- **Temporary File Ignoring**: Skips incomplete downloads and temporary system files.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

- Python 3.x
- `watchdog` library

### Installation

1. Clone the repository (or download the script):
   ```bash
   git clone https://github.com/Yo014/File-Sorter.git
   cd File-Sorter
2. Install the watchdog library:
    ```bash
    pip install watchdog

## Configuration

Open the `File-Sorter.py` file and modify the following variables to suit your needs:

### Directory Settings

```python
    downloads_folder = os.path.expanduser("~/Downloads")# Adjust this path if necessary
    destination_folder = os.path.expanduser("~/Desktop")# Adjust this path if necessary

```
Customize the file categories and their corresponding extensions in the `FILE_CATEGORIES` dictionary.

## Ignored Extensions
Add or remove temporary file extensions to ignore in the `IGNORED_EXTENSIONS` list.

## How to Run
1. Open your terminal or command prompt
2. Navigate to the directory containing `File-Sorter.py`
3. Execute the script:
```bash
python File-Sorter.py
```
## Script Behavior

The script will:
- Begin monitoring your `downloads_folder`
- Display terminal messages when files are detected and moved
- **To stop:** Press `Ctrl+C` in the terminal

## How It Works

The script uses the `watchdog` library's `Observer` to monitor `downloads_folder`:

### Event Detection
- `FileSorterHandler` (inherits from `FileSystemEventHandler`) listens for `on_created` events

### File Validation
- Verifies the item is a file (not directory)
- Ignores temporary/hidden files (based on `IGNORED_EXTENSIONS` and files starting with `.`)

### Processing Delay
- Includes `time.sleep(1)` to ensure complete file writes (especially for large files)

### Category Determination
- matches extensions to predefined categories
- Unrecognized extensions go to "Others"

### Directory Management
- `create_directory_if_not_exists()` ensures category folders exist in `DESTINATION_BASE_DIR`

### File Movement
- Uses `shutil.move` to transfer files
- Handles name conflicts by appending numbers (e.g., `document_1.pdf`)

## Customization

### Adding New Categories
To add new file categories, update the `FILE_CATEGORIES` dictionary with your desired extensions:

```python
FILE_CATEGORIES = {
    # Existing categories...
    "Fonts": [".ttf", ".otf", ".woff", ".woff2"],
    "MyCustomCategory": [".myext1", ".myext2"]
}
```
### Modifying Ignored Extensions
To change which files are ignored, update the `IGNORED_EXTENSIONS` list:
```python
IGNORED_EXTENSIONS = [
    # Existing extensions...
    ".some_temp_file_extension", 
    ".another_partial_download"
]
```
## Troubleshooting
### Files Not Moving
- Verify both DOWNLOAD_DIR and DESTINATION_BASE_DIR paths are correct

- Ensure the script has proper read/write permissions

- Check terminal output for any error messages

- Increase time.sleep() duration if working with large files or slow disks

## Credit
-  Santo Mukiza



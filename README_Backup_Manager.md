
# Backup Manager Script

## Overview
The Backup Manager is a Python script designed to copy files from a source directory to a destination directory. It ensures data integrity and avoids overwriting files by appending unique timestamps to duplicate filenames. This tool is ideal for creating regular backups of important files and preserving directory structures.

## Features
- **Directory Validation**: Ensures source and destination directories are valid.
- **Unique Filenames**: Appends timestamps to prevent overwriting files in the destination.
- **Preserve Directory Structure**: Maintains the relative path of files in the destination directory.
- **Metadata Preservation**: Retains file metadata (e.g., timestamps, permissions) during copying.
- **Error Resilience**: Continues the backup process even if some files fail.
- **Detailed Summary**: Provides a summary of the total, successful, and failed file operations.

## Usage
### Prerequisites
- Python 3.7 or higher.
- Required modules: `os`, `shutil`, `argparse`, `datetime`, `pathlib`.

### Command
Run the script from the command line as follows:
```bash
python backup.py <source_directory> <destination_directory>
```

### Example
```bash
python backup.py /path/to/source /path/to/destination
```

### Output Example
```
Copied: /path/to/source/file1.txt -> /path/to/destination/file1.txt
Copied: /path/to/source/file2.txt -> /path/to/destination/file2_20231124_153045.txt

Backup Summary:
Total files processed: 2
Successfully copied: 2
Failed copies: 0
```

## Implementation Details
### Key Functions
- **`validate_directories`**: Checks the existence and validity of source and destination directories.
- **`generate_unique_name`**: Generates a new file name with a timestamp if a file already exists.
- **`copy_file`**: Handles file copying and captures errors if any occur.
- **`backup_files`**: Orchestrates the backup process, iterates through files, and reports status.

### Error Handling
- Gracefully handles missing directories or permission issues.
- Logs errors for failed files and continues with the backup process.

### Directory Structure Preservation
If the source directory has nested subdirectories, their structure is mirrored in the destination directory.

## Exit Codes
- **0**: Backup completed successfully.
- **1**: Errors occurred during the backup.

## Notes
- Ensure the source directory exists and contains files to back up.
- The destination directory will be created if it does not already exist.

## License
This script is provided "as-is" without any warranties or guarantees.

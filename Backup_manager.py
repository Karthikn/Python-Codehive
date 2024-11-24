import os
import shutil
import argparse
from datetime import datetime
from pathlib import Path
from typing import Tuple


class BackupManager:
    def __init__(self, source_dir: str, dest_dir: str):
        self.source_dir = Path(source_dir)
        self.dest_dir = Path(dest_dir)

    def validate_directories(self) -> Tuple[bool, str]:
        """Validate source and destination directories."""
        if not self.source_dir.exists():
            return False, f"Source directory does not exist: {self.source_dir}"
        if not self.source_dir.is_dir():
            return False, f"Source path is not a directory: {self.source_dir}"

        try:
            self.dest_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            return False, f"Failed to create destination directory: {str(e)}"

        return True, ""

    def generate_unique_name(self, file_path: Path) -> Path:
        """Generate unique filename with timestamp if needed."""
        if not file_path.exists():
            return file_path

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        new_name = f"{file_path.stem}_{timestamp}{file_path.suffix}"
        return file_path.parent / new_name

    def copy_file(self, source_file: Path, dest_file: Path) -> Tuple[bool, str]:
        """Copy a single file with error handling."""
        try:
            shutil.copy2(source_file, dest_file)  # Preserve metadata
            return True, ""
        except Exception as e:
            return False, f"Failed to copy {source_file}: {str(e)}"

    def backup_files(self) -> bool:
        """Perform the backup operation."""
        # Validate directories
        is_valid, error_msg = self.validate_directories()
        if not is_valid:
            print(f"Error: {error_msg}")
            return False

        total_files = 0
        copied_files = 0
        failed_files = []

        try:
            for root, _, files in os.walk(self.source_dir):
                for file in files:
                    total_files += 1
                    source_file = Path(root) / file

                    # Maintain relative path structure
                    rel_path = Path(root).relative_to(self.source_dir)
                    dest_file = self.dest_dir / rel_path / file

                    # Create subdirectories if needed
                    dest_file.parent.mkdir(parents=True, exist_ok=True)

                    # Generate unique name if file exists
                    dest_file = self.generate_unique_name(dest_file)

                    # Copy file
                    is_copied, error = self.copy_file(source_file, dest_file)
                    if is_copied:
                        copied_files += 1
                        print(f"Copied: {source_file} -> {dest_file}")
                    else:
                        failed_files.append((source_file, error))

            # Summary
            print("\nBackup Summary:")
            print(f"Total files processed: {total_files}")
            print(f"Successfully copied: {copied_files}")
            print(f"Failed copies: {len(failed_files)}")

            if failed_files:
                print("\nFailed Files:")
                for failed_file, error in failed_files:
                    print(f"  {failed_file}: {error}")

            return len(failed_files) == 0

        except Exception as e:
            print(f"Unexpected error during backup: {str(e)}")
            return False


def main():
    parser = argparse.ArgumentParser(description="Backup files from source to destination directory")
    parser.add_argument("source", help="Source directory path")
    parser.add_argument("destination", help="Destination directory path")
    args = parser.parse_args()

    backup_manager = BackupManager(args.source, args.destination)
    success = backup_manager.backup_files()
    exit(0 if success else 1)


if __name__ == "__main__":
    main()

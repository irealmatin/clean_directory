import shutil  # for moving files
from collections import Counter  # for counting file extensions
from pathlib import Path  # for working with file paths

from loguru import logger  # for logging

from src.data import DATA_DIR  # directory containing data files
from src.utils.io import read_json  # for reading JSON files


class cleanfiles:
    """
    A class for organizing files in a directory by moving them to different
    directories based on their file extensions.
    """
    
    def __init__(self, directory):
        """
        Initializes a new instance of the cleanfiles class.
        
        Args:
            directory (str): The path to the directory to clean.
        """
        
        self.directory = Path(directory)
        
        # Check that the directory exists.
        if not self.directory.exists():
            raise FileNotFoundError(f"{self.directory} does not exist")
        
        # Read the extension.json file and create a dictionary that maps file
        # extensions to destination directories.
        ext_d = read_json(DATA_DIR / 'extension.json')
        self.extension_dest = {}
        for dir_name, ext_list in ext_d.items():
            for ext in ext_list:
                self.extension_dest[ext] = dir_name
            print(self.extension_dest)

    def __call__(self):
        """
        Organizes files in a directory by moving them to different directories
        based on their file extensions.
        """
        
        logger.info(f"Cleaning files in {self.directory}...")
        
        file_extensions = []  # a list to hold the file extensions of all files
        
        for file_path in self.directory.iterdir():
            # Ignore directories.
            if file_path.is_dir():
                continue
            
            # Ignore hidden files.
            if file_path.name.startswith('.'):
                continue
            
            # Move the file to the appropriate destination directory based
            # on its file extension.
            file_extensions.append(file_path.suffix)
            if file_path.suffix not in self.extension_dest:
                DEST_DIR = self.directory / 'other'
            else:
                DEST_DIR = self.directory / self.extension_dest[file_path.suffix]
            
            DEST_DIR.mkdir(exist_ok=True)  # create the destination directory if it doesn't exist
            logger.info(f"Moving {file_path} to {DEST_DIR}...")
            shutil.move(str(file_path), str(DEST_DIR))

if __name__ == "__main__":
    # Create an instance of the cleanfiles class with the specified directory
    # and call its __call__ method to organize the files in the directory.
    org_file = cleanfiles("/mnt/c/Users/ireal/Downloads") # give your directory
    org_file()
    print('Done........ !!!')

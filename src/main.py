import shutil
from collections import Counter
from pathlib import Path

from loguru import logger

from src.data import DATA_DIR
from src.utils.io import read_json


class cleanfiles :
    """
    this class is used to clean files in a directory
    by moving file into directoris based on extensions .
    """
    def __init__(self,directory):
        self.directory = Path(directory)
        if not self.directory.exists():
            raise FileNotFoundError(f"{self.directory} does not exist")

        
        ext_d = read_json(DATA_DIR / 'extension.json')
        self.extension_dest = {}
        for dir_name , ext_list in ext_d.items():
            for ext in ext_list :
                self.extension_dest[ext] = dir_name
            print(self.extension_dest)    


    def __call__ (self):
        """
        organize files in a directory by moving them
        to directory based on extesions
        """
        logger.info(f"clean files in {self.directory}...")
        file_extensions = []
        for file_path in self.directory.iterdir():
           #ignor directories
           if file_path.is_dir():
               continue
    
           # ignor hidden files
           if file_path.name.startswith('.'):
               continue
        
          # move file
           file_extensions.append(file_path.suffix)
           if file_path.suffix not in self.extension_dest:
               DEST_DIR = self.directory / 'other'
           else :
              DEST_DIR = self.directory / self.extension_dest [file_path.suffix]
        
           DEST_DIR.mkdir(exist_ok = True)
           logger.info(f"moving{file_path} to {DEST_DIR}....")
           shutil.move(str(file_path) , str(DEST_DIR))


if __name__ == "__main__":
      org_file = cleanfiles("/mnt/c/Users/ireal/Downloads")
      org_file()
      print('Done !!')
            

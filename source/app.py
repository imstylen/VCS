from genericpath import isdir
import os

from file import File

class Application:
    
    def __init__(self, in_directory:str):
        self.directory:str = in_directory
        self.backup_folder:str = self.setup_backup_folder()
        
        self.files:list(File) = []
        self.update()
        
    def setup_backup_folder(self) -> str:
        new_backup_folder:str = self.directory + "/.backup"
        
        if not os.path.exists(new_backup_folder):
            os.mkdir(new_backup_folder)
        
        return new_backup_folder
        
    def update(self) -> None:
        items = os.listdir(self.directory)
    
        for item in items:
            
            if os.path.isdir(self.directory + "/" + item):
                print("Skipping directory: " + item)
                continue
            
            filtered_items = filter(lambda file: file.file_path == item, self.files)
            found_files = list(filtered_items)
            
            file_handle:File = None
            
            if found_files == []:
                file_handle = File(self, self.directory + "/" + item)
                self.files.append(file_handle)
            else:
                print("Found: " + item + "... Skipping")
                file_handle = found_files[0]
            
            file_handle.check()
            
    def loop(self) -> None:
        pass
        #sleep for a bit, then call update()
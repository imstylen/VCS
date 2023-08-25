import os
import datetime
import shutil

from app import Application

class File:
    
    def __init__(self, in_app:Application, in_path:str):
        self.app = in_app
        self.file_path:str = in_path
        self.m_time = None
        
    def check(self):
        new_m_time = os.path.getmtime(self.file_path)
        
        if self.m_time:
            if new_m_time > self.m_time:
                self.m_time = new_m_time
                self.backup()
        else:
            self.m_time = new_m_time
            self.backup()
                
    def backup(self):
        print("Backing up: " + self.file_path)
        
        path_part_list = self.file_path.split(".")
        
        backup_path = self.app.backup_folder + "/" + path_part_list[:-1] + self.get_time_string() + "." + path_part_list[-1]
        print(backup_path)
        
        #use shutil to copy
    
    def get_time_string() -> str:
        current_datetime = datetime.datetime.now()
        desired_format = current_datetime.strftime("%Y%m%d%H%M")
        return desired_format
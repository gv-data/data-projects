import os, shutil, sys
from os import listdir

class Search:
    def __init__(self, source_directory):
        self.source_directory = source_directory
        self.target_directory = source_directory + 'target'

    # Create target directory
    def create_directory(self):
        if os.path.exists(self.target_directory):
            shutil.rmtree(self.target_directory)
        os.makedirs(self.target_directory)
    
    def copy_files(self): 
        self.create_directory()

        # Capture all pbix files
        file_list = []
        file_target_list = []
        for file in os.listdir(self.source_directory):
            if file.endswith('.pbix'):
                file_list.append(self.source_directory + file)
                file_target_list.append(self.target_directory + file)
        
        # Copy files to target directory
        for file in file_list:
            shutil.copy(file, self.target_directory)      

        # Replace .pbix with .zip
        for file in os.listdir(self.target_directory):
            old_file = os.path.join(self.target_directory, file)
            new_file = old_file.replace('.pbix','.zip')
            os.rename(old_file, new_file)
    
    def capture_input(self):
        text = input('Enter a measure, column, or entity: ')
        return text




    
directory = '/mnt/c/Reports/'
app = Search(directory)
app.copy_files()
print(app.capture_input())


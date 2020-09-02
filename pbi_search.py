import os, shutil, sys, zipfile
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
    
    def unzip(self, target_directory):
        folder_list = []
        for file in os.listdir(target_directory):
            src_file_path = target_directory + '/' + file
            dest_file_path = src_file_path.replace('.zip','')
            with zipfile.ZipFile(src_file_path,'r') as zip_ref:
                zip_ref.extractall(dest_file_path)
                folder_list.append(dest_file_path)
        return folder_list

    def search(self):
        text = self.capture_input()
        folders = self.unzip(self.target_directory)
        paths = []
        for folder in folders:
            layout_file = folder + '/Report/Layout'
            layout_text = layout_file + '.txt' 
            os.rename(layout_file, layout_text)
            os.chdir(folder + '/Report')
            print(os.getcwd())
            
            '''
            with open('Layout.txt','r') as f:
                search_lines = f.readlines()
            for i, line in enumerate(search_lines):                
                if text in line:
                    for l in search_lines[i:i+3:]:
                        print(l)
                        paths.append(l)
            '''
            
            search_file = open('Layout.txt', 'r')
            for i, line in enumerate(search_file):
                line = line.strip().lower()
                text = text.strip().lower()
                print(i, text, len(line), len(text), line.count(text))
                if line.count(text) > 0:
                #if text.lower() in line.lower():
                    if folder not in paths:
                        paths.append(folder)
            search_file.close()
            
            '''
            with open('Layout.txt','r') as f:
                print('Searching ' + text + ' in ' + layout_text)
                print(any(text in line for line in f))
                if text in f.read():
                    paths.append(folder)
            '''
        print(paths)
        return paths




    
directory = '/mnt/c/Reports/'
app = Search(directory)
app.copy_files()
#print(app.capture_input())
#print(app.unzip(directory + 'target/'))
print(app.search())

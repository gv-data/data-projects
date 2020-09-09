import os, shutil, sys, zipfile, codecs
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

    
    def search_file(self, file, text):
        read_obj = codecs.open(file, 'r', 'utf-16-le')
        for line in read_obj:
            if text in line:
                return True
        read_obj.close()
        return False


    def search_directory(self):
        text = self.capture_input()
        folders = self.unzip(self.target_directory)
        paths = []
        for folder in folders:
            layout_file = folder + '/Report/Layout'
            layout_text = layout_file + '.txt' 
            os.rename(layout_file, layout_text)
            os.chdir(folder + '/Report')
            print(os.getcwd())

            if self.search_file('Layout.txt', text):
                paths.append(folder)
        return paths




directory = '/mnt/c/Reports/'
app = Search(directory)
app.copy_files()
#print(app.capture_input())
#print(app.unzip(directory + 'target/'))
print(app.search_directory())

'''
test_directory = '/mnt/c/Test/'
test_app = Search(test_directory)
test_file='/mnt/c/Test/Layout.txt'
text = 'Man'
test_app.search_file(test_file, text)
'''
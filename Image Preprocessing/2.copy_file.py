import os
import shutil

def copy_files(source_folder, target_folder, file_end):
    subfolder = next(os.walk(source_folder))[1]
    for sub in subfolder:
        person_folder = source_folder + "/" + sub
        # print(person_folder)

        for file in os.listdir(person_folder):
            if file.endswith(file_end):
                old_path = person_folder + "/" + file
                # print(old_path)
                new_path = os.path.join(target_folder, file)
                # print(new_path)
                shutil.copyfile(old_path,new_path)
            
source_folder = 'Path/to/source_folder'
target_folder = 'Path/to/target_folder'
file_end = 'mask.png'

copy_files(source_folder, target_folder, file_end)
import os
import shutil
    
def copystatic(dir_path, destination_path):
    if os.path.isdir(destination_path):
        shutil.rmtree(destination_path)
    os.mkdir(destination_path)
    copy_rec(dir_path, destination_path)

def copy_rec(dir_path, destination_path):
    dir_list = os.listdir(dir_path)
    for item in dir_list:
        item_path = os.path.abspath(os.path.join(dir_path, item))
        if os.path.isfile(item_path):
            shutil.copy(item_path, destination_path)
        else:
            rec_dir = os.path.join(destination_path, item)
            os.mkdir(rec_dir)
            copy_rec(item_path, rec_dir)


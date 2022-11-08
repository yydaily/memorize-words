import os

def mkdir(dir_path):
    if os.path.exists(dir_path):
        for i in os.listdir(dir_path):
            file_path = dir_path + '/' + i
            os.remove(file_path)
    else:
        os.makedirs(dir_path)
